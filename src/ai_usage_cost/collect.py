from __future__ import annotations

import json
import platform
import shutil
import sqlite3
import subprocess
import time
import urllib.request
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel

from . import store

SAMPLES_DDL = """
CREATE TABLE IF NOT EXISTS samples (
  machine TEXT NOT NULL, sampled_at TEXT NOT NULL,
  gpu_util REAL, vram_used INTEGER, vram_total INTEGER,
  power_w REAL, source TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS samples_machine_time ON samples(machine, sampled_at);
"""

OLLAMA_PS_URL = "http://127.0.0.1:11434/api/ps"

NVIDIA_SMI_COMMAND = [
    "nvidia-smi",
    "--query-gpu=utilization.gpu,memory.used,memory.total,power.draw",
    "--format=csv,noheader,nounits",
]

PERF_COUNTER_SCRIPT = (
    "$u = (Get-Counter '\\GPU Engine(*)\\Utilization Percentage' "
    "-ErrorAction SilentlyContinue).CounterSamples "
    "| Measure-Object -Property CookedValue -Sum; "
    "$m = (Get-Counter '\\GPU Adapter Memory(*)\\Dedicated Usage' "
    "-ErrorAction SilentlyContinue).CounterSamples "
    "| Measure-Object -Property CookedValue -Maximum; "
    "Write-Output ($u.Sum.ToString([cultureinfo]::InvariantCulture) + ' ' "
    "+ $m.Maximum.ToString([cultureinfo]::InvariantCulture))"
)

_MIB = 1024 * 1024


class Sample(BaseModel):
    machine: str
    sampled_at: datetime
    gpu_util: float | None = None
    vram_used: int | None = None
    vram_total: int | None = None
    power_w: float | None = None
    source: str


def ensure_samples_table(conn: sqlite3.Connection) -> None:
    conn.executescript(SAMPLES_DDL)
    conn.commit()


def insert_sample(conn: sqlite3.Connection, sample: Sample) -> None:
    conn.execute(
        "INSERT INTO samples "
        "(machine, sampled_at, gpu_util, vram_used, vram_total, power_w, source) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            sample.machine, sample.sampled_at.isoformat(), sample.gpu_util,
            sample.vram_used, sample.vram_total, sample.power_w, sample.source,
        ),
    )
    conn.commit()


ROCM_SMI_COMMAND = ("rocm-smi", "--showuse", "--showmemuse", "--showpower", "--json")


def select_backend() -> str | None:
    if shutil.which("nvidia-smi"):
        return "nvidia-smi"
    if shutil.which("rocm-smi"):
        return "rocm-smi"
    if shutil.which("powershell"):
        return "perf-counters"
    return None


def parse_rocm_smi(output: str) -> tuple[float, int | None, int | None, float | None] | None:
    try:
        payload = json.loads(output)
    except ValueError:
        return None
    cards = [
        value
        for key, value in payload.items()
        if key.startswith("card") and isinstance(value, dict)
    ]
    if not cards:
        return None
    card = cards[0]
    use = _first_number(card, ("GPU use (%)", "GPU use (%%)"))
    if use is None:
        return None
    used = _first_number(card, ("GPU Memory Allocated (VRAM%)",))
    total = _first_number(card, ("GPU memory total (B)", "VRAM Total Memory (B)"))
    used_bytes = _first_number(card, ("VRAM Total Used Memory (B)",))
    power = _first_number(
        card,
        ("Average Graphics Package Power (W)", "Current Socket Graphics Package Power (W)"),
    )
    if used_bytes is None and used is not None and total is not None:
        used_bytes = total * used / 100
    return (
        use / 100,
        None if used_bytes is None else int(used_bytes),
        None if total is None else int(total),
        power,
    )


def _first_number(card: dict, keys: Sequence[str]) -> float | None:
    for key in keys:
        value = card.get(key)
        if isinstance(value, int | float) and not isinstance(value, bool):
            return float(value)
        if isinstance(value, str):
            number = _number(value.strip())
            if number is not None:
                return number
    return None


def _number(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def _scaled_int(value: str, scale: int) -> int | None:
    number = _number(value)
    return None if number is None else int(number * scale)


def _run(command: Sequence[str], timeout: float) -> str | None:
    try:
        completed = subprocess.run(
            list(command), capture_output=True, text=True, timeout=timeout, check=False
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout


def parse_nvidia_smi(text: str) -> tuple[float, int | None, int | None, float | None] | None:
    for line in text.splitlines():
        fields = [field.strip() for field in line.split(",")]
        if len(fields) != 4:
            continue
        util = _number(fields[0])
        if util is None:
            continue
        return (
            util / 100.0,
            _scaled_int(fields[1], _MIB),
            _scaled_int(fields[2], _MIB),
            _number(fields[3]),
        )
    return None


def read_perf_counters() -> tuple[float, int] | None:
    output = _run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", PERF_COUNTER_SCRIPT], 30.0
    )
    if output is None:
        return None
    fields = output.split()
    if len(fields) != 2:
        return None
    util = _number(fields[0])
    used = _number(fields[1])
    if util is None or used is None:
        return None
    return util / 100.0, int(used)


def ollama_loaded(timeout: float = 0.5) -> str | None:
    try:
        with urllib.request.urlopen(OLLAMA_PS_URL, timeout=timeout) as response:
            payload = json.loads(response.read())
    except (OSError, ValueError):
        return None
    models = payload.get("models") if isinstance(payload, dict) else None
    if not models:
        return None
    return ",".join(
        f"{model.get('name', 'unknown')}={model.get('size_vram', 0)}" for model in models
    )


def sample_once(backend: str | None = None) -> Sample | None:
    backend = backend or select_backend()
    if backend == "nvidia-smi":
        output = _run(NVIDIA_SMI_COMMAND, 10.0)
        parsed = parse_nvidia_smi(output) if output is not None else None
        if parsed is None:
            return None
        gpu_util, vram_used, vram_total, power_w = parsed
    elif backend == "rocm-smi":
        output = _run(ROCM_SMI_COMMAND, 10.0)
        parsed = parse_rocm_smi(output) if output is not None else None
        if parsed is None:
            return None
        gpu_util, vram_used, vram_total, power_w = parsed
    elif backend == "perf-counters":
        counters = read_perf_counters()
        if counters is None:
            return None
        gpu_util, vram_used = counters
        vram_total = None
        power_w = None
    else:
        return None

    loaded = ollama_loaded()
    return Sample(
        machine=platform.node(),
        sampled_at=datetime.now(tz=UTC),
        gpu_util=gpu_util,
        vram_used=vram_used,
        vram_total=vram_total,
        power_w=power_w,
        source=backend if loaded is None else f"{backend}+ollama[{loaded}]",
    )


def energy_kwh(samples: Sequence[Sample], tdp_watts: float | None) -> float | None:
    if tdp_watts is None:
        return None
    joules = 0.0
    previous: Sample | None = None
    for sample in samples:
        if previous is not None and sample.gpu_util is not None:
            seconds = (sample.sampled_at - previous.sampled_at).total_seconds()
            joules += tdp_watts * sample.gpu_util * seconds
        previous = sample
    return joules / 3_600_000.0


def collect(
    db_path: Path | str,
    interval: float,
    tdp_watts: float | None,
    duration: float | None = None,
) -> tuple[list[Sample], float | None]:
    conn = store.open_store(db_path)
    ensure_samples_table(conn)
    backend = select_backend()
    samples: list[Sample] = []
    started = time.monotonic()
    try:
        while duration is None or time.monotonic() - started < duration:
            sample = sample_once(backend)
            if sample is not None:
                insert_sample(conn, sample)
                samples.append(sample)
            time.sleep(interval)
    except KeyboardInterrupt:
        pass
    finally:
        conn.close()
    return samples, energy_kwh(samples, tdp_watts)
