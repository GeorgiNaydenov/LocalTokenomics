from __future__ import annotations

import hashlib
import json
import sqlite3
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path

from .models import TokenUsage, UsageEvent
from .sources.base import Source, present_roots
from .trace import Outcome, OutcomeUpdate, Span

# Bytes hashed on either side of a file's previously-ingested end, to cheaply confirm that
# range is still byte-identical before trusting a resumed (partial) parse of it. Bounded
# cost regardless of file size -- this is a seek-and-read of a fixed window, never a hash of
# the whole prefix.
_BOUNDARY_WINDOW = 8192

MIGRATIONS: list[str] = [
    """
    CREATE TABLE requests (
      fingerprint TEXT PRIMARY KEY,
      source TEXT NOT NULL, client TEXT NOT NULL, provider TEXT,
      model TEXT, session_id TEXT NOT NULL, timestamp TEXT NOT NULL,
      request_id TEXT,
      uncached_input INTEGER, cache_read INTEGER, cache_write_5m INTEGER,
      cache_write_1h INTEGER, output INTEGER, reasoning_output INTEGER,
      is_sidechain INTEGER NOT NULL, tier TEXT NOT NULL,
      project TEXT, working_directory TEXT, repository TEXT, branch TEXT,
      machine TEXT NOT NULL, source_file TEXT NOT NULL, raw TEXT NOT NULL
    );
    CREATE INDEX requests_timestamp ON requests(timestamp);
    CREATE INDEX requests_source_file ON requests(source_file);
    CREATE TABLE files (
      path TEXT PRIMARY KEY, source TEXT NOT NULL,
      mtime REAL NOT NULL, size INTEGER NOT NULL,
      ingested_at TEXT NOT NULL, warnings TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE trace_events (
      span_id TEXT PRIMARY KEY,
      parent_id TEXT, record_parent TEXT,
      source TEXT NOT NULL, session_id TEXT NOT NULL, turn_id TEXT, agent_id TEXT,
      is_sidechain INTEGER NOT NULL, seq INTEGER NOT NULL,
      kind TEXT NOT NULL, name TEXT, model TEXT, status TEXT NOT NULL,
      started_at TEXT NOT NULL, ended_at TEXT,
      duration_ms INTEGER, duration_provenance TEXT NOT NULL,
      ttft_ms INTEGER,
      uncached_input INTEGER, cache_read INTEGER, cache_write_5m INTEGER,
      cache_write_1h INTEGER, output INTEGER, reasoning_output INTEGER,
      tokens_provenance TEXT NOT NULL,
      context_capacity INTEGER, capacity_provenance TEXT NOT NULL,
      retry_attempt INTEGER, error TEXT,
      source_file TEXT NOT NULL, record_offset INTEGER NOT NULL,
      record_length INTEGER NOT NULL, content_path TEXT,
      detail TEXT NOT NULL
    );
    CREATE INDEX trace_events_session ON trace_events(source, session_id, started_at, seq);
    CREATE INDEX trace_events_source_file ON trace_events(source_file);
    CREATE TABLE outcomes (
      source TEXT NOT NULL, session_id TEXT NOT NULL,
      outcome TEXT NOT NULL, notes TEXT NOT NULL, tags TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      PRIMARY KEY (source, session_id)
    );
    CREATE TABLE session_exclusions (
      source TEXT NOT NULL, session_id TEXT NOT NULL, excluded_at TEXT NOT NULL,
      PRIMARY KEY (source, session_id)
    );
    ALTER TABLE files ADD COLUMN parser_version INTEGER NOT NULL DEFAULT 0;
    """,
    """
    ALTER TABLE requests ADD COLUMN title TEXT;
    ALTER TABLE requests ADD COLUMN title_source TEXT NOT NULL DEFAULT 'folder';
    """,
    """
    ALTER TABLE files ADD COLUMN ingested_offset INTEGER NOT NULL DEFAULT 0;
    ALTER TABLE files ADD COLUMN boundary_hash TEXT;
    ALTER TABLE files ADD COLUMN title_seed TEXT;
    """,
]

PARSER_VERSION = 5

_TOKEN_COLUMNS = (
    "uncached_input",
    "cache_read",
    "cache_write_5m",
    "cache_write_1h",
    "output",
    "reasoning_output",
)

_SPAN_COLUMNS = (
    "span_id",
    "parent_id",
    "record_parent",
    "source",
    "session_id",
    "turn_id",
    "agent_id",
    "is_sidechain",
    "seq",
    "kind",
    "name",
    "model",
    "status",
    "started_at",
    "ended_at",
    "duration_ms",
    "duration_provenance",
    "ttft_ms",
    *_TOKEN_COLUMNS,
    "tokens_provenance",
    "context_capacity",
    "capacity_provenance",
    "retry_attempt",
    "error",
    "source_file",
    "record_offset",
    "record_length",
    "content_path",
    "detail",
)


@dataclass
class IngestSummary:
    files_parsed: int = 0
    files_skipped: int = 0
    warnings: list[str] = field(default_factory=list)


def open_store(path: Path | str) -> sqlite3.Connection:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    current = conn.execute("PRAGMA user_version").fetchone()[0]
    for index, migration in enumerate(MIGRATIONS[current:], start=current):
        conn.executescript(migration)
        conn.execute(f"PRAGMA user_version = {index + 1}")
        conn.commit()
    return conn


def fingerprint_of(event: UsageEvent) -> str:
    if event.request_id:
        key = f"{event.source}:id:{event.request_id}"
    else:
        total = event.tokens.total if event.tokens else ""
        offset = event.record_offset if event.record_offset is not None else ""
        key = (
            f"{event.source}:seq:{event.session_id}|{event.timestamp.isoformat()}|"
            f"{event.model or ''}|{total}|{event.source_file}|{offset}"
        )
    # A short, deterministic dedup key, never a security boundary. SHA-256 costs nothing
    # noticeable at this scale and avoids CodeQL's weak-hash rule outright, which does not
    # treat usedforsecurity=False as a mitigation for this query.
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def _to_utc(ts: datetime) -> datetime:
    return ts.astimezone(UTC) if ts.tzinfo is not None else ts.replace(tzinfo=UTC)


def _boundary_hash(path: Path, end: int) -> str:
    start = max(0, end - _BOUNDARY_WINDOW)
    with path.open("rb") as handle:
        handle.seek(start)
        chunk = handle.read(end - start)
    # A change-detection checksum, not a security use -- see fingerprint_of() above.
    return hashlib.sha256(chunk).hexdigest()


def _last_title(events: list[UsageEvent], fallback: str | None) -> str | None:
    for event in reversed(events):
        if event.title_source == "tool" and event.title:
            return event.title
    return fallback


def ingest(
    conn: sqlite3.Connection,
    sources: Iterable[Source],
    roots: dict[str, list[Path]] | None = None,
    *,
    rebuild: bool = False,
    exclude_projects: Sequence[str] = (),
    metadata_retention_days: int | None = None,
) -> IngestSummary:
    summary = IngestSummary()
    if rebuild:
        conn.execute("DELETE FROM requests")
        conn.execute("DELETE FROM trace_events")
        conn.execute("DELETE FROM files")
        conn.commit()

    known: dict[str, tuple[float, int, int, int, str | None, str | None]] = {
        row[0]: (row[1], row[2], row[3], row[4], row[5], row[6])
        for row in conn.execute(
            "SELECT path, mtime, size, parser_version, ingested_offset, "
            "boundary_hash, title_seed FROM files"
        )
    }
    excluded_sessions = {
        (row[0], row[1])
        for row in conn.execute("SELECT source, session_id FROM session_exclusions")
    }

    for source in sources:
        for root in present_roots(source, (roots or {}).get(source.id)):
            for path in source.files(root):
                key = str(path)
                try:
                    stat = path.stat()
                except OSError as exc:
                    summary.warnings.append(f"{source.id}: cannot read {path}: {exc}")
                    continue
                mtime, size = stat.st_mtime, stat.st_size
                prior = known.get(key)
                if not rebuild and prior is not None and (mtime, size, PARSER_VERSION) == prior[:3]:
                    summary.files_skipped += 1
                    continue

                warnings: list[str] = []
                # A file that only grew, whose source declares a resume hook, whose parser
                # logic hasn't changed, whose previous scan reached exactly its old end (not
                # a partial/failed run), and whose bytes up to that point are still
                # byte-identical (the boundary-hash check) can safely be re-read starting
                # from where the last scan left off -- every other case (a shrink, a
                # rewrite, an unresumable source, a version bump) gets the full, always-safe
                # reparse this already did.
                resumed = False
                try:
                    if (
                        not rebuild
                        and prior is not None
                        and source.parse_resume is not None
                        and prior[2] == PARSER_VERSION
                        and size > prior[1]
                        and prior[3] == prior[1]
                        and _boundary_hash(path, prior[1]) == prior[4]
                    ):
                        events = list(source.parse_resume(path, warnings, prior[1], prior[5]))
                        resumed = True
                    else:
                        events = list(source.parse(path, warnings))
                except OSError as exc:
                    summary.warnings.append(f"{source.id}: cannot read {path}: {exc}")
                    continue

                spans: list[Span] = []
                if source.spans is not None:
                    try:
                        spans = list(source.spans(path, warnings))
                    except OSError as exc:
                        warnings.append(f"{source.id}: cannot read {path}: {exc}")

                if not resumed:
                    conn.execute("DELETE FROM requests WHERE source_file = ?", (key,))
                conn.execute("DELETE FROM trace_events WHERE source_file = ?", (key,))
                for event in events:
                    _insert(conn, event, warnings)
                for span in spans:
                    if (span.source, span.session_id) in excluded_sessions:
                        continue
                    if _in_excluded_project(span, exclude_projects):
                        continue
                    _insert_span(conn, span)

                title_seed = _last_title(events, prior[5] if resumed and prior else None)
                conn.execute(
                    "INSERT OR REPLACE INTO files (path, source, mtime, size, ingested_at, "
                    "warnings, parser_version, ingested_offset, boundary_hash, title_seed) "
                    "VALUES (?, ?, ?, ?, datetime('now'), ?, ?, ?, ?, ?)",
                    (
                        key,
                        source.id,
                        mtime,
                        size,
                        json.dumps(warnings),
                        PARSER_VERSION,
                        size,
                        _boundary_hash(path, size),
                        title_seed,
                    ),
                )
                conn.commit()
                summary.files_parsed += 1
                summary.warnings.extend(warnings)

    if metadata_retention_days is not None:
        cutoff = datetime.now(tz=UTC) - timedelta(days=metadata_retention_days)
        conn.execute("DELETE FROM trace_events WHERE started_at < ?", (cutoff.isoformat(),))
        conn.commit()

    return summary


def _in_excluded_project(span: Span, exclude_projects: Sequence[str]) -> bool:
    project = span.detail.get("project")
    directory = span.detail.get("working_directory")
    for entry in exclude_projects:
        if project == entry:
            return True
        if isinstance(directory, str) and directory.startswith(entry):
            return True
    return False


def _insert(conn: sqlite3.Connection, event: UsageEvent, warnings: list[str] | None = None) -> None:
    tokens = event.tokens
    fingerprint = fingerprint_of(event)
    timestamp = _to_utc(event.timestamp).isoformat()
    token_values = (
        (
            tokens.uncached_input,
            tokens.cache_read,
            tokens.cache_write_5m,
            tokens.cache_write_1h,
            tokens.output,
            tokens.reasoning_output,
        )
        if tokens is not None
        else (None, None, None, None, None, None)
    )

    if tokens is not None:
        existing = conn.execute(
            "SELECT uncached_input, cache_read, cache_write_5m, cache_write_1h, "
            "output, reasoning_output FROM requests WHERE fingerprint = ?",
            (fingerprint,),
        ).fetchone()
        if existing is not None:
            if existing[:4] != (
                tokens.uncached_input,
                tokens.cache_read,
                tokens.cache_write_5m,
                tokens.cache_write_1h,
            ):
                if warnings is not None:
                    warnings.append(
                        f"{event.source}: two records for request {event.request_id!r} "
                        "disagree on input tokens -- keeping the first, discarding the other"
                    )
                return
            existing_output, existing_reasoning = existing[4], existing[5]
            if tokens.output > existing_output or tokens.reasoning_output > existing_reasoning:
                # Claude Code streams several assistant records per API response sharing one
                # message.id; input fields never vary across them but output/reasoning grow --
                # the last (equivalently, largest) record carries the final, billed count.
                conn.execute(
                    "UPDATE requests SET output = ?, reasoning_output = ?, "
                    "source_file = ?, timestamp = ?, raw = ? WHERE fingerprint = ?",
                    (
                        max(tokens.output, existing_output),
                        max(tokens.reasoning_output, existing_reasoning),
                        event.source_file,
                        timestamp,
                        json.dumps(event.raw),
                        fingerprint,
                    ),
                )
            return

    conn.execute(
        f"""
        INSERT OR IGNORE INTO requests (
          fingerprint, source, client, provider, model, session_id, timestamp, request_id,
          {", ".join(_TOKEN_COLUMNS)},
          is_sidechain, tier, project, working_directory, repository, branch,
          title, title_source, machine, source_file, raw
        ) VALUES (
          ?, ?, ?, ?, ?, ?, ?, ?, {", ".join("?" * len(_TOKEN_COLUMNS))},
          ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        (
            fingerprint,
            event.source,
            event.client,
            event.provider,
            event.model,
            event.session_id,
            timestamp,
            event.request_id,
            *token_values,
            int(event.is_sidechain),
            event.tier,
            event.project,
            event.working_directory,
            event.repository,
            event.branch,
            event.title,
            event.title_source,
            event.machine,
            event.source_file,
            json.dumps(event.raw),
        ),
    )


def _insert_span(conn: sqlite3.Connection, span: Span) -> None:
    tokens = span.tokens
    token_values = (
        (
            tokens.uncached_input,
            tokens.cache_read,
            tokens.cache_write_5m,
            tokens.cache_write_1h,
            tokens.output,
            tokens.reasoning_output,
        )
        if tokens is not None
        else (None, None, None, None, None, None)
    )
    if tokens is not None:
        existing = conn.execute(
            "SELECT output, reasoning_output FROM trace_events WHERE span_id = ?",
            (span.span_id,),
        ).fetchone()
        if existing is not None:
            existing_output, existing_reasoning = existing
            if existing_output is not None and (
                tokens.output > existing_output
                or tokens.reasoning_output > (existing_reasoning or 0)
            ):
                # Mirrors the requests-table rule in _insert(): a later record for the same
                # span (a later record within one file, or the same message.id re-ingested
                # from a different source_file) can carry a larger, final output/reasoning
                # count -- refresh it in place rather than leaving the trace stuck on a
                # partial value from whichever record happened to be seen first.
                conn.execute(
                    "UPDATE trace_events SET output = ?, reasoning_output = ?, "
                    "ended_at = COALESCE(?, ended_at) WHERE span_id = ?",
                    (
                        max(tokens.output, existing_output),
                        max(tokens.reasoning_output, existing_reasoning or 0),
                        span.ended_at.isoformat() if span.ended_at else None,
                        span.span_id,
                    ),
                )
            return
    conn.execute(
        f"""
        INSERT OR IGNORE INTO trace_events ({", ".join(_SPAN_COLUMNS)})
        VALUES ({", ".join("?" * len(_SPAN_COLUMNS))})
        """,
        (
            span.span_id,
            span.parent_id,
            span.record_parent,
            span.source,
            span.session_id,
            span.turn_id,
            span.agent_id,
            int(span.is_sidechain),
            span.seq,
            span.kind,
            span.name,
            span.model,
            span.status,
            span.started_at.isoformat(),
            span.ended_at.isoformat() if span.ended_at else None,
            span.duration_ms,
            span.duration_provenance,
            span.ttft_ms,
            *token_values,
            span.tokens_provenance,
            span.context_capacity,
            span.capacity_provenance,
            span.retry_attempt,
            span.error,
            span.source_file,
            span.record_offset,
            span.record_length,
            span.content_path,
            json.dumps(span.detail),
        ),
    )


def _span_from_row(row: dict) -> Span:
    tokens = None
    if row["tokens_provenance"] != "unavailable":
        tokens = TokenUsage(**{col: row[col] for col in _TOKEN_COLUMNS})
    return Span(
        span_id=row["span_id"],
        parent_id=row["parent_id"],
        record_parent=row["record_parent"],
        source=row["source"],
        session_id=row["session_id"],
        turn_id=row["turn_id"],
        agent_id=row["agent_id"],
        is_sidechain=bool(row["is_sidechain"]),
        seq=row["seq"],
        kind=row["kind"],
        name=row["name"],
        model=row["model"],
        status=row["status"],
        started_at=row["started_at"],
        ended_at=row["ended_at"],
        duration_ms=row["duration_ms"],
        duration_provenance=row["duration_provenance"],
        ttft_ms=row["ttft_ms"],
        tokens=tokens,
        tokens_provenance=row["tokens_provenance"],
        context_capacity=row["context_capacity"],
        capacity_provenance=row["capacity_provenance"],
        retry_attempt=row["retry_attempt"],
        error=row["error"],
        source_file=row["source_file"],
        record_offset=row["record_offset"],
        record_length=row["record_length"],
        content_path=row["content_path"],
        detail=json.loads(row["detail"]),
    )


def load_spans(conn: sqlite3.Connection, source: str, session_id: str) -> list[Span]:
    rows = conn.execute(
        f"SELECT {', '.join(_SPAN_COLUMNS)} FROM trace_events "
        "WHERE source = ? AND session_id = ? ORDER BY started_at, seq",
        (source, session_id),
    ).fetchall()
    spans = [_span_from_row(dict(zip(_SPAN_COLUMNS, row, strict=True))) for row in rows]
    subagents: dict[str, str] = {}
    for span in spans:
        if span.kind == "subagent" and span.agent_id:
            subagents[span.agent_id] = span.span_id
    for span in spans:
        if span.parent_id is not None or not span.agent_id:
            continue
        parent = subagents.get(span.agent_id)
        if parent is not None and parent != span.span_id:
            span.parent_id = parent
    return spans


def get_outcome(conn: sqlite3.Connection, source: str, session_id: str) -> Outcome | None:
    row = conn.execute(
        "SELECT outcome, notes, tags, updated_at FROM outcomes WHERE source = ? AND session_id = ?",
        (source, session_id),
    ).fetchone()
    if row is None:
        return None
    return Outcome(
        source=source,
        session_id=session_id,
        outcome=row[0],
        notes=row[1],
        tags=json.loads(row[2]),
        updated_at=row[3],
    )


def put_outcome(
    conn: sqlite3.Connection, source: str, session_id: str, update: OutcomeUpdate
) -> Outcome:
    updated_at = datetime.now(tz=UTC)
    conn.execute(
        "INSERT OR REPLACE INTO outcomes "
        "(source, session_id, outcome, notes, tags, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
        (
            source,
            session_id,
            update.outcome,
            update.notes,
            json.dumps(update.tags),
            updated_at.isoformat(),
        ),
    )
    conn.commit()
    return Outcome(
        source=source,
        session_id=session_id,
        outcome=update.outcome,
        notes=update.notes,
        tags=list(update.tags),
        updated_at=updated_at,
    )


def delete_session(conn: sqlite3.Connection, source: str, session_id: str) -> int:
    deleted = conn.execute(
        "DELETE FROM trace_events WHERE source = ? AND session_id = ?", (source, session_id)
    ).rowcount
    conn.execute("DELETE FROM outcomes WHERE source = ? AND session_id = ?", (source, session_id))
    conn.execute(
        "INSERT OR REPLACE INTO session_exclusions (source, session_id, excluded_at) "
        "VALUES (?, ?, datetime('now'))",
        (source, session_id),
    )
    conn.commit()
    return deleted


def session_exists(conn: sqlite3.Connection, source: str, session_id: str) -> bool:
    row = conn.execute(
        """
        SELECT 1 FROM requests WHERE source = ? AND session_id = ?
        UNION ALL
        SELECT 1 FROM trace_events WHERE source = ? AND session_id = ?
        LIMIT 1
        """,
        (source, session_id, source, session_id),
    ).fetchone()
    if row is None:
        return False
    excluded = conn.execute(
        "SELECT 1 FROM session_exclusions WHERE source = ? AND session_id = ?",
        (source, session_id),
    ).fetchone()
    return excluded is None


def session_flags(conn: sqlite3.Connection) -> dict[tuple[str, str], tuple[bool, int, str]]:
    # A failed tool call and its tool_result both carry status='error' (the sources copy
    # the result's status onto the call span that opened it), so counting every row with
    # status='error' double-counts the same failure. Mirrors trace.is_error_span: an
    # 'error'-kind row always counts; a tool_result with status='error' always counts; a
    # tool_call/retrieval/subagent row counts only when it has no paired tool_result (kept
    # in sync with trace.TOOL_KINDS); any other kind with status='error' counts.
    rows = conn.execute(
        """
        SELECT source, session_id, SUM(spans), SUM(errors), MAX(outcome) FROM (
          SELECT source, session_id, 1 AS spans,
                 CASE
                   WHEN kind = 'error' THEN 1
                   WHEN status != 'error' THEN 0
                   WHEN kind = 'tool_result' THEN 1
                   WHEN kind IN ('tool_call', 'retrieval', 'subagent')
                        AND span_id NOT IN (
                          SELECT parent_id FROM trace_events
                          WHERE kind = 'tool_result' AND parent_id IS NOT NULL
                        )
                   THEN 1
                   WHEN kind NOT IN ('tool_call', 'retrieval', 'subagent', 'tool_result', 'error')
                   THEN 1
                   ELSE 0
                 END AS errors,
                 '' AS outcome
          FROM trace_events
          UNION ALL
          SELECT source, session_id, 0, 0, outcome FROM outcomes
        )
        GROUP BY source, session_id
        """
    ).fetchall()
    return {(row[0], row[1]): (row[2] > 0, row[3], row[4] or "unrated") for row in rows}


def file_counts(conn: sqlite3.Connection) -> dict[str, int]:
    return dict(conn.execute("SELECT source, COUNT(*) FROM files GROUP BY source"))


def load(conn: sqlite3.Connection) -> tuple[list[UsageEvent], int, list[str]]:
    columns = [
        "source",
        "client",
        "provider",
        "model",
        "session_id",
        "timestamp",
        "request_id",
        *_TOKEN_COLUMNS,
        "is_sidechain",
        "tier",
        "project",
        "working_directory",
        "repository",
        "branch",
        "title",
        "title_source",
        "machine",
        "source_file",
        "raw",
    ]
    rows = conn.execute(f"SELECT {', '.join(columns)} FROM requests ORDER BY timestamp").fetchall()
    events = [_event_from_row(dict(zip(columns, row, strict=True))) for row in rows]

    files_count = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    warnings: list[str] = []
    for (raw_warnings,) in conn.execute("SELECT warnings FROM files"):
        warnings.extend(json.loads(raw_warnings))

    return events, files_count, warnings


def _event_from_row(row: dict) -> UsageEvent:
    tokens = None
    if row["uncached_input"] is not None:
        tokens = TokenUsage(**{col: row[col] for col in _TOKEN_COLUMNS})
    return UsageEvent(
        source=row["source"],
        client=row["client"],
        provider=row["provider"],
        model=row["model"],
        timestamp=row["timestamp"],
        session_id=row["session_id"],
        request_id=row["request_id"],
        tokens=tokens,
        is_sidechain=bool(row["is_sidechain"]),
        tier=row["tier"],
        project=row["project"],
        working_directory=row["working_directory"],
        repository=row["repository"],
        branch=row["branch"],
        title=row["title"],
        title_source=row["title_source"],
        machine=row["machine"],
        source_file=row["source_file"],
        raw=json.loads(row["raw"]),
    )
