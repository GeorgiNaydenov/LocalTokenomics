from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from ai_usage_cost import collect as collect_module
from ai_usage_cost import store
from ai_usage_cost.collect import (
    Sample,
    collect,
    energy_kwh,
    ensure_samples_table,
    parse_nvidia_smi,
    sample_once,
)

NVIDIA_CSV = "37, 1024, 8192, 91.42\n"
NVIDIA_CSV_NO_POWER = "0, 512, 8192, [N/A]\n"


def _sample(second: int, gpu_util: float = 0.5) -> Sample:
    return Sample(
        machine="test-machine",
        sampled_at=datetime(2026, 9, 8, 12, 0, second, tzinfo=UTC),
        gpu_util=gpu_util,
        vram_used=1_000,
        source="fake",
    )


def _rows(db_path: Path) -> list[tuple]:
    conn = store.open_store(db_path)
    try:
        return conn.execute(
            "SELECT machine, sampled_at, gpu_util, vram_used, vram_total, power_w, source "
            "FROM samples ORDER BY sampled_at"
        ).fetchall()
    finally:
        conn.close()


def _fake_sampler(samples: list[Sample | None]):
    pending = list(samples)

    def sampler(backend: str | None = None) -> Sample | None:
        if not pending:
            raise KeyboardInterrupt
        return pending.pop(0)

    return sampler


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(collect_module.time, "sleep", lambda _: None)


def test_ensure_samples_table_is_idempotent(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    try:
        ensure_samples_table(conn)
        ensure_samples_table(conn)
        assert conn.execute("SELECT COUNT(*) FROM samples").fetchone()[0] == 0
    finally:
        conn.close()


def test_collect_writes_a_row_per_sample(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db_path = tmp_path / "usage.db"
    monkeypatch.setattr(collect_module, "select_backend", lambda: "fake")
    monkeypatch.setattr(
        collect_module, "sample_once", _fake_sampler([_sample(0), _sample(2), _sample(4)])
    )

    samples, energy = collect(db_path, interval=2.0, tdp_watts=None)

    assert len(samples) == 3
    assert energy is None
    rows = _rows(db_path)
    assert len(rows) == 3
    assert rows[0] == ("test-machine", "2026-09-08T12:00:00+00:00", 0.5, 1000, None, None, "fake")


def test_collect_inserts_nothing_when_no_backend_is_available(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    db_path = tmp_path / "usage.db"
    monkeypatch.setattr(collect_module, "select_backend", lambda: None)
    monkeypatch.setattr(collect_module, "sample_once", _fake_sampler([None, None]))

    samples, _ = collect(db_path, interval=2.0, tdp_watts=100.0)

    assert samples == []
    assert _rows(db_path) == []


def test_sample_once_returns_none_without_a_backend(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(collect_module, "select_backend", lambda: None)
    assert sample_once() is None


def test_energy_is_unavailable_without_a_tdp() -> None:
    assert energy_kwh([_sample(0), _sample(10)], None) is None


def test_energy_sums_tdp_times_utilisation_times_elapsed() -> None:
    samples = [_sample(0, gpu_util=0.5), _sample(10, gpu_util=0.5)]
    assert energy_kwh(samples, 200.0) == pytest.approx(1000.0 / 3_600_000.0)


def test_energy_of_a_single_sample_is_zero() -> None:
    assert energy_kwh([_sample(0)], 200.0) == 0.0


def test_nvidia_smi_output_is_parsed_into_measured_values() -> None:
    assert parse_nvidia_smi(NVIDIA_CSV) == (0.37, 1024 * 1024 * 1024, 8192 * 1024 * 1024, 91.42)


def test_nvidia_smi_reports_no_power_when_the_driver_says_not_available() -> None:
    parsed = parse_nvidia_smi(NVIDIA_CSV_NO_POWER)
    assert parsed is not None
    assert parsed[0] == 0.0
    assert parsed[3] is None


def test_unparseable_nvidia_smi_output_yields_no_sample() -> None:
    assert parse_nvidia_smi("no supported devices were found\n") is None


def test_rocm_smi_output_is_parsed() -> None:
    output = json.dumps(
        {
            "card0": {
                "GPU use (%)": "42",
                "VRAM Total Memory (B)": "17163091968",
                "VRAM Total Used Memory (B)": "5368709120",
                "Average Graphics Package Power (W)": "138.0",
            }
        }
    )
    parsed = collect_module.parse_rocm_smi(output)
    assert parsed == (0.42, 5368709120, 17163091968, 138.0)


def test_rocm_smi_without_power_reports_none() -> None:
    output = json.dumps({"card0": {"GPU use (%)": "7", "VRAM Total Memory (B)": "8589934592"}})
    parsed = collect_module.parse_rocm_smi(output)
    assert parsed is not None
    assert parsed[0] == 0.07
    assert parsed[3] is None


def test_rocm_smi_rejects_output_without_a_card() -> None:
    assert collect_module.parse_rocm_smi(json.dumps({"system": {"driver": "1"}})) is None
