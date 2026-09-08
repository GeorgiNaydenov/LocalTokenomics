from __future__ import annotations

import platform
import re
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path

from ..models import RawScalar, UsageEvent
from ..trace import Capabilities, Span, SpanKind, SpanStatus
from .base import Source, parse_timestamp, project_of, read_json_lines, read_json_records

MODEL_SWITCH_RE = re.compile(
    r"`Model Selection`\s+from\s+.+?\s+to\s+(.+?)\.(?=</USER_SETTINGS_CHANGE>|\s|$)"
)

TIMING_RE = re.compile(r"Created At: (\S+)\s+Completed At: (\S+)")

SUBAGENT_RE = re.compile(r'"conversationId":\s*"([0-9a-fA-F-]{16,})"')

EXIT_CODE_RE = re.compile(r"(?i)exit code:\s*(-?\d+)")

TOOL_TYPES = {
    "VIEW_FILE",
    "CODE_ACTION",
    "RUN_COMMAND",
    "LIST_DIRECTORY",
    "GREP_SEARCH",
    "READ_URL_CONTENT",
}

STATUS_BY_STEP: dict[str, SpanStatus] = {"DONE": "ok", "RUNNING": "running", "ERROR": "error"}

SPAN_TYPES = TOOL_TYPES | {
    "USER_INPUT",
    "PLANNER_RESPONSE",
    "ERROR_MESSAGE",
    "SEARCH_WEB",
    "INVOKE_SUBAGENT",
    "ASK_QUESTION",
}


def default_roots() -> list[Path]:
    return [Path.home() / ".gemini" / "antigravity" / "brain"]


def antigravity_files(root: Path) -> list[Path]:
    chosen: list[Path] = []
    for sub in root.iterdir():
        if not sub.is_dir():
            continue
        full = sub / ".system_generated" / "logs" / "transcript_full.jsonl"
        basic = sub / ".system_generated" / "logs" / "transcript.jsonl"
        if full.is_file():
            chosen.append(full)
        elif basic.is_file():
            chosen.append(basic)
    return sorted(chosen)


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    session_id = path.parent.parent.parent.name
    model: str | None = None
    cwd: str | None = None
    for record in read_json_lines(path, warnings):
        content = record.get("content")
        if record.get("type") == "USER_INPUT" and isinstance(content, str):
            match = MODEL_SWITCH_RE.search(content)
            if match:
                model = match.group(1).strip()
        if record.get("type") != "PLANNER_RESPONSE":
            continue
        cwd = _cwd_from_tool_calls(record.get("tool_calls")) or cwd
        yield UsageEvent(
            source="antigravity",
            client="antigravity",
            provider="google",
            model=model,
            timestamp=parse_timestamp(record.get("created_at"), path),
            session_id=session_id,
            request_id=f"antigravity:{session_id}:{record.get('step_index')}",
            tokens=None,
            working_directory=cwd,
            project=project_of(cwd),
            machine=platform.node(),
            source_file=str(path),
        )


def spans(path: Path, warnings: list[str]) -> Iterator[Span]:
    session_id = path.parent.parent.parent.name
    source_file = str(path)
    active_model: str | None = None
    cwd: str | None = None
    turn_id: str | None = None
    model_call_id: str | None = None
    seq = 0

    def emit(
        span_id: str,
        kind: SpanKind,
        status: SpanStatus,
        *,
        parent_id: str | None = None,
        name: str | None = None,
        model: str | None = None,
        error: str | None = None,
        content_path: str | None = None,
        agent_id: str | None = None,
    ) -> Span:
        nonlocal seq
        seq += 1
        return Span(
            span_id=span_id,
            parent_id=parent_id,
            source="antigravity",
            session_id=session_id,
            turn_id=turn_id,
            agent_id=agent_id,
            seq=seq,
            kind=kind,
            name=name,
            model=model,
            status=status,
            started_at=started_at,
            ended_at=ended_at,
            duration_ms=duration_ms,
            duration_provenance="derived" if duration_ms is not None else "unavailable",
            error=error,
            source_file=source_file,
            record_offset=offset,
            record_length=length,
            content_path=content_path,
            detail=detail,
        )

    for entry in read_json_records(path, warnings):
        offset, length, record = entry
        step_type = record.get("type")
        if step_type not in SPAN_TYPES:
            continue
        content = record.get("content")
        if step_type == "PLANNER_RESPONSE":
            cwd = _cwd_from_tool_calls(record.get("tool_calls")) or cwd
        elif step_type == "USER_INPUT" and isinstance(content, str):
            match = MODEL_SWITCH_RE.search(content)
            if match:
                active_model = match.group(1).strip()
        step_id = f"{session_id}:{record.get('step_index')}"
        status = STATUS_BY_STEP.get(str(record.get("status")), "unknown")
        started_at = parse_timestamp(record.get("created_at"), path)
        ended_at, duration_ms = _timing(content)
        detail = _detail(cwd, record)

        if step_type == "USER_INPUT":
            turn_id = f"{session_id}:t{record.get('step_index')}"
            model_call_id = None
            yield emit(turn_id, "turn", status)
            yield emit(step_id, "user", status, parent_id=turn_id, content_path="content")
        elif step_type == "PLANNER_RESPONSE":
            model_call_id = step_id
            yield emit(step_id, "model_call", status, parent_id=turn_id, model=active_model)
            thinking = record.get("thinking")
            if isinstance(thinking, str) and thinking:
                yield emit(
                    f"{step_id}:thinking",
                    "reasoning",
                    status,
                    parent_id=step_id,
                    content_path="thinking",
                )
            if isinstance(content, str) and content:
                yield emit(
                    f"{step_id}:content",
                    "assistant",
                    status,
                    parent_id=step_id,
                    content_path="content",
                )
        elif step_type == "INVOKE_SUBAGENT":
            child = _child_session(content)
            if child is not None:
                detail["child_session_id"] = child
            yield emit(
                step_id,
                "subagent",
                status,
                parent_id=model_call_id or turn_id,
                name=str(step_type),
                agent_id=child,
                content_path="content",
            )
        elif step_type == "SEARCH_WEB":
            yield emit(
                step_id,
                "retrieval",
                status,
                parent_id=model_call_id or turn_id,
                name=str(step_type),
                content_path="content",
            )
        elif step_type == "ASK_QUESTION":
            yield emit(
                step_id,
                "assistant",
                status,
                parent_id=model_call_id or turn_id,
                name=str(step_type),
                content_path="content",
            )
        elif step_type == "ERROR_MESSAGE":
            yield emit(
                step_id,
                "error",
                "error",
                parent_id=model_call_id or turn_id,
                error=_text(record.get("error")),
                content_path="content",
            )
        else:
            exit_code = _exit_code(record.get("exit_code"), content)
            if exit_code is not None:
                detail["exit_code"] = exit_code
            yield emit(
                step_id,
                "tool_call",
                status,
                parent_id=model_call_id or turn_id,
                name=str(step_type),
                error=_text(record.get("error")),
                content_path="content",
            )


def _detail(cwd: str | None, record: dict) -> dict[str, RawScalar]:
    detail: dict[str, RawScalar] = {"project": project_of(cwd), "working_directory": cwd}
    truncated = record.get("truncated_fields")
    if isinstance(truncated, list) and truncated:
        detail["truncated_fields"] = ",".join(str(field) for field in truncated)
    return detail


def _child_session(content: object) -> str | None:
    if not isinstance(content, str):
        return None
    match = SUBAGENT_RE.search(content)
    return match.group(1) if match else None


def _exit_code(reported: object, content: object) -> int | None:
    if isinstance(reported, int) and not isinstance(reported, bool):
        return reported
    if not isinstance(content, str):
        return None
    match = EXIT_CODE_RE.search(content)
    return int(match.group(1)) if match else None


def _timing(content: object) -> tuple[datetime | None, int | None]:
    if not isinstance(content, str):
        return None, None
    match = TIMING_RE.match(content)
    if match is None:
        return None, None
    created = _isoformat(match.group(1))
    completed = _isoformat(match.group(2))
    if created is None or completed is None:
        return completed, None
    return completed, int((completed - created).total_seconds() * 1000)


def _isoformat(value: str) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def _text(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _cwd_from_tool_calls(tool_calls: object) -> str | None:
    if not isinstance(tool_calls, list):
        return None
    for call in tool_calls:
        if not isinstance(call, dict):
            continue
        args = call.get("args")
        if isinstance(args, dict) and isinstance(args.get("Cwd"), str):
            return args["Cwd"]
    return None


SOURCE = Source(
    id="antigravity",
    label="Antigravity",
    clients={"antigravity": "Antigravity"},
    default_roots=default_roots,
    files=antigravity_files,
    parse=parse,
    token_data="session",
    display_path="~/.gemini/antigravity/brain/*/.system_generated/logs/transcript*.jsonl",
    spans=spans,
    capabilities=Capabilities(
        trace="measured",
        tokens="unavailable",
        cost="unavailable",
        context="unavailable",
        latency="derived",
    ),
)
