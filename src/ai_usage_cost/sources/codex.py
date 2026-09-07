from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path

from ..models import TokenUsage, UsageEvent
from .base import Source, jsonl_files, parse_timestamp, project_of, read_json_lines

RECONCILE_TOLERANCE = 0.01
RECONCILE_MIN_TOKENS = 1000

_ORIGINATOR_CLIENTS = {
    "Codex Desktop": "codex-desktop",
    "codex_work_desktop": "codex-desktop",
    "codex_cli_rs": "codex-cli",
}


def default_roots() -> list[Path]:
    return [Path.home() / ".codex" / "sessions"]


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    model = ""
    session_id = _session_id_from_name(path)
    project: str | None = None
    cwd: str | None = None
    client = "codex-cli"
    provider: str | None = None
    repository: str | None = None
    branch: str | None = None
    is_sidechain = False
    summed = TokenUsage()
    final_total: dict | None = None

    for record in read_json_lines(path, warnings):
        payload = record.get("payload")
        payload = payload if isinstance(payload, dict) else record
        kind = payload.get("type") or record.get("type")

        if kind == "session_meta" or record.get("type") == "session_meta":
            client = _client_of(payload.get("originator"))
            if isinstance(payload.get("model_provider"), str):
                provider = payload["model_provider"]
            git = payload.get("git")
            if isinstance(git, dict):
                repository = git.get("repository_url") or repository
                branch = git.get("branch") or branch
            if isinstance(payload.get("source"), dict) and "subagent" in payload["source"]:
                is_sidechain = True

        found_model = _find_model(payload)
        if found_model:
            model = found_model
        found_session = _find_session_id(payload)
        if found_session:
            session_id = found_session
        found_cwd = _find_raw_cwd(payload)
        if found_cwd:
            cwd = found_cwd
            project = project_of(found_cwd)

        if kind != "token_count":
            continue

        info = payload.get("info")
        info = info if isinstance(info, dict) else payload
        last = info.get("last_token_usage")
        total = info.get("total_token_usage")

        if isinstance(total, dict):
            final_total = total
        if not isinstance(last, dict):
            continue

        tokens = _tokens_from_usage(last)
        if tokens.total == 0:
            continue
        summed = summed + tokens

        yield UsageEvent(
            source="codex",
            client=client,
            provider=provider,
            model=model or None,
            timestamp=parse_timestamp(record.get("timestamp") or payload.get("timestamp"), path),
            session_id=session_id,
            tokens=tokens,
            is_sidechain=is_sidechain,
            project=project,
            working_directory=cwd,
            repository=repository,
            branch=branch,
            source_file=str(path),
        )

    _reconcile(path, summed, final_total, warnings)


def _client_of(originator: object) -> str:
    if isinstance(originator, str) and originator:
        mapped = _ORIGINATOR_CLIENTS.get(originator)
        if mapped:
            return mapped
        return re.sub(r"[^a-z0-9]+", "-", originator.lower()).strip("-") or "codex-cli"
    return "codex-cli"


def _reconcile(
    path: Path, summed: TokenUsage, final_total: dict | None, warnings: list[str]
) -> None:
    if final_total is None:
        return
    reported = _int(final_total.get("total_tokens"))
    if reported <= 0:
        return
    drift = abs(summed.total - reported)
    if drift > RECONCILE_MIN_TOKENS and drift / reported > RECONCILE_TOLERANCE:
        warnings.append(
            f"codex: {path.name}: summed turns {summed.total:,} vs session total "
            f"{reported:,} ({drift / reported:.1%} drift)"
        )


def _tokens_from_usage(usage: dict) -> TokenUsage:
    total_input = _int(usage.get("input_tokens"))
    cached = _int(usage.get("cached_input_tokens"))
    if total_input:
        cached = min(cached, total_input)
    return TokenUsage(
        uncached_input=max(0, total_input - cached),
        cache_read=cached,
        cache_write_5m=_int(usage.get("cache_write_input_tokens")),
        output=_int(usage.get("output_tokens")),
        reasoning_output=_int(usage.get("reasoning_output_tokens")),
    )


def _find_model(payload: dict) -> str:
    for candidate in (
        payload.get("model"),
        _nested(payload, "turn_context", "model"),
        _nested(payload, "info", "model"),
        _nested(payload, "model", "slug"),
    ):
        if isinstance(candidate, str) and candidate:
            return candidate
    return ""


def _find_session_id(payload: dict) -> str:
    for candidate in (payload.get("id"), payload.get("session_id"), payload.get("conversation_id")):
        if isinstance(candidate, str) and len(candidate) >= 8:
            return candidate
    return ""


def _find_raw_cwd(payload: dict) -> str | None:
    for candidate in (payload.get("cwd"), _nested(payload, "turn_context", "cwd")):
        if isinstance(candidate, str) and candidate:
            return candidate
    return None


def _nested(payload: dict, *keys: str) -> object:
    current: object = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _session_id_from_name(path: Path) -> str:
    stem = path.stem
    parts = stem.split("-")
    return "-".join(parts[-5:]) if len(parts) >= 5 else stem


def _int(value: object) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


SOURCE = Source(
    id="codex",
    label="Codex",
    clients={"codex-cli": "Codex CLI", "codex-desktop": "Codex Desktop"},
    default_roots=default_roots,
    files=jsonl_files,
    parse=parse,
)
