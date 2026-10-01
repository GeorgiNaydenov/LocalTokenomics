"""Muse Code (Meta's terminal coding agent) session logs -- EXPERIMENTAL.

The log format is undocumented and the CLI is closed source. Everything below comes from
third-party parsers (tokscale, codeburn, ccusage, Irrlicht, herdr, relayhistory); no real
log has been checked against this module. Assumptions, all unverified:

* Location: ``$MUSE_DATA_DIR`` (exact directory, one source) else
  ``<$XDG_DATA_HOME or ~/.local/share>/muse/sessions/`` -- the same XDG-style path on Windows
  (``C:\\Users\\<u>\\.local\\share\\muse\\sessions\\``). Files are
  ``YYYY/MM/DD/<session-uuid>/session.jsonl``; subagent children live at
  ``<session-dir>/subagent/<child-uuid>/session.jsonl`` (``is_sidechain=True``).
  ``.msp-view-v1/``, ``model-catalog/`` and lock files are skipped; ``auth.json`` is never read.
* Envelope: ``{payload_type, payload, recorded_at, stream, seq, record}``, optionally wrapped
  in ``{"record": "retained_frame", "children": [{"record_json": "<escaped JSON>"}]}`` (seen
  by one reporter on v1.1.1). Both are accepted; anything else is skipped and counted in one
  warning per file.
* Usage record: ``payload_type == "runtime.session"`` and ``payload.event.kind ==
  "model_completed"``; model ``payload.event.model``; tokens in ``payload.event.usage``
  (``input_tokens``, ``output_tokens``, ``cache_read_tokens``, ``cache_write_tokens``,
  ``cached_tokens`` alias, ``reasoning_tokens``); ``payload.event.duration_ms``.
* ``recorded_at`` is in MICROSECONDS (converted here; ``base.parse_timestamp`` only does s/ms).
* ``input_tokens`` includes cache reads; ``output_tokens`` already includes reasoning.
  Whether ``cache_write_tokens`` is inside ``input_tokens`` is UNVERIFIED -- see
  ``_CACHE_WRITE_INSIDE_INPUT``.
* Double-count traps handled: ``goal_usage_attribution`` records (same numbers as the step)
  are never usage; records whose ``stream.id`` is not this file's own session stream
  (mirrored child runs) are skipped, the child's own file counts them; fork/resume prefix
  replays are deduped on ``usage_id`` and ``(stream.id, seq)`` -- the same key is the
  ``request_id``, so a replay in a second file is also deduped by the store.
* No cost is logged (``reported_cost=None``), no title field is known (folder fallback), and
  the context window is not in the log (``model-catalog/*.json`` ``context_limit`` is
  unverified), so no spans are produced.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path

from ..models import RawScalar, TokenUsage, UsageEvent
from ..trace import Capabilities
from .base import Source, as_int, parse_timestamp, project_of, read_json_lines, title_of

SOURCE_ID = "muse-code"

# Policy: is cache_write_tokens a subset of input_tokens (like cache reads)? Unverified.
# True  -> uncached = input - cache_read - cache_write
# False -> uncached = input - cache_read, cache_write is billed on top
_CACHE_WRITE_INSIDE_INPUT = True

_SKIP_DIRS = frozenset({".msp-view-v1", "model-catalog"})
_MAX_UNWRAP_DEPTH = 8
_NO_PROVIDER = frozenset({"echo"})


def default_roots() -> list[Path]:
    override = os.environ.get("MUSE_DATA_DIR", "").strip()
    if override:
        return [Path(override)]
    xdg = os.environ.get("XDG_DATA_HOME", "").strip()
    base = Path(xdg) if xdg else Path.home() / ".local" / "share"
    return [base / "muse" / "sessions"]


def session_files(root: Path) -> list[Path]:
    return sorted(
        p
        for p in root.rglob("session.jsonl")
        if p.is_file() and not _SKIP_DIRS.intersection(p.relative_to(root).parts)
    )


def _micros_to_timestamp(value: object, path: Path) -> datetime:
    if isinstance(value, int | float) and not isinstance(value, bool):
        # Epoch seconds ~1.8e9, millis ~1.8e12, micros ~1.8e15.
        if value > 100_000_000_000_000:
            value = value / 1_000_000
        elif value > 100_000_000_000:
            value = value / 1000
    return parse_timestamp(value, path)


def _flatten(record: dict, unknown: list[int], depth: int = 0) -> Iterator[dict]:
    """Yield plain envelope records, unwrapping `retained_frame` wrappers recursively."""
    children = record.get("children")
    if record.get("record") == "retained_frame" or (
        isinstance(children, list) and "payload_type" not in record
    ):
        if depth >= _MAX_UNWRAP_DEPTH or not isinstance(children, list):
            unknown[0] += 1
            return
        for child in children:
            if not isinstance(child, dict):
                unknown[0] += 1
                continue
            inner: object = child
            if "record_json" in child:
                try:
                    inner = json.loads(child["record_json"])
                except (TypeError, ValueError):
                    unknown[0] += 1
                    continue
            if not isinstance(inner, dict):
                unknown[0] += 1
                continue
            if "recorded_at" not in inner and "recorded_at" in record:
                inner = {**inner, "recorded_at": record["recorded_at"]}
            yield from _flatten(inner, unknown, depth + 1)
        return
    if isinstance(record.get("payload_type"), str) and isinstance(record.get("payload"), dict):
        yield record
        return
    unknown[0] += 1


def _stream_id(record: dict) -> str | None:
    stream = record.get("stream")
    value = stream.get("id") if isinstance(stream, dict) else stream
    return value if isinstance(value, str) and value else None


def _dict(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def _str(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _nat(value: object) -> int:
    """Token counts are never negative; a bad (negative) log value reads as 0."""
    return max(0, as_int(value))


def _survey(
    path: Path,
) -> tuple[str | None, list[tuple[str | None, str | None, str | None, str | None]]]:
    """First pass, streaming: the file's own stream id and its metadata candidates.

    Own stream = the stream id equal to the directory name when present, else the id on the
    most metadata/`model_completed` records (ties: earliest), so a mirrored child record
    that happens to come first does not win (assumes the parent logs more of its own steps).
    """
    counts: dict[str, int] = {}
    metas: list[tuple[str | None, str | None, str | None, str | None]] = []
    for raw_record in read_json_lines(path, []):
        for record in _flatten(raw_record, [0]):
            payload = record["payload"]
            stream = _stream_id(record)
            if record["payload_type"] == "runtime.session.metadata":
                # The nesting is unverified: look in payload.record, payload.metadata, then payload.
                for body in (_dict(payload.get("record")), _dict(payload.get("metadata")), payload):
                    provider = _str(body.get("provider_id"))
                    cwd = _str(body.get("workspace_root"))
                    if provider is not None or cwd is not None:
                        semver = _str(_dict(body.get("build")).get("semver"))
                        metas.append((stream, provider, cwd, semver))
                        break
            elif (
                record["payload_type"] == "runtime.session"
                and _dict(payload.get("event")).get("kind") == "model_completed"
            ):
                pass
            else:
                continue
            if stream is not None:
                counts[stream] = counts.get(stream, 0) + 1
    own: str | None = None
    if counts:
        own = (
            path.parent.name if path.parent.name in counts else max(counts, key=counts.__getitem__)
        )
    return own, metas


def _tokens(usage: dict, mismatch: list[int]) -> TokenUsage:
    input_tokens = _nat(usage.get("input_tokens"))
    cache_write = _nat(usage.get("cache_write_tokens"))
    explicit, alias = usage.get("cache_read_tokens"), usage.get("cached_tokens")
    if explicit is not None:
        cache_read = _nat(explicit)
        if alias is not None and _nat(alias) != cache_read:
            mismatch[0] += 1
    else:
        cache_read = _nat(alias)
    inside = cache_read + (cache_write if _CACHE_WRITE_INSIDE_INPUT else 0)
    output = _nat(usage.get("output_tokens"))
    return TokenUsage(
        uncached_input=max(0, input_tokens - inside),
        cache_read=cache_read,
        cache_write_5m=cache_write,
        output=output,
        reasoning_output=min(output, _nat(usage.get("reasoning_tokens"))),
    )


def _records(path: Path, warnings: list[str], unknown: list[int]) -> Iterator[dict]:
    for raw_record in read_json_lines(path, warnings):
        yield from _flatten(raw_record, unknown)


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    session_id = path.parent.name or "unknown"
    own, metas = _survey(path)
    provider, cwd, semver = next(
        ((p, c, v) for stream, p, c, v in metas if stream is None or own is None or stream == own),
        (None, None, None),
    )
    if provider in _NO_PROVIDER:
        return
    project = project_of(cwd)
    sidechain = path.parent.parent.name == "subagent"

    seen: set[str] = set()
    mismatch = [0]
    ordinal = 0
    unknown = [0]
    for record in _records(path, warnings, unknown):
        event = _dict(record["payload"].get("event"))
        if record["payload_type"] != "runtime.session" or event.get("kind") != "model_completed":
            continue
        stream = _stream_id(record)
        if stream is not None and own is not None and stream != own:
            continue
        usage = event.get("usage")
        if not isinstance(usage, dict):
            continue
        ordinal += 1
        usage_id = _str(usage.get("usage_id")) or _str(event.get("usage_id"))
        seq = record.get("seq")
        keys = []
        if usage_id:
            keys.append(f"usage:{usage_id}")
        if isinstance(seq, int) and not isinstance(seq, bool):
            keys.append(f"seq:{stream or own or session_id}:{seq}")
        if any(key in seen for key in keys):
            continue
        seen.update(keys)

        tokens = _tokens(usage, mismatch)
        if tokens.total == 0:
            continue
        if usage_id:
            request_id = f"{SOURCE_ID}:{usage_id}"
        elif isinstance(seq, int) and not isinstance(seq, bool):
            request_id = f"{SOURCE_ID}:{stream or own or session_id}:{seq}"
        else:
            request_id = f"{SOURCE_ID}:{session_id}:n{ordinal}"

        raw: dict[str, RawScalar] = {}
        if (duration := event.get("duration_ms")) is not None and as_int(duration) >= 0:
            raw["duration_ms"] = as_int(duration)
        if semver:
            raw["cli_version"] = semver
        yield UsageEvent(
            source=SOURCE_ID,
            client=SOURCE_ID,
            provider=provider,
            model=_str(event.get("model")),
            timestamp=_micros_to_timestamp(record.get("recorded_at"), path),
            session_id=session_id,
            request_id=request_id,
            tokens=tokens,
            is_sidechain=sidechain,
            project=project,
            working_directory=cwd,
            title=title_of(project, session_id),
            title_source="folder",
            source_file=str(path),
            raw=raw,
        )
    if unknown[0]:
        warnings.append(f"{path.name}: {unknown[0]} records in unrecognised format")
    if mismatch[0]:
        warnings.append(
            f"{path.name}: {mismatch[0]} records where cache_read_tokens and cached_tokens "
            "differ (used cache_read_tokens)"
        )


SOURCE = Source(
    id=SOURCE_ID,
    label="Muse Code",
    clients={SOURCE_ID: "Muse Code"},
    default_roots=default_roots,
    files=session_files,
    parse=parse,
    token_data="full",
    display_path="$MUSE_DATA_DIR or ~/.local/share/muse/sessions/YYYY/MM/DD/<id>/session.jsonl",
    capabilities=Capabilities(),
    experimental=True,
)
