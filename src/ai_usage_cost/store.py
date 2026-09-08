from __future__ import annotations

import hashlib
import json
import sqlite3
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path

from .models import TokenUsage, UsageEvent
from .sources.base import Source, scan
from .trace import Outcome, OutcomeUpdate, Span

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
]

PARSER_VERSION = 2

_TOKEN_COLUMNS = (
    "uncached_input", "cache_read", "cache_write_5m", "cache_write_1h",
    "output", "reasoning_output",
)

_SPAN_COLUMNS = (
    "span_id", "parent_id", "record_parent", "source", "session_id", "turn_id", "agent_id",
    "is_sidechain", "seq", "kind", "name", "model", "status", "started_at", "ended_at",
    "duration_ms", "duration_provenance", "ttft_ms",
    *_TOKEN_COLUMNS,
    "tokens_provenance", "context_capacity", "capacity_provenance",
    "retry_attempt", "error", "source_file", "record_offset", "record_length",
    "content_path", "detail",
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
        key = f"id:{event.request_id}"
    else:
        total = event.tokens.total if event.tokens else ""
        key = f"seq:{event.session_id}|{event.timestamp.isoformat()}|{event.model or ''}|{total}"
    return hashlib.sha1(key.encode("utf-8")).hexdigest()


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

    known: dict[str, tuple[float, int, int]] = {
        row[0]: (row[1], row[2], row[3])
        for row in conn.execute("SELECT path, mtime, size, parser_version FROM files")
    }
    excluded_sessions = {
        (row[0], row[1])
        for row in conn.execute("SELECT source, session_id FROM session_exclusions")
    }

    for source in sources:
        for path, events, spans, warnings in scan(source, (roots or {}).get(source.id)):
            stat = path.stat()
            current = (stat.st_mtime, stat.st_size, PARSER_VERSION)
            if not rebuild and known.get(str(path)) == current:
                summary.files_skipped += 1
                continue

            conn.execute("DELETE FROM requests WHERE source_file = ?", (str(path),))
            conn.execute("DELETE FROM trace_events WHERE source_file = ?", (str(path),))
            for event in events:
                _insert(conn, event)
            for span in spans:
                if (span.source, span.session_id) in excluded_sessions:
                    continue
                if _in_excluded_project(span, exclude_projects):
                    continue
                _insert_span(conn, span)
            conn.execute(
                "INSERT OR REPLACE INTO files "
                "(path, source, mtime, size, ingested_at, warnings, parser_version) "
                "VALUES (?, ?, ?, ?, datetime('now'), ?, ?)",
                (str(path), source.id, current[0], current[1], json.dumps(warnings), current[2]),
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


def _insert(conn: sqlite3.Connection, event: UsageEvent) -> None:
    tokens = event.tokens
    token_values = (
        (tokens.uncached_input, tokens.cache_read, tokens.cache_write_5m,
         tokens.cache_write_1h, tokens.output, tokens.reasoning_output)
        if tokens is not None
        else (None, None, None, None, None, None)
    )
    conn.execute(
        f"""
        INSERT OR IGNORE INTO requests (
          fingerprint, source, client, provider, model, session_id, timestamp, request_id,
          {", ".join(_TOKEN_COLUMNS)},
          is_sidechain, tier, project, working_directory, repository, branch,
          machine, source_file, raw
        ) VALUES (
          ?, ?, ?, ?, ?, ?, ?, ?, {", ".join("?" * len(_TOKEN_COLUMNS))},
          ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        (
            fingerprint_of(event), event.source, event.client, event.provider,
            event.model, event.session_id, event.timestamp.isoformat(), event.request_id,
            *token_values,
            int(event.is_sidechain), event.tier, event.project, event.working_directory,
            event.repository, event.branch, event.machine, event.source_file,
            json.dumps(event.raw),
        ),
    )


def _insert_span(conn: sqlite3.Connection, span: Span) -> None:
    tokens = span.tokens
    token_values = (
        (tokens.uncached_input, tokens.cache_read, tokens.cache_write_5m,
         tokens.cache_write_1h, tokens.output, tokens.reasoning_output)
        if tokens is not None
        else (None, None, None, None, None, None)
    )
    conn.execute(
        f"""
        INSERT OR IGNORE INTO trace_events ({", ".join(_SPAN_COLUMNS)})
        VALUES ({", ".join("?" * len(_SPAN_COLUMNS))})
        """,
        (
            span.span_id, span.parent_id, span.record_parent, span.source, span.session_id,
            span.turn_id, span.agent_id, int(span.is_sidechain), span.seq, span.kind,
            span.name, span.model, span.status, span.started_at.isoformat(),
            span.ended_at.isoformat() if span.ended_at else None,
            span.duration_ms, span.duration_provenance, span.ttft_ms,
            *token_values,
            span.tokens_provenance, span.context_capacity, span.capacity_provenance,
            span.retry_attempt, span.error, span.source_file, span.record_offset,
            span.record_length, span.content_path, json.dumps(span.detail),
        ),
    )


def _span_from_row(row: dict) -> Span:
    tokens = None
    if row["tokens_provenance"] != "unavailable":
        tokens = TokenUsage(**{col: row[col] for col in _TOKEN_COLUMNS})
    return Span(
        span_id=row["span_id"], parent_id=row["parent_id"], record_parent=row["record_parent"],
        source=row["source"], session_id=row["session_id"], turn_id=row["turn_id"],
        agent_id=row["agent_id"], is_sidechain=bool(row["is_sidechain"]), seq=row["seq"],
        kind=row["kind"], name=row["name"], model=row["model"], status=row["status"],
        started_at=row["started_at"], ended_at=row["ended_at"],
        duration_ms=row["duration_ms"], duration_provenance=row["duration_provenance"],
        ttft_ms=row["ttft_ms"], tokens=tokens, tokens_provenance=row["tokens_provenance"],
        context_capacity=row["context_capacity"], capacity_provenance=row["capacity_provenance"],
        retry_attempt=row["retry_attempt"], error=row["error"], source_file=row["source_file"],
        record_offset=row["record_offset"], record_length=row["record_length"],
        content_path=row["content_path"], detail=json.loads(row["detail"]),
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
        "SELECT outcome, notes, tags, updated_at FROM outcomes "
        "WHERE source = ? AND session_id = ?",
        (source, session_id),
    ).fetchone()
    if row is None:
        return None
    return Outcome(
        source=source, session_id=session_id,
        outcome=row[0], notes=row[1], tags=json.loads(row[2]), updated_at=row[3],
    )


def put_outcome(
    conn: sqlite3.Connection, source: str, session_id: str, update: OutcomeUpdate
) -> Outcome:
    updated_at = datetime.now(tz=UTC)
    conn.execute(
        "INSERT OR REPLACE INTO outcomes "
        "(source, session_id, outcome, notes, tags, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
        (source, session_id, update.outcome, update.notes, json.dumps(update.tags),
         updated_at.isoformat()),
    )
    conn.commit()
    return Outcome(
        source=source, session_id=session_id, outcome=update.outcome,
        notes=update.notes, tags=list(update.tags), updated_at=updated_at,
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
    rows = conn.execute(
        """
        SELECT source, session_id, SUM(spans), SUM(errors), MAX(outcome) FROM (
          SELECT source, session_id, 1 AS spans,
                 CASE WHEN kind = 'error' OR status = 'error' THEN 1 ELSE 0 END AS errors,
                 '' AS outcome
          FROM trace_events
          UNION ALL
          SELECT source, session_id, 0, 0, outcome FROM outcomes
        )
        GROUP BY source, session_id
        """
    ).fetchall()
    return {
        (row[0], row[1]): (row[2] > 0, row[3], row[4] or "unrated")
        for row in rows
    }


def file_counts(conn: sqlite3.Connection) -> dict[str, int]:
    return dict(conn.execute("SELECT source, COUNT(*) FROM files GROUP BY source"))


def load(conn: sqlite3.Connection) -> tuple[list[UsageEvent], int, list[str]]:
    columns = [
        "source", "client", "provider", "model", "session_id", "timestamp", "request_id",
        *_TOKEN_COLUMNS,
        "is_sidechain", "tier", "project", "working_directory", "repository", "branch",
        "machine", "source_file", "raw",
    ]
    rows = conn.execute(
        f"SELECT {', '.join(columns)} FROM requests ORDER BY timestamp"
    ).fetchall()
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
        source=row["source"], client=row["client"], provider=row["provider"],
        model=row["model"], timestamp=row["timestamp"], session_id=row["session_id"],
        request_id=row["request_id"], tokens=tokens,
        is_sidechain=bool(row["is_sidechain"]), tier=row["tier"],
        project=row["project"], working_directory=row["working_directory"],
        repository=row["repository"], branch=row["branch"], machine=row["machine"],
        source_file=row["source_file"], raw=json.loads(row["raw"]),
    )
