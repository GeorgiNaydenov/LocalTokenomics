from __future__ import annotations

import json
from collections.abc import Iterator
from datetime import datetime, timedelta
from pathlib import Path

from ..models import RawScalar, TokenUsage, UsageEvent
from ..trace import Capabilities, Span, SpanKind, SpanStatus
from .base import (
    Source,
    jsonl_files,
    parse_timestamp,
    project_of,
    read_json_lines,
    read_json_records,
    title_of,
)

SYNTHETIC_MODELS = {"<synthetic>", "synthetic"}
RETRIEVAL_TOOLS = {"WebSearch", "WebFetch"}
SUBAGENT_TOOLS = {"Agent", "Task"}
TRACED_TYPES = {"user", "assistant", "system"}
INTERRUPTED_TEXT = "[Request interrupted by user]"
LONG_CONTEXT_SUFFIX = "[1m]"
LONG_CONTEXT_CAPACITY = 1_000_000
MAX_ERROR_CHARS = 500
AGENT_META_FIELDS = (
    ("agentType", "agent_type"),
    ("spawnDepth", "spawn_depth"),
    ("toolUseId", "tool_use_id"),
)


def default_roots() -> list[Path]:
    home = Path.home()
    return [home / ".claude" / "projects", home / ".config" / "claude" / "projects"]


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    session_id = path.stem
    # `custom-title` records carry the title shown in the `claude --resume` picker. The
    # record is re-emitted (e.g. on every resume) with an identical value once set, or a
    # newer value on a manual rename -- latest wins during this same linear scan, the same
    # pattern already used for the sessionId/cwd overrides below.
    title: str | None = None
    for record in read_json_lines(path, warnings):
        if record.get("type") == "custom-title":
            candidate = record.get("customTitle")
            if isinstance(candidate, str) and candidate.strip():
                title = candidate.strip()
            continue
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
        event_session_id = str(record.get("sessionId") or session_id)
        project = _project_name(record, path)

        yield UsageEvent(
            source="claude-code",
            client="claude-code",
            model=model,
            timestamp=parse_timestamp(record.get("timestamp"), path),
            session_id=event_session_id,
            request_id=str(message_id or request_id) if (message_id or request_id) else None,
            tokens=tokens,
            is_sidechain=bool(record.get("isSidechain")),
            tier=_tier(usage),
            project=project,
            working_directory=cwd if isinstance(cwd, str) else None,
            branch=record.get("gitBranch") if isinstance(record.get("gitBranch"), str) else None,
            title=title if title else title_of(project, event_session_id),
            title_source="tool" if title else "folder",
            source_file=str(path),
        )


def spans(path: Path, warnings: list[str]) -> Iterator[Span]:
    file_agent_id = _agent_file_id(path)
    emitted: list[Span] = []
    ts_by_uuid: dict[str, datetime] = {}
    open_tools: dict[str, Span] = {}
    model_calls: dict[str, Span] = {}
    turn: Span | None = None
    turn_prompt: str | None = None
    compaction: Span | None = None
    seq = 0

    def add(span: Span) -> Span:
        nonlocal seq
        span.seq = seq
        seq += 1
        emitted.append(span)
        return span

    for offset, length, record in read_json_records(path, warnings):
        record_type = record.get("type")
        if record_type not in TRACED_TYPES or record.get("isMeta"):
            continue

        location = (str(path), offset, length)
        timestamp = parse_timestamp(record.get("timestamp"), path)
        uuid = _text(record.get("uuid")) or f"{path.stem}:{offset}"
        ts_by_uuid[uuid] = timestamp
        session_id = _text(record.get("sessionId")) or path.stem
        agent_id = _text(record.get("agentId")) or file_agent_id
        where = _place(record, path)
        parent_turn = turn.span_id if turn is not None else None

        if record_type == "system":
            subtype = _text(record.get("subtype"))
            if subtype == "api_error":
                add(
                    _new_span(
                        record,
                        location,
                        span_id=uuid,
                        kind="error",
                        started_at=timestamp,
                        session_id=session_id,
                        agent_id=agent_id,
                        parent_id=parent_turn,
                        turn_id=parent_turn,
                        name="api_error",
                        status="error",
                        error=_error_text(record.get("error")),
                        retry_attempt=_int_or_none(record.get("retryAttempt")),
                        detail={
                            **where,
                            "retry_in_ms": _int_or_none(record.get("retryInMs")),
                            "max_retries": _int_or_none(record.get("maxRetries")),
                        },
                    )
                )
            elif subtype == "compact_boundary":
                metadata = record.get("compactMetadata")
                metadata = metadata if isinstance(metadata, dict) else {}
                compaction = add(
                    _new_span(
                        record,
                        location,
                        span_id=uuid,
                        kind="compaction",
                        started_at=timestamp,
                        session_id=session_id,
                        agent_id=agent_id,
                        parent_id=parent_turn,
                        turn_id=parent_turn,
                        name=_text(metadata.get("trigger")),
                        status="ok",
                        detail={**where, "pre_tokens": _int_or_none(metadata.get("preTokens"))},
                    )
                )
                measured = _int_or_none(metadata.get("durationMs"))
                if measured is not None:
                    compaction.duration_ms = measured
                    compaction.duration_provenance = "measured"
                    compaction.ended_at = _shift(timestamp, measured)
            elif subtype == "model_refusal_fallback":
                add(
                    _new_span(
                        record,
                        location,
                        span_id=uuid,
                        kind="error",
                        started_at=timestamp,
                        session_id=session_id,
                        agent_id=agent_id,
                        parent_id=parent_turn,
                        turn_id=parent_turn,
                        name=subtype,
                        status="error",
                        error=_error_text(record.get("content")),
                        detail=dict(where),
                    )
                )
            continue

        message = record.get("message")
        content = message.get("content") if isinstance(message, dict) else None

        if record_type == "user":
            results = [
                (index, block)
                for index, block in _indexed_blocks(content)
                if block.get("type") == "tool_result"
            ]
            if results:
                outcome = record.get("toolUseResult")
                for index, block in results:
                    tool_use_id = _text(block.get("tool_use_id"))
                    call = open_tools.pop(tool_use_id, None) if tool_use_id else None
                    status = _result_status(outcome, block)
                    add(
                        _new_span(
                            record,
                            location,
                            span_id=_block_id(uuid, index),
                            kind="tool_result",
                            started_at=timestamp,
                            session_id=session_id,
                            agent_id=agent_id,
                            parent_id=call.span_id if call is not None else parent_turn,
                            turn_id=parent_turn,
                            name=call.name if call is not None else None,
                            status=status,
                            content_path=_result_content_path(outcome, index),
                            detail={**where, "tool_use_id": tool_use_id},
                        )
                    )
                    if call is not None:
                        _close_call(call, timestamp, status, outcome)
                continue

            if record.get("isCompactSummary"):
                add(
                    _new_span(
                        record,
                        location,
                        span_id=uuid,
                        kind="user",
                        started_at=timestamp,
                        session_id=session_id,
                        agent_id=agent_id,
                        parent_id=compaction.span_id if compaction is not None else parent_turn,
                        turn_id=parent_turn,
                        name="compact_summary",
                        status="ok",
                        content_path=_text_content_path(content),
                        detail=dict(where),
                    )
                )
                continue

            if _user_text(content) == INTERRUPTED_TEXT:
                add(
                    _new_span(
                        record,
                        location,
                        span_id=uuid,
                        kind="user",
                        started_at=timestamp,
                        session_id=session_id,
                        agent_id=agent_id,
                        parent_id=parent_turn,
                        turn_id=parent_turn,
                        name="interrupted",
                        status="interrupted",
                        content_path=_text_content_path(content),
                        detail=dict(where),
                    )
                )
                if turn is not None:
                    turn.status = "aborted"
                continue

            prompt_id = _text(record.get("promptId"))
            if turn is None or prompt_id is None or prompt_id != turn_prompt:
                turn = add(
                    _new_span(
                        record,
                        location,
                        span_id=prompt_id or uuid,
                        kind="turn",
                        started_at=timestamp,
                        session_id=session_id,
                        agent_id=agent_id,
                        status="ok",
                        detail={
                            **where,
                            "version": _text(record.get("version")),
                            "permission_mode": _text(record.get("permissionMode")),
                        },
                    )
                )
                turn.turn_id = turn.span_id
                turn_prompt = prompt_id
            add(
                _new_span(
                    record,
                    location,
                    span_id=uuid,
                    kind="user",
                    started_at=timestamp,
                    session_id=session_id,
                    agent_id=agent_id,
                    parent_id=turn.span_id,
                    turn_id=turn.span_id,
                    status="ok",
                    content_path=_text_content_path(content),
                    detail=dict(where),
                )
            )
            continue

        if not isinstance(message, dict):
            continue
        model = _text(message.get("model"))
        if model is None or model in SYNTHETIC_MODELS:
            continue

        message_id = _text(message.get("id")) or uuid
        call = model_calls.get(message_id)
        usage = message.get("usage")
        if call is None:
            call = add(
                _new_span(
                    record,
                    location,
                    span_id=message_id,
                    kind="model_call",
                    started_at=ts_by_uuid.get(_text(record.get("parentUuid")) or "", timestamp),
                    session_id=session_id,
                    agent_id=agent_id,
                    parent_id=parent_turn,
                    turn_id=parent_turn,
                    model=model,
                    status="ok",
                    retry_attempt=_retry_attempt(usage),
                    detail={
                        **where,
                        "tier": _tier(usage) if isinstance(usage, dict) else None,
                        "stop_reason": _text(message.get("stop_reason")),
                        "request_id": _text(record.get("requestId")),
                    },
                )
            )
            if isinstance(usage, dict):
                call.tokens = _tokens_from_usage(usage)
                call.tokens_provenance = "measured"
            if model.endswith(LONG_CONTEXT_SUFFIX):
                call.context_capacity = LONG_CONTEXT_CAPACITY
                call.capacity_provenance = "inferred"
            model_calls[message_id] = call
        elif isinstance(usage, dict) and call.tokens is not None:
            # Several assistant records can share one message.id while streaming; input
            # fields never vary across them but output/reasoning grow, so a later record
            # carrying a larger count is the final, billed value -- refresh in place rather
            # than leaving the first (possibly partial) record's tokens on the span.
            candidate = _tokens_from_usage(usage)
            if candidate.output > call.tokens.output or (
                candidate.reasoning_output > call.tokens.reasoning_output
            ):
                call.tokens = TokenUsage(
                    uncached_input=call.tokens.uncached_input,
                    cache_read=call.tokens.cache_read,
                    cache_write_5m=call.tokens.cache_write_5m,
                    cache_write_1h=call.tokens.cache_write_1h,
                    output=max(call.tokens.output, candidate.output),
                    reasoning_output=max(call.tokens.reasoning_output, candidate.reasoning_output),
                )
        call.ended_at = timestamp

        for index, block in _indexed_blocks(content):
            block_type = block.get("type")
            kind: SpanKind
            if block_type == "thinking":
                kind, name, field = "reasoning", None, "thinking"
            elif block_type == "text":
                kind, name, field = "assistant", None, "text"
            elif block_type == "tool_use":
                name = _text(block.get("name"))
                kind, field = _tool_kind(name), "input"
            else:
                continue
            block_span = add(
                _new_span(
                    record,
                    location,
                    span_id=_block_id(uuid, index),
                    kind=kind,
                    started_at=timestamp,
                    session_id=session_id,
                    agent_id=agent_id,
                    parent_id=message_id,
                    turn_id=call.turn_id,
                    name=name,
                    model=model,
                    status="running" if block_type == "tool_use" else "ok",
                    content_path=f"message.content.{index}.{field}",
                    detail=dict(where),
                )
            )
            tool_use_id = _text(block.get("id")) if block_type == "tool_use" else None
            if tool_use_id:
                block_span.detail["tool_use_id"] = tool_use_id
                open_tools[tool_use_id] = block_span

    _close_turns(emitted)
    if file_agent_id:
        _apply_agent_meta(path, emitted)
    yield from emitted


def _new_span(
    record: dict,
    location: tuple[str, int, int],
    *,
    span_id: str,
    kind: SpanKind,
    started_at: datetime,
    session_id: str,
    agent_id: str | None = None,
    parent_id: str | None = None,
    turn_id: str | None = None,
    name: str | None = None,
    model: str | None = None,
    status: SpanStatus = "unknown",
    error: str | None = None,
    retry_attempt: int | None = None,
    content_path: str | None = None,
    detail: dict[str, RawScalar] | None = None,
) -> Span:
    return Span(
        span_id=span_id,
        parent_id=parent_id,
        record_parent=_text(record.get("parentUuid")),
        source="claude-code",
        session_id=session_id,
        turn_id=turn_id,
        agent_id=agent_id,
        is_sidechain=bool(record.get("isSidechain")),
        seq=0,
        kind=kind,
        name=name,
        model=model,
        status=status,
        started_at=started_at,
        error=error,
        retry_attempt=retry_attempt,
        source_file=location[0],
        record_offset=location[1],
        record_length=location[2],
        content_path=content_path,
        detail=detail or {},
    )


def _close_call(call: Span, ended_at: datetime, status: SpanStatus, outcome: object) -> None:
    call.ended_at = ended_at
    call.status = status
    call.duration_ms = _elapsed_ms(call.started_at, ended_at)
    call.duration_provenance = "derived"
    if call.kind != "subagent" or not isinstance(outcome, dict):
        return
    agent_id = _text(outcome.get("agentId"))
    if agent_id:
        call.agent_id = agent_id
    measured = _int_or_none(outcome.get("totalDurationMs"))
    if measured is not None:
        call.duration_ms = measured
        call.duration_provenance = "measured"
        call.ended_at = _shift(call.started_at, measured)
    call.detail["total_tokens"] = _int_or_none(outcome.get("totalTokens"))
    call.detail["tool_use_count"] = _int_or_none(outcome.get("totalToolUseCount"))


def _close_turns(emitted: list[Span]) -> None:
    last_seen: dict[str, datetime] = {}
    for span in emitted:
        if span.kind == "turn" or not span.turn_id:
            continue
        end = span.ended_at or span.started_at
        current = last_seen.get(span.turn_id)
        if current is None or end > current:
            last_seen[span.turn_id] = end
    for span in emitted:
        if span.kind == "turn":
            _derive_duration(span, last_seen.get(span.span_id))
        elif span.kind == "model_call":
            _derive_duration(span, span.ended_at)


def _derive_duration(span: Span, ended_at: datetime | None) -> None:
    if ended_at is None or ended_at <= span.started_at:
        return
    span.ended_at = ended_at
    span.duration_ms = _elapsed_ms(span.started_at, ended_at)
    span.duration_provenance = "derived"


def _agent_file_id(path: Path) -> str | None:
    if path.parent.name != "subagents" or not path.stem.startswith("agent-"):
        return None
    return path.stem[len("agent-") :] or None


def _apply_agent_meta(path: Path, emitted: list[Span]) -> None:
    root = next((span for span in emitted if span.parent_id is None), None)
    if root is None:
        return
    try:
        raw = json.loads(path.with_name(f"{path.stem}.meta.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return
    if not isinstance(raw, dict):
        return
    for key, field in AGENT_META_FIELDS:
        value = raw.get(key)
        if isinstance(value, str | int | float | bool):
            root.detail[field] = value


def _place(record: dict, path: Path) -> dict[str, RawScalar]:
    cwd = record.get("cwd")
    return {
        "project": _project_name(record, path),
        "working_directory": cwd if isinstance(cwd, str) else None,
    }


def _tool_kind(name: str | None) -> SpanKind:
    if name in RETRIEVAL_TOOLS:
        return "retrieval"
    if name in SUBAGENT_TOOLS:
        return "subagent"
    return "tool_call"


def _result_status(outcome: object, block: dict) -> SpanStatus:
    if isinstance(outcome, dict):
        if outcome.get("interrupted"):
            return "interrupted"
        if outcome.get("is_error"):
            return "error"
    if block.get("is_error"):
        return "error"
    return "ok"


def _result_content_path(outcome: object, index: int) -> str:
    if isinstance(outcome, dict) and isinstance(outcome.get("stdout"), str):
        return "toolUseResult.stdout"
    return f"message.content.{index}.content"


def _text_content_path(content: object) -> str | None:
    if isinstance(content, str):
        return "message.content"
    for index, block in _indexed_blocks(content):
        if block.get("type") == "text":
            return f"message.content.{index}.text"
    return None


def _user_text(content: object) -> str | None:
    if isinstance(content, str):
        return content.strip()
    for _, block in _indexed_blocks(content):
        text = _text(block.get("text")) if block.get("type") == "text" else None
        if text is not None:
            return text.strip()
    return None


def _indexed_blocks(content: object) -> list[tuple[int, dict]]:
    if not isinstance(content, list):
        return []
    return [(index, block) for index, block in enumerate(content) if isinstance(block, dict)]


def _block_id(uuid: str, index: int) -> str:
    return uuid if index == 0 else f"{uuid}:{index}"


def _retry_attempt(usage: object) -> int | None:
    if not isinstance(usage, dict):
        return None
    iterations = usage.get("iterations")
    return len(iterations) - 1 if isinstance(iterations, list) and iterations else None


def _error_text(value: object) -> str | None:
    if isinstance(value, dict):
        value = value.get("message") or value.get("formatted")
    text = _text(value)
    return text[:MAX_ERROR_CHARS] if text is not None else None


def _elapsed_ms(start: datetime, end: datetime) -> int:
    return max(int((end - start).total_seconds() * 1000), 0)


def _shift(start: datetime, milliseconds: int) -> datetime:
    return start + timedelta(milliseconds=milliseconds)


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


def _int_or_none(value: object) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _text(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


SOURCE = Source(
    id="claude-code",
    label="Claude Code",
    clients={"claude-code": "Claude Code"},
    default_roots=default_roots,
    files=jsonl_files,
    parse=parse,
    token_data="full",
    display_path="~/.claude/projects/*/*.jsonl",
    spans=spans,
    capabilities=Capabilities(
        trace="measured",
        tokens="measured",
        cost="derived",
        context="estimated",
        latency="derived",
    ),
)
