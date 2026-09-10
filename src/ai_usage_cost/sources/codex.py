from __future__ import annotations

import re
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from typing import Any

from ..models import Provenance, RawScalar, TokenUsage, UsageEvent
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

RECONCILE_TOLERANCE = 0.01
RECONCILE_MIN_TOKENS = 1000
_TITLE_COMMAND_WRAPPER = re.compile(r"^<command-name>.*</command-name>$")
_SESSION_INDEX_CACHE: dict[Path, dict[str, str]] = {}

_ORIGINATOR_CLIENTS = {
    "Codex Desktop": "codex-desktop",
    "codex_work_desktop": "codex-desktop",
    "codex_cli_rs": "codex-cli",
}

_TIMED_BY_ID_ITEMS = {"Reasoning", "AgentMessage", "UserMessage"}
_TOOL_ITEMS = {
    "CommandExecution",
    "FileChange",
    "DynamicToolCall",
    "Extension",
    "ImageView",
    "FunctionCallOutput",
    "McpToolCall",
}
_AGENT_ITEMS = {"SubAgentActivity", "CollabAgentToolCall"}
_EXIT_CODE = re.compile(r"\s*Exit code:\s*(-?\d+)")


def default_roots() -> list[Path]:
    return [Path.home() / ".codex" / "sessions"]


def _has_token_usage_records(path: Path) -> bool:
    """Whether this file uses the newer per-response `token_usage_record` format.

    A one-shot lookahead pass (its own throwaway warnings sink, so a bad line is not
    reported twice) -- if any such record is present, `parse` prefers those exclusively
    over the older, coarser `token_count` cumulative snapshots for token accounting.
    """
    for record in read_json_lines(path, []):
        payload = record.get("payload")
        payload = payload if isinstance(payload, dict) else record
        kind = payload.get("type") or record.get("type")
        if kind == "token_usage_record":
            return True
    return False


def _codex_root(path: Path) -> Path | None:
    """The `.codex`-equivalent root that holds `session_index.jsonl`, one level above the
    `sessions/` directory a rollout file lives under (`~/.codex/sessions/**/rollout-*.jsonl`
    -> `~/.codex/session_index.jsonl`)."""
    for parent in path.parents:
        if parent.name == "sessions":
            return parent.parent
    return None


def _session_index(path: Path) -> dict[str, str]:
    """Load and cache `session_index.jsonl` once per codex root, not once per rollout file.

    Schema (verified against the real file): one JSON object per line, `{"id": "<thread
    uuid>", "thread_name": "<title>", "updated_at": ...}`. A `thread_name` that is literally
    a `<command-name>...</command-name>` wrapper (the thread's only turn was a bare slash
    command, the one degenerate case found in the real index) is not a usable title -- it is
    dropped here so the caller falls through to the next rung of the title chain.
    """
    root = _codex_root(path)
    if root is None:
        return {}
    cached = _SESSION_INDEX_CACHE.get(root)
    if cached is not None:
        return cached
    index_path = root / "session_index.jsonl"
    index: dict[str, str] = {}
    if index_path.is_file():
        for record in read_json_lines(index_path, []):
            thread_id = record.get("id")
            thread_name = record.get("thread_name")
            if not isinstance(thread_id, str) or not isinstance(thread_name, str):
                continue
            thread_name = thread_name.strip()
            if not thread_name or _TITLE_COMMAND_WRAPPER.match(thread_name):
                continue
            index[thread_id] = thread_name
    _SESSION_INDEX_CACHE[root] = index
    return index


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    model = ""
    session_id = _session_id_from_name(path)
    title = _session_index(path).get(session_id)
    project: str | None = None
    cwd: str | None = None
    client = "codex-cli"
    provider: str | None = None
    repository: str | None = None
    branch: str | None = None
    is_sidechain = False
    forked = False
    summed_reported = 0
    final_total: dict | None = None
    previous_total_snapshot: dict | None = None
    first_token_count_seen = False
    inherited_tokens = 0
    reset_detected = False
    pending: list[dict[str, Any]] = []
    prefer_usage_records = _has_token_usage_records(path)

    for offset, _length, record in read_json_records(path, warnings):
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
            if payload.get("forked_from_id"):
                forked = True
            found_session = _find_session_id(payload)
            if found_session:
                session_id = found_session
                title = _session_index(path).get(session_id) or title

        just_discovered = False
        found_model = _find_model(payload)
        if found_model:
            just_discovered = not model
            model = found_model
        found_cwd = _find_raw_cwd(payload)
        if found_cwd:
            cwd = found_cwd
            project = project_of(found_cwd)

        if just_discovered and pending:
            for kwargs in pending:
                yield UsageEvent(model=model, **kwargs)
            pending = []

        usage: dict | None = None
        if kind == "token_usage_record" and prefer_usage_records:
            payload_usage = payload.get("usage")
            if isinstance(payload_usage, dict):
                usage = payload_usage
        elif kind == "token_count":
            info = payload.get("info")
            info = info if isinstance(info, dict) else payload
            last = info.get("last_token_usage")
            total = info.get("total_token_usage")

            if isinstance(total, dict):
                if not first_token_count_seen:
                    first_token_count_seen = True
                    if isinstance(last, dict):
                        # A forked/resumed thread's first total_token_usage already carries
                        # its parent's history; last_token_usage is only this turn's delta,
                        # so the gap between them is what this file inherited, not earned.
                        inherited_tokens = max(
                            0, _int(total.get("total_tokens")) - _int(last.get("total_tokens"))
                        )
                if previous_total_snapshot is not None and _int(total.get("total_tokens")) < _int(
                    previous_total_snapshot.get("total_tokens")
                ):
                    reset_detected = True
                if total == previous_total_snapshot:
                    # Codex re-emits token_count with an unchanged total_token_usage on
                    # rate-limit-only updates; counting it again double-counts last_token_usage.
                    continue
                previous_total_snapshot = total
                final_total = total
            if not prefer_usage_records and isinstance(last, dict):
                usage = last

        if usage is None:
            continue

        summed_reported += _int(usage.get("total_tokens"))
        tokens = _tokens_from_usage(usage)
        if tokens.total == 0:
            continue

        kwargs = {
            "source": "codex",
            "client": client,
            "provider": provider,
            "timestamp": parse_timestamp(record.get("timestamp") or payload.get("timestamp"), path),
            "session_id": session_id,
            "tokens": tokens,
            "is_sidechain": is_sidechain,
            "project": project,
            "working_directory": cwd,
            "repository": repository,
            "branch": branch,
            "title": title if title else title_of(project, session_id),
            "title_source": "tool" if title else "folder",
            "source_file": str(path),
            "record_offset": offset,
        }
        if model:
            yield UsageEvent(model=model, **kwargs)
        else:
            pending.append(kwargs)

    for kwargs in pending:
        yield UsageEvent(model=model or None, **kwargs)
    _reconcile(
        path,
        summed_reported,
        final_total,
        warnings,
        forked=forked,
        inherited=inherited_tokens,
        reset_detected=reset_detected,
    )


def spans(path: Path, warnings: list[str]) -> Iterator[Span]:
    source_file = str(path)
    session_id = _session_id_from_name(path)
    model = ""
    cwd: str | None = None
    project: str | None = None
    effort: str | None = None
    is_sidechain = False
    capacity: int | None = None

    emitted: list[Span] = []
    pending: list[Span] = []
    open_calls: dict[str, Span] = {}
    timings: dict[str, tuple[int, int]] = {}
    item_timed: set[str] = set()
    turn: Span | None = None
    compaction: Span | None = None
    boundary_at: datetime | None = None
    deltas = 0
    previous_total_snapshot: dict | None = None
    # Mirrors parse()'s exclusivity: when a file has any token_usage_record line, that
    # exact per-response usage replaces token_count's coarser cumulative snapshot for
    # every model_call span in this file, not just for the aggregate cost pipeline.
    prefer_usage_records = _has_token_usage_records(path)

    def build(
        kind: SpanKind,
        span_id: str,
        started_at: datetime,
        offset: int,
        length: int,
        **fields: Any,
    ) -> Span:
        detail: dict[str, RawScalar] = {"project": project, "working_directory": cwd}
        detail.update(fields.pop("detail", {}))
        span = Span(
            span_id=span_id,
            source="codex",
            session_id=session_id,
            turn_id=record_turn or (turn.span_id if turn else None),
            is_sidechain=is_sidechain,
            seq=len(emitted),
            kind=kind,
            started_at=started_at,
            source_file=source_file,
            record_offset=offset,
            record_length=length,
            detail=detail,
            **fields,
        )
        emitted.append(span)
        return span

    def apply_timing(span: Span, payload: dict) -> None:
        bounds = _item_bounds(payload)
        if bounds is not None:
            _set_bounds(span, bounds, item_timed)

    def flush(ended_at: datetime) -> None:
        for span in pending:
            if span.parent_id is None and turn is not None:
                span.parent_id = turn.span_id
        pending.clear()
        for call in open_calls.values():
            if call.ended_at is None:
                call.ended_at = ended_at
        open_calls.clear()

    for offset, length, record in read_json_records(path, warnings):
        raw_payload = record.get("payload")
        payload = raw_payload if isinstance(raw_payload, dict) else record
        prefix = "payload." if payload is raw_payload else ""
        kind = payload.get("type") or record.get("type")
        at = parse_timestamp(record.get("timestamp") or payload.get("timestamp"), path)
        record_turn = _text(payload.get("turn_id")) or _text(
            _nested(payload, "internal_chat_message_metadata_passthrough", "turn_id")
        )

        if record.get("type") == "session_meta" or kind == "session_meta":
            found = _find_session_id(payload)
            if found:
                session_id = found
            if isinstance(payload.get("source"), dict) and "subagent" in payload["source"]:
                is_sidechain = True

        found_model = _find_model(payload)
        if found_model:
            model = found_model
        found_cwd = _find_raw_cwd(payload)
        if found_cwd:
            cwd = found_cwd
            project = project_of(found_cwd)
        if isinstance(payload.get("effort"), str):
            effort = payload["effort"]
            if turn is not None:
                turn.detail["effort"] = effort

        if kind == "task_started":
            if turn is not None:
                flush(at)
                turn.ended_at = at
            capacity = _int(payload.get("model_context_window")) or capacity
            turn = None
            turn_id = _text(payload.get("turn_id")) or f"{session_id}:turn:{len(emitted)}"
            turn = build(
                "turn",
                turn_id,
                at,
                offset,
                length,
                status="running",
                model=model or None,
                context_capacity=capacity or None,
                capacity_provenance="measured" if capacity else "unavailable",
                detail={"effort": effort},
            )
            boundary_at = at
            continue

        if kind in ("task_complete", "turn_aborted"):
            flush(at)
            if turn is not None:
                turn.ended_at = at
                turn.status = "aborted" if kind == "turn_aborted" else "ok"
                duration = _int(payload.get("duration_ms"))
                if duration:
                    turn.duration_ms = duration
                    turn.duration_provenance = "measured"
                ttft = _int(payload.get("time_to_first_token_ms"))
                if ttft:
                    turn.ttft_ms = ttft
                if kind == "turn_aborted":
                    turn.name = _text(payload.get("reason"))
                    turn.detail["reason"] = _text(payload.get("reason"))
            turn = None
            compaction = None
            boundary_at = None
            continue

        if kind == "item_completed":
            item = payload.get("item")
            if not isinstance(item, dict):
                continue
            item_type = _text(item.get("type"))
            item_id = _text(item.get("id"))
            if item_type in _TIMED_BY_ID_ITEMS:
                existing = _by_id(emitted, item_id)
                if existing is not None:
                    apply_timing(existing, payload)
                else:
                    bounds = _item_bounds(payload)
                    if bounds is not None and item_id:
                        timings[item_id] = bounds
                continue
            if item_type in _AGENT_ITEMS:
                target = open_calls.get(item_id)
                if target is None:
                    target = build(
                        "subagent",
                        item_id or f"{session_id}:agent:{len(emitted)}",
                        at,
                        offset,
                        length,
                        name=item_type,
                    )
                    pending.append(target)
                else:
                    target.kind = "subagent"
                apply_timing(target, payload)
                target.agent_id = _text(item.get("agent_thread_id")) or target.agent_id
                target.status, exit_code = _item_status(item)
                if exit_code is not None:
                    target.detail["exit_code"] = exit_code
                target.detail["item_id"] = item_id
                continue
            if item_type == "ContextCompaction":
                if compaction is not None:
                    apply_timing(compaction, payload)
                continue
            if item_type in _TOOL_ITEMS:
                target = open_calls.get(item_id) or _oldest_untimed(open_calls, item_timed)
                if target is None:
                    continue
                apply_timing(target, payload)
                target.status, exit_code = _item_status(item)
                if exit_code is not None:
                    target.detail["exit_code"] = exit_code
                target.detail["item_id"] = item_id
                if item_type == "Extension":
                    target.kind = "retrieval"
            continue

        if kind == "mcp_tool_call_end":
            call = open_calls.get(_text(payload.get("call_id")))
            if call is not None:
                spent = payload.get("duration")
                if isinstance(spent, dict):
                    call.duration_ms = (
                        _int(spent.get("secs")) * 1000 + _int(spent.get("nanos")) // 1_000_000
                    )
                    call.duration_provenance = "measured"
                call.ended_at = at
                result = payload.get("result")
                ok = result.get("Ok") if isinstance(result, dict) else None
                failed = isinstance(ok, dict) and ok.get("isError") is True
                call.status = "error" if failed else "ok"
            continue

        if kind == "token_usage_record" and prefer_usage_records:
            usage_payload = payload.get("usage")
            if not isinstance(usage_payload, dict):
                continue
            tokens = _tokens_from_usage(usage_payload)
            if tokens.total == 0:
                continue
            deltas += 1
            started, ended, elapsed, provenance = _call_bounds(pending, item_timed, boundary_at, at)
            call_span = build(
                "model_call",
                f"{session_id}:mc:{deltas}",
                started,
                offset,
                length,
                parent_id=turn.span_id if turn else None,
                model=model or None,
                status="ok",
                ended_at=ended,
                duration_ms=elapsed,
                duration_provenance=provenance,
                tokens=tokens,
                tokens_provenance="measured",
                context_capacity=capacity or None,
                capacity_provenance="measured" if capacity else "unavailable",
            )
            for span in pending:
                if span.parent_id is None:
                    span.parent_id = call_span.span_id
            pending.clear()
            boundary_at = at
            continue

        if kind == "token_count":
            info = payload.get("info")
            if not isinstance(info, dict):
                continue
            # token_usage_record carries no context-window figure, so keep drawing capacity
            # from token_count's info even in a file where token_usage_record wins on tokens.
            capacity = _int(info.get("model_context_window")) or capacity
            if prefer_usage_records:
                continue
            total = info.get("total_token_usage")
            if isinstance(total, dict):
                if total == previous_total_snapshot:
                    # Same duplicate-emission case parse() skips: an unchanged cumulative
                    # snapshot means this is a re-emitted token_count, not a new API call.
                    continue
                previous_total_snapshot = total
            last = info.get("last_token_usage")
            if not isinstance(last, dict):
                continue
            tokens = _tokens_from_usage(last)
            if tokens.total == 0:
                continue
            deltas += 1
            started, ended, elapsed, provenance = _call_bounds(pending, item_timed, boundary_at, at)
            call_span = build(
                "model_call",
                f"{session_id}:mc:{deltas}",
                started,
                offset,
                length,
                parent_id=turn.span_id if turn else None,
                model=model or None,
                status="ok",
                ended_at=ended,
                duration_ms=elapsed,
                duration_provenance=provenance,
                tokens=tokens,
                tokens_provenance="measured",
                context_capacity=capacity or None,
                capacity_provenance="measured" if capacity else "unavailable",
            )
            for span in pending:
                if span.parent_id is None:
                    span.parent_id = call_span.span_id
            pending.clear()
            boundary_at = at
            continue

        if kind == "compacted":
            history = payload.get("replacement_history")
            compaction = build(
                "compaction",
                f"{session_id}:cmp:{len(emitted)}",
                at,
                offset,
                length,
                parent_id=turn.span_id if turn else None,
                name="compacted",
                status="ok",
                content_path=prefix + "replacement_history",
                detail={
                    "replacement_count": len(history) if isinstance(history, list) else 0,
                    "window_number": _int(payload.get("window_number")),
                },
            )
            continue

        if record.get("type") == "event_msg" and isinstance(kind, str) and "error" in kind:
            build(
                "error",
                f"{session_id}:err:{len(emitted)}",
                at,
                offset,
                length,
                parent_id=turn.span_id if turn else None,
                name=kind,
                status="error",
                error=_text(payload.get("message"))[:500] or None,
            )
            continue

        if record.get("type") != "response_item":
            continue

        if kind == "message":
            role = _text(payload.get("role"))
            if role == "user":
                build(
                    "user",
                    _text(payload.get("id")) or f"{session_id}:um:{len(emitted)}",
                    at,
                    offset,
                    length,
                    parent_id=turn.span_id if turn else None,
                    status="ok",
                    content_path=prefix + "content",
                )
            elif role == "assistant":
                span = build(
                    "assistant",
                    _text(payload.get("id")) or f"{session_id}:am:{len(emitted)}",
                    at,
                    offset,
                    length,
                    status="ok",
                    model=model or None,
                    content_path=prefix + "content",
                )
                _take_timing(span, timings, item_timed)
                pending.append(span)
            continue

        if kind == "reasoning":
            span = build(
                "reasoning",
                _text(payload.get("id")) or f"{session_id}:rs:{len(emitted)}",
                at,
                offset,
                length,
                status="ok",
                model=model or None,
                content_path=prefix + "summary",
            )
            _take_timing(span, timings, item_timed)
            pending.append(span)
            continue

        if kind in ("function_call", "custom_tool_call"):
            call_id = _text(payload.get("call_id")) or f"{session_id}:call:{len(emitted)}"
            span = build(
                "tool_call",
                call_id,
                at,
                offset,
                length,
                name=_text(payload.get("name")) or None,
                status="running",
                content_path=prefix + ("arguments" if kind == "function_call" else "input"),
            )
            open_calls[call_id] = span
            pending.append(span)
            continue

        if kind == "web_search_call":
            build(
                "retrieval",
                f"{session_id}:ws:{len(emitted)}",
                at,
                offset,
                length,
                parent_id=turn.span_id if turn else None,
                name="web_search",
                status="ok",
                content_path=prefix + "action",
            )
            continue

        if kind in ("function_call_output", "custom_tool_call_output"):
            call_id = _text(payload.get("call_id"))
            call = open_calls.pop(call_id, None)
            text = _output_text(payload.get("output"))
            exit_code = _leading_exit_code(text)
            status: SpanStatus = "ok" if exit_code in (None, 0) else "error"
            result = build(
                "tool_result",
                f"{call_id or len(emitted)}:out",
                at,
                offset,
                length,
                parent_id=call.span_id if call else (turn.span_id if turn else None),
                name=call.name if call else None,
                status=status,
                content_path=prefix + "output",
                detail={"exit_code": exit_code},
            )
            pending.append(result)
            if call is not None:
                call.ended_at = at
                if call.span_id not in item_timed:
                    call.duration_ms = _elapsed_ms(call.started_at, at)
                    call.duration_provenance = "derived"
                if call.status == "running":
                    call.status = status
            continue

    flush(emitted[-1].started_at if emitted else parse_timestamp(None, path))

    _scope_to_file(emitted, path)
    yield from emitted


def _scope_to_file(emitted: list[Span], path: Path) -> None:
    prefix = f"{path.stem}:"
    for span in emitted:
        span.span_id = prefix + span.span_id
        if span.parent_id is not None:
            span.parent_id = prefix + span.parent_id
        if span.turn_id is not None:
            span.turn_id = prefix + span.turn_id


def _by_id(emitted: list[Span], span_id: str) -> Span | None:
    if not span_id:
        return None
    for span in reversed(emitted):
        if span.span_id == span_id:
            return span
    return None


def _take_timing(span: Span, timings: dict[str, tuple[int, int]], item_timed: set[str]) -> None:
    bounds = timings.pop(span.span_id, None)
    if bounds is not None:
        _set_bounds(span, bounds, item_timed)


def _item_bounds(payload: dict) -> tuple[int, int] | None:
    started = payload.get("started_at_ms")
    completed = payload.get("completed_at_ms")
    if isinstance(started, int) and isinstance(completed, int):
        return started, completed
    return None


def _set_bounds(span: Span, bounds: tuple[int, int], item_timed: set[str]) -> None:
    started, completed = bounds
    span.started_at = parse_timestamp(started)
    span.ended_at = parse_timestamp(completed)
    span.duration_ms = max(0, completed - started)
    span.duration_provenance = "measured"
    item_timed.add(span.span_id)


def _oldest_untimed(open_calls: dict[str, Span], item_timed: set[str]) -> Span | None:
    for call in open_calls.values():
        if call.span_id not in item_timed:
            return call
    return None


def _item_status(item: dict) -> tuple[SpanStatus, int | None]:
    raw = item.get("exit_code")
    if isinstance(raw, int) and not isinstance(raw, bool):
        return ("ok" if raw == 0 else "error"), raw
    result = item.get("result")
    if isinstance(result, dict) and result.get("isError") is True:
        return "error", None
    if item.get("success") is False:
        return "error", None
    status = _text(item.get("status"))
    if status in ("failed", "error"):
        return "error", None
    if status in ("in_progress", "running"):
        return "running", None
    return "ok", None


def _call_bounds(
    pending: list[Span], item_timed: set[str], boundary_at: datetime | None, at: datetime
) -> tuple[datetime, datetime | None, int | None, Provenance]:
    timed = [
        span
        for span in pending
        if span.kind in ("reasoning", "assistant")
        and span.span_id in item_timed
        and span.ended_at is not None
    ]
    if timed:
        started = min(span.started_at for span in timed)
        ended = max(span.ended_at for span in timed if span.ended_at is not None)
        return started, ended, _elapsed_ms(started, ended), "measured"
    started = boundary_at or at
    if started > at:
        return started, at, None, "unavailable"
    return started, at, _elapsed_ms(started, at), "derived"


def _elapsed_ms(started: datetime, ended: datetime) -> int:
    return max(0, int((ended - started).total_seconds() * 1000))


def _output_text(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts = [
            block["text"]
            for block in value
            if isinstance(block, dict) and isinstance(block.get("text"), str)
        ]
        return "\n".join(parts)
    return ""


def _leading_exit_code(text: str) -> int | None:
    match = _EXIT_CODE.match(text)
    return int(match.group(1)) if match else None


def _text(value: object) -> str:
    return value if isinstance(value, str) else ""


def _client_of(originator: object) -> str:
    if isinstance(originator, str) and originator:
        mapped = _ORIGINATOR_CLIENTS.get(originator)
        if mapped:
            return mapped
        return re.sub(r"[^a-z0-9]+", "-", originator.lower()).strip("-") or "codex-cli"
    return "codex-cli"


def _reconcile(
    path: Path,
    summed_reported: int,
    final_total: dict | None,
    warnings: list[str],
    *,
    forked: bool = False,
    inherited: int = 0,
    reset_detected: bool = False,
) -> None:
    if reset_detected:
        # The file's own cumulative counter went backwards partway through (Codex resets it
        # on some sessions); the last total_token_usage is no longer a valid whole-file
        # baseline, so comparing the summed turns against it would just be noise.
        warnings.append(
            f"codex: {path.name}: counter reset -- this session's cumulative token count "
            "decreased partway through the file, so its final total cannot be used as a "
            "reconciliation baseline"
        )
        return
    if final_total is None:
        return
    reported = _int(final_total.get("total_tokens"))
    if reported <= 0:
        return
    baseline = reported
    if forked and inherited > 0:
        baseline = max(0, reported - inherited)
    if baseline <= 0:
        return
    drift = abs(summed_reported - baseline)
    if drift <= RECONCILE_MIN_TOKENS or drift / baseline <= RECONCILE_TOLERANCE:
        return
    if forked:
        warnings.append(
            f"codex: {path.name}: forked thread -- summed turns {summed_reported:,} vs "
            f"{baseline:,} after excluding {inherited:,} tokens inherited from the parent "
            f"thread ({drift / baseline:.1%} still unexplained)"
        )
    else:
        warnings.append(
            f"codex: {path.name}: summed turns {summed_reported:,} vs session total "
            f"{baseline:,} ({drift / baseline:.1%} drift)"
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
    token_data="full",
    display_path="~/.codex/sessions/**/rollout-*.jsonl",
    spans=spans,
    capabilities=Capabilities(
        trace="measured",
        tokens="measured",
        cost="derived",
        context="measured",
        latency="measured",
    ),
)
