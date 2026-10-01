"""Qwen Code (QwenLM/qwen-code, a Gemini CLI fork) session logs.

Layout: ``<base>/projects/<sanitized-cwd>/chats/<sessionId>.jsonl`` with ``<base>`` =
``QWEN_RUNTIME_DIR`` > ``QWEN_HOME`` > ``~/.qwen``. One ``ChatRecord`` per line. Tokens come
from ``type == "assistant"`` records' ``usageMetadata`` only: the ``system``/``ui_telemetry``
records repeat the same numbers and are never counted. Records are deduped by ``uuid``.

Output arithmetic depends on the provider path: Gemini-native records satisfy
``total == prompt + candidates + thoughts`` (thoughts are separate); OpenAI-compatible records
satisfy ``total == prompt + candidates`` (candidates already include reasoning). A record that
reconciles neither way keeps ``candidates`` only (never double counts) and warns.

``contextWindowSize`` is a measured context capacity, surfaced through minimal ``model_call``
spans. Limitation: the pre-``projects/`` era (``~/.qwen/tmp/<hash>/chats/*.json``) is not read.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

from ..models import TokenUsage, UsageEvent
from ..trace import Capabilities, Span
from .base import Source, as_int, parse_timestamp, project_of, read_json_records, title_of

SOURCE_ID = "qwen-code"


def default_roots() -> list[Path]:
    for name in ("QWEN_RUNTIME_DIR", "QWEN_HOME"):
        value = os.environ.get(name, "").strip()
        if value:
            return [Path(value) / "projects"]
    return [Path.home() / ".qwen" / "projects"]


def session_files(root: Path) -> list[Path]:
    found: set[Path] = set()
    for base in (root, root / "projects"):
        if base.is_dir():
            found.update(p for p in base.glob("*/chats/*.jsonl") if p.is_file())
    return sorted(found)


def _count(value: object) -> int:
    return max(0, as_int(value))


def _tokens_of(usage: dict) -> tuple[TokenUsage | None, bool]:
    """Tokens plus whether thoughts were present but the total reconciled neither way."""
    prompt = _count(usage.get("promptTokenCount"))
    cached = min(_count(usage.get("cachedContentTokenCount")), prompt)
    candidates = _count(usage.get("candidatesTokenCount"))
    thoughts = _count(usage.get("thoughtsTokenCount"))
    total = _count(usage.get("totalTokenCount"))
    output = candidates
    mismatch = False
    if thoughts:
        if total == prompt + candidates + thoughts:
            output = candidates + thoughts
        elif total != prompt + candidates:
            mismatch = True
    tokens = TokenUsage(
        uncached_input=prompt - cached,
        cache_read=cached,
        output=output,
        reasoning_output=min(thoughts, output),
    )
    return (tokens if tokens.total > 0 else None), mismatch


def _records(path: Path, warnings: list[str]) -> tuple[list[tuple[int, int, dict]], str | None]:
    """Deduped assistant records with usage (uuid, last wins) plus the last custom title."""
    assistants: dict[str, tuple[int, int, dict]] = {}
    title: str | None = None
    for offset, length, record in read_json_records(path, warnings):
        kind = record.get("type")
        if kind == "assistant" and isinstance(record.get("usageMetadata"), dict):
            key = record.get("uuid")
            key = key if isinstance(key, str) and key else f"@{offset}"
            assistants[key] = (offset, length, record)
        elif kind == "system" and record.get("subtype") == "custom_title":
            payload = record.get("systemPayload")
            custom = payload.get("customTitle") if isinstance(payload, dict) else None
            if isinstance(custom, str) and custom.strip():
                title = custom.strip()
    return list(assistants.values()), title


def _text(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    records, title = _records(path, warnings)
    mismatches = 0
    for offset, _length, record in records:
        tokens, mismatch = _tokens_of(record["usageMetadata"])
        mismatches += mismatch
        if tokens is None:
            continue
        session_id = _text(record.get("sessionId")) or path.stem
        cwd = _text(record.get("cwd"))
        project = project_of(cwd)
        uuid = _text(record.get("uuid"))
        yield UsageEvent(
            source=SOURCE_ID,
            client=SOURCE_ID,
            model=_text(record.get("model")),
            timestamp=parse_timestamp(record.get("timestamp"), path),
            session_id=session_id,
            request_id=f"{SOURCE_ID}:{session_id}:{uuid}" if uuid else None,
            tokens=tokens,
            is_sidechain=record.get("isSidechain") is True,
            project=project,
            working_directory=cwd,
            branch=_text(record.get("gitBranch")),
            title=title if title else title_of(project, session_id),
            title_source="tool" if title else "folder",
            source_file=str(path),
            record_offset=offset,
        )
    if mismatches:
        warnings.append(
            f"{path.name}: {mismatches} records had a total that does not reconcile; "
            "output taken as candidates only"
        )


def spans(path: Path, warnings: list[str]) -> Iterator[Span]:
    # Bad-line warnings were already reported by parse(); do not duplicate them here.
    del warnings
    records, _title = _records(path, [])
    for seq, (offset, length, record) in enumerate(records):
        tokens, _mismatch = _tokens_of(record["usageMetadata"])
        if tokens is None:
            continue
        session_id = _text(record.get("sessionId")) or path.stem
        cwd = _text(record.get("cwd"))
        capacity = as_int(record.get("contextWindowSize"))
        yield Span(
            span_id=f"{session_id}:{_text(record.get('uuid')) or offset}",
            source=SOURCE_ID,
            session_id=session_id,
            is_sidechain=record.get("isSidechain") is True,
            seq=seq,
            kind="model_call",
            model=_text(record.get("model")),
            status="ok",
            started_at=parse_timestamp(record.get("timestamp"), path),
            tokens=tokens,
            tokens_provenance="measured",
            context_capacity=capacity or None,
            capacity_provenance="measured" if capacity else "unavailable",
            source_file=str(path),
            record_offset=offset,
            record_length=length,
            detail={"project": project_of(cwd), "working_directory": cwd},
        )


SOURCE = Source(
    id=SOURCE_ID,
    label="Qwen Code",
    clients={SOURCE_ID: "Qwen Code"},
    default_roots=default_roots,
    files=session_files,
    parse=parse,
    token_data="full",
    display_path="$QWEN_HOME/projects/<sanitized-cwd>/chats/<session-id>.jsonl",
    spans=spans,
    capabilities=Capabilities(tokens="measured", cost="derived", context="measured"),
    experimental=True,
)
