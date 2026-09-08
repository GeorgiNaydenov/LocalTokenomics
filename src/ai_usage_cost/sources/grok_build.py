from __future__ import annotations

import json
import os
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import unquote

from ..models import TokenUsage, UsageEvent
from ..trace import Capabilities
from .base import Source, as_int, parse_timestamp, project_of, read_json_lines


def default_roots() -> list[Path]:
    home_env = os.environ.get("GROK_HOME", "").strip()
    root = Path(home_env) if home_env else Path.home() / ".grok"
    return [root / "sessions"]


def session_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("updates.jsonl") if p.is_file())


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    session_id, cwd, default_model = _session_meta(path)
    project = project_of(cwd)

    for record in read_json_lines(path, warnings):
        params = record.get("params")
        if not isinstance(params, dict):
            continue
        update = params.get("update")
        if not isinstance(update, dict) or update.get("sessionUpdate") != "turn_completed":
            continue
        usage = update.get("usage")
        if not isinstance(usage, dict):
            continue

        meta = params.get("_meta")
        meta = meta if isinstance(meta, dict) else {}
        event_id = meta.get("eventId")
        event_id = event_id if isinstance(event_id, str) and event_id else None
        timestamp = parse_timestamp(meta.get("agentTimestampMs") or record.get("timestamp"), path)
        session = params.get("sessionId")
        session = session if isinstance(session, str) and session else session_id

        for model, model_usage in _model_usage_rows(usage, default_model):
            tokens = _tokens_from_usage(model_usage)
            if tokens.total == 0:
                continue
            yield UsageEvent(
                source="grok-build",
                client="grok-build",
                model=model,
                timestamp=timestamp,
                session_id=session,
                request_id=f"grok-build:{event_id}:{model}" if event_id else None,
                tokens=tokens,
                project=project,
                working_directory=cwd,
                source_file=str(path),
            )


def _session_meta(path: Path) -> tuple[str, str | None, str | None]:
    session_dir = path.parent
    session_id = session_dir.name
    cwd = unquote(session_dir.parent.name) if session_dir.parent.name else None
    default_model: str | None = None

    summary_path = session_dir / "summary.json"
    if summary_path.is_file():
        try:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            summary = {}
        info = summary.get("info")
        info = info if isinstance(info, dict) else {}
        info_id = info.get("id")
        if isinstance(info_id, str) and info_id:
            session_id = info_id
        info_cwd = info.get("cwd") or summary.get("git_root_dir")
        if isinstance(info_cwd, str) and info_cwd:
            cwd = info_cwd
        model_id = summary.get("current_model_id")
        if isinstance(model_id, str) and model_id:
            default_model = model_id

    return session_id, cwd, default_model


def _model_usage_rows(usage: dict, default_model: str | None) -> list[tuple[str, dict]]:
    model_usage = usage.get("modelUsage")
    if isinstance(model_usage, dict) and model_usage:
        return [(model, row) for model, row in model_usage.items() if isinstance(row, dict)]
    return [(default_model or "unknown", usage)]


def _tokens_from_usage(usage: dict) -> TokenUsage:
    input_tokens = as_int(usage.get("inputTokens"))
    cache_read = min(as_int(usage.get("cachedReadTokens")), input_tokens)
    uncached = max(0, input_tokens - cache_read)
    cache_write = min(as_int(usage.get("cacheCreationTokens")), uncached)
    return TokenUsage(
        uncached_input=uncached - cache_write,
        cache_read=cache_read,
        cache_write_5m=cache_write,
        output=as_int(usage.get("outputTokens")),
        reasoning_output=as_int(usage.get("reasoningTokens")),
    )


SOURCE = Source(
    id="grok-build",
    label="Grok Build",
    clients={"grok-build": "Grok Build"},
    default_roots=default_roots,
    files=session_files,
    parse=parse,
    token_data="full",
    display_path="$GROK_HOME/sessions/<url-encoded-cwd>/<session-id>/updates.jsonl",
    capabilities=Capabilities(),
)
