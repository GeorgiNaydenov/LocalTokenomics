from __future__ import annotations

import hashlib
import json
import sqlite3
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

from .models import TokenUsage, UsageEvent
from .sources.base import Source, scan

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
]

_TOKEN_COLUMNS = (
    "uncached_input", "cache_read", "cache_write_5m", "cache_write_1h",
    "output", "reasoning_output",
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
) -> IngestSummary:
    summary = IngestSummary()
    if rebuild:
        conn.execute("DELETE FROM requests")
        conn.execute("DELETE FROM files")
        conn.commit()

    known: dict[str, tuple[float, int]] = {
        row[0]: (row[1], row[2])
        for row in conn.execute("SELECT path, mtime, size FROM files")
    }

    for source in sources:
        for path, events, warnings in scan(source, (roots or {}).get(source.id)):
            stat = path.stat()
            current = (stat.st_mtime, stat.st_size)
            if not rebuild and known.get(str(path)) == current:
                summary.files_skipped += 1
                continue

            conn.execute("DELETE FROM requests WHERE source_file = ?", (str(path),))
            for event in events:
                _insert(conn, event)
            conn.execute(
                "INSERT OR REPLACE INTO files (path, source, mtime, size, ingested_at, warnings) "
                "VALUES (?, ?, ?, ?, datetime('now'), ?)",
                (str(path), source.id, current[0], current[1], json.dumps(warnings)),
            )
            conn.commit()
            summary.files_parsed += 1
            summary.warnings.extend(warnings)

    return summary


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
