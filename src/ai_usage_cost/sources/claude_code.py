from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from ..models import TokenUsage, UsageEvent
from .base import Source, jsonl_files, parse_timestamp, project_of, read_json_lines

SYNTHETIC_MODELS = {"<synthetic>", "synthetic"}


def default_roots() -> list[Path]:
    home = Path.home()
    return [home / ".claude" / "projects", home / ".config" / "claude" / "projects"]


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    session_id = path.stem
    for record in read_json_lines(path, warnings):
        if record.get("type") != "assistant":
            continue
        message = record.get("message")
        if not isinstance(message, dict):
            continue
        usage = message.get("usage")
        if not isinstance(usage, dict):
            continue

        model = str(message.get("model") or "")
        if not model or model in SYNTHETIC_MODELS:
            continue

        tokens = _tokens_from_usage(usage)
        if tokens.total == 0:
            continue

        message_id = message.get("id")
        request_id = message.get("requestId") or record.get("requestId")
        cwd = record.get("cwd")

        yield UsageEvent(
            source="claude-code",
            client="claude-code",
            model=model,
            timestamp=parse_timestamp(record.get("timestamp"), path),
            session_id=str(record.get("sessionId") or session_id),
            request_id=str(message_id or request_id) if (message_id or request_id) else None,
            tokens=tokens,
            is_sidechain=bool(record.get("isSidechain")),
            tier=_tier(usage),
            project=_project_name(record, path),
            working_directory=cwd if isinstance(cwd, str) else None,
            branch=record.get("gitBranch") if isinstance(record.get("gitBranch"), str) else None,
            source_file=str(path),
        )


def _tokens_from_usage(usage: dict) -> TokenUsage:
    creation = usage.get("cache_creation")
    write_5m = write_1h = 0
    if isinstance(creation, dict):
        write_5m = _int(creation.get("ephemeral_5m_input_tokens"))
        write_1h = _int(creation.get("ephemeral_1h_input_tokens"))
    if write_5m == 0 and write_1h == 0:
        write_5m = _int(usage.get("cache_creation_input_tokens"))

    details = usage.get("output_tokens_details")
    thinking = _int(details.get("thinking_tokens")) if isinstance(details, dict) else 0

    return TokenUsage(
        uncached_input=_int(usage.get("input_tokens")),
        cache_read=_int(usage.get("cache_read_input_tokens")),
        cache_write_5m=write_5m,
        cache_write_1h=write_1h,
        output=_int(usage.get("output_tokens")),
        reasoning_output=thinking,
    )


def _tier(usage: dict) -> str:
    if usage.get("speed") == "fast":
        return "fast"
    if usage.get("service_tier") == "batch":
        return "batch"
    return "standard"


def _project_name(record: dict, path: Path) -> str | None:
    name = project_of(record.get("cwd"))
    if name:
        return name
    return path.parent.name.strip("-").split("-")[-1] or path.parent.name


def _int(value: object) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


SOURCE = Source(
    id="claude-code",
    label="Claude Code",
    clients={"claude-code": "Claude Code"},
    default_roots=default_roots,
    files=jsonl_files,
    parse=parse,
)
