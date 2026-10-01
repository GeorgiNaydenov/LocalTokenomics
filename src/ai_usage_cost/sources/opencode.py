"""OpenCode (anomalyco/opencode, formerly sst/opencode) -- SQLite ``opencode.db``.

Kilo Code v7 is an OpenCode fork with the same schema; ``kilo_code.py`` builds its own
``Source`` from :func:`make_source` below.

Exact per-request records are the ``part`` rows whose ``data.type`` is ``step-finish``
(tokens + USD cost per model call). The parent assistant message carries cost accumulated
across steps but its ``tokens`` are OVERWRITTEN by each step, so message-level tokens are
used only for completed assistant messages that have no step-finish part at all.

Limitations:
- JSON ``storage/`` (OpenCode < v1.2.0) is not parsed, and ignored when a DB exists.
- The DB is WAL-mode: recent writes sit in ``<db>-wal`` while the main file's mtime/size do
  not change, and ``store.ingest`` only skips on (mtime, size). ``files()`` therefore also
  returns the ``-wal`` sibling purely as a change trigger: parsing it re-reads the main DB
  (SQLite merges the WAL) and yields the same events keyed to the DB path, which the store
  deduplicates by ``request_id``. Truncation after a checkpoint changes the main file, so
  that path is covered too.
- Prompt/response text is never selected: values are pulled with ``json_extract``.
"""

from __future__ import annotations

import os
import re
import sys
from collections.abc import Callable, Iterator
from pathlib import Path

from ..models import TokenUsage, UsageEvent
from ..trace import Capabilities
from .base import Source, as_int, parse_timestamp, project_of, read_sqlite, title_of

_PLACEHOLDER_TITLE = re.compile(r"^(new|child) session\b", re.IGNORECASE)
_WAL = "-wal"
_DRIFT_RATIO = 0.10
_DRIFT_MIN_TOKENS = 1_000

_TOKEN_PATHS = (
    ("input", "$.tokens.input"),
    ("output", "$.tokens.output"),
    ("reasoning", "$.tokens.reasoning"),
    ("cache_read", "$.tokens.cache.read"),
    ("cache_write", "$.tokens.cache.write"),
)
# `data.type` per the upstream schema; `$type` accepted in case a build tags it that way.
_PART_TYPE = (
    "COALESCE(json_extract(p.data, '$.type'), json_extract(p.data, '$.\"$type\"')) = 'step-finish'"
)
# json_extract raises on malformed JSON and would void the whole query, so rows are filtered
# through json_valid first and the skipped count is reported once.
_VALID_PART = "(SELECT * FROM part WHERE json_valid(data)) p"
_VALID_MESSAGE = "(SELECT * FROM message WHERE json_valid(data)) m"
_MEMO: dict[Path, tuple[tuple, list[UsageEvent]]] = {}
_SESSION_TOKEN_COLS = (
    "tokens_input",
    "tokens_output",
    "tokens_reasoning",
    "tokens_cache_read",
    "tokens_cache_write",
)


def _xdg_data_home() -> Path:
    env = os.environ.get("XDG_DATA_HOME", "").strip()
    return Path(env) if env else Path.home() / ".local" / "share"


def make_roots(app: str, db_env: str) -> Callable[[], list[Path]]:
    def default_roots() -> list[Path]:
        override = os.environ.get(db_env, "").strip()
        if override:
            return [Path(override)]
        roots = [_xdg_data_home() / app]
        if sys.platform == "win32":
            appdata = os.environ.get("APPDATA", "").strip()
            if appdata:
                roots.append(Path(appdata) / app)
        unique: list[Path] = []
        for root in roots:
            if root not in unique:
                unique.append(root)
        return unique

    return default_roots


def make_files(app: str) -> Callable[[Path], list[Path]]:
    channel = re.compile(f"{re.escape(app)}-.+\\.db")

    def files(root: Path) -> list[Path]:
        if root.is_file():
            databases = [root]
        elif root.is_dir():
            # `<app>.db` plus channel builds `<app>-<channel>.db`; never the -wal/-shm files.
            databases = sorted(
                p
                for p in root.iterdir()
                if p.is_file() and (p.name == f"{app}.db" or channel.fullmatch(p.name))
            )
        else:
            return []
        found: list[Path] = []
        for database in databases:
            found.append(database)
            wal = database.with_name(database.name + _WAL)
            if wal.is_file():
                found.append(wal)
        return found

    return files


def _columns(path: Path, table: str, warnings: list[str]) -> set[str]:
    rows = read_sqlite(path, f"PRAGMA table_info({table})", warnings=warnings)
    return {str(row[1]) for row in rows}


def _tokens_sql(alias: str) -> str:
    return ", ".join(f"json_extract({alias}.data, '{path}')" for _, path in _TOKEN_PATHS)


def _tokens_of(values: tuple) -> TokenUsage:
    got = {name: max(0, as_int(v)) for (name, _), v in zip(_TOKEN_PATHS, values, strict=True)}
    return TokenUsage(
        # tokens.input is already exclusive of cache.
        uncached_input=got["input"],
        cache_read=got["cache_read"],
        cache_write_5m=got["cache_write"],
        # Pricing prices `output` only; reasoning is billed as output.
        output=got["output"] + got["reasoning"],
        reasoning_output=got["reasoning"],
    )


def _cost_of(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return float(value) if value >= 0 else None


def _text(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _stamp(path: Path) -> tuple[float, int]:
    try:
        stat = path.stat()
    except OSError:
        return (0.0, -1)
    return (stat.st_mtime, stat.st_size)


def make_parse(
    source_id: str, client: str, app: str
) -> Callable[[Path, list[str]], Iterator[UsageEvent]]:
    def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
        db = path.with_name(path.name[: -len(_WAL)]) if path.name.endswith(_WAL) else path
        if not db.is_file():
            return
        # `files()` lists the db and its -wal; both map here, so parse once per change.
        key = (source_id, *_stamp(db), *_stamp(db.with_name(db.name + _WAL)))
        cached = _MEMO.get(db)
        if cached is not None and cached[0] == key:
            yield from cached[1]
            return
        events = list(_parse_db(db, source_id, client, app, warnings))
        _MEMO[db] = (key, events)
        yield from events

    return parse


def _parse_db(
    db: Path, source_id: str, client: str, app: str, warnings: list[str]
) -> Iterator[UsageEvent]:
    message_cols = _columns(db, "message", warnings)
    if not {"id", "session_id", "data"} <= message_cols:
        warnings.append(f"{db.name}: no usable `message` table (unsupported schema), skipped")
        return
    part_cols = _columns(db, "part", warnings)
    has_parts = {"id", "message_id", "data"} <= part_cols
    if not has_parts:
        warnings.append(f"{db.name}: no usable `part` table, using message-level tokens only")
    bad = read_sqlite(
        db,
        "SELECT (SELECT count(*) FROM message WHERE NOT json_valid(data)) + "
        + ("(SELECT count(*) FROM part WHERE NOT json_valid(data))" if has_parts else "0"),
        warnings=warnings,
    )
    if bad and bad[0][0]:
        warnings.append(f"{db.name}: skipped {bad[0][0]} rows with malformed JSON data")
    sessions = _load_sessions(db, _columns(db, "session", warnings), warnings)
    totals: dict[str, int] = {}

    def build(
        *,
        row_id: str,
        request_id: str,
        session_id: str | None,
        values: tuple,
        cost: object,
        model: object,
        provider: object,
        stamp: object,
    ) -> UsageEvent | None:
        if not session_id:
            return None
        tokens = _tokens_of(values)
        reported = _cost_of(cost)
        if tokens.total == 0 and not reported:
            return None
        info = sessions.get(session_id, {})
        directory = _text(info.get("directory"))
        project = project_of(directory)
        title = _text(info.get("title"))
        use_title = title is not None and not _PLACEHOLDER_TITLE.match(title)
        totals[session_id] = totals.get(session_id, 0) + tokens.total
        return UsageEvent(
            source=source_id,
            client=client,
            provider=_text(provider),
            model=_text(model),
            timestamp=parse_timestamp(stamp, db),
            session_id=session_id,
            request_id=f"{source_id}:{request_id}",
            tokens=tokens,
            is_sidechain=info.get("parent_id") is not None,
            project=project,
            working_directory=directory,
            title=title if use_title and title else title_of(project, session_id),
            title_source="tool" if use_title else "folder",
            source_file=str(db),
            reported_cost=reported,
            raw={"opencode_id": row_id},
        )

    if has_parts:
        part_time = "p.time_created" if "time_created" in part_cols else "NULL"
        part_session = "p.session_id" if "session_id" in part_cols else "m.session_id"
        rows = read_sqlite(
            db,
            f"SELECT p.id, {part_session}, {part_time}, json_extract(p.data, '$.cost'), "
            f"{_tokens_sql('p')}, json_extract(m.data, '$.modelID'), "
            "json_extract(m.data, '$.providerID'), json_extract(m.data, '$.time.completed') "
            f"FROM {_VALID_PART} LEFT JOIN {_VALID_MESSAGE} ON m.id = p.message_id "
            f"WHERE {_PART_TYPE} ORDER BY p.id",
            warnings=warnings,
        )
        for row in rows:
            event = build(
                row_id=str(row[0]),
                request_id=str(row[0]),
                session_id=_text(row[1]),
                values=row[4:9],
                cost=row[3],
                model=row[9],
                provider=row[10],
                stamp=row[2] or row[11],
            )
            if event:
                yield event

    exclusion = (
        f"AND NOT EXISTS (SELECT 1 FROM {_VALID_PART} WHERE p.message_id = m.id AND {_PART_TYPE}) "
        if has_parts
        else ""
    )
    msg_time = "m.time_created" if "time_created" in message_cols else "NULL"
    # Completed messages only: an in-flight one will gain step-finish parts, and counting
    # its overwritten message-level tokens now would double count once they land.
    fallback = read_sqlite(
        db,
        f"SELECT m.id, m.session_id, {msg_time}, json_extract(m.data, '$.cost'), "
        f"{_tokens_sql('m')}, json_extract(m.data, '$.modelID'), "
        "json_extract(m.data, '$.providerID'), json_extract(m.data, '$.time.completed') "
        f"FROM {_VALID_MESSAGE} WHERE json_extract(m.data, '$.role') = 'assistant' "
        "AND json_extract(m.data, '$.time.completed') IS NOT NULL "
        f"{exclusion}ORDER BY m.id",
        warnings=warnings,
    )
    for row in fallback:
        event = build(
            row_id=str(row[0]),
            request_id=f"msg:{row[0]}",
            session_id=_text(row[1]),
            values=row[4:9],
            cost=row[3],
            model=row[9],
            provider=row[10],
            stamp=row[11] or row[2],
        )
        if event:
            yield event

    for session_id, derived in totals.items():
        recorded = sessions.get(session_id, {}).get("tokens")
        if isinstance(recorded, int) and recorded > 0:
            gap = abs(derived - recorded)
            if gap >= _DRIFT_MIN_TOKENS and gap > _DRIFT_RATIO * recorded:
                warnings.append(
                    f"{app}: session {session_id} has {derived:,} tokens in its requests but "
                    f"the tool recorded {recorded:,} for the session"
                )


def _load_sessions(db: Path, cols: set[str], warnings: list[str]) -> dict[str, dict]:
    if "id" not in cols:
        warnings.append(f"{db.name}: no usable `session` table, titles and projects unavailable")
        return {}
    present = [c for c in ("parent_id", "directory", "title") if c in cols]
    token_cols = [c for c in _SESSION_TOKEN_COLS if c in cols]
    selected = "".join(f", {c}" for c in present + token_cols)
    rows = read_sqlite(db, f"SELECT id{selected} FROM session", warnings=warnings)
    sessions: dict[str, dict] = {}
    for row in rows:
        info: dict = dict(zip(present, row[1 : 1 + len(present)], strict=True))
        if len(token_cols) == len(_SESSION_TOKEN_COLS):
            info["tokens"] = sum(as_int(v) for v in row[1 + len(present) :])
        sessions[str(row[0])] = info
    return sessions


def make_source(
    *,
    source_id: str,
    label: str,
    app: str,
    db_env: str,
    display_path: str,
) -> Source:
    return Source(
        id=source_id,
        label=label,
        clients={source_id: label},
        default_roots=make_roots(app, db_env),
        files=make_files(app),
        parse=make_parse(source_id, source_id, app),
        token_data="full",
        display_path=display_path,
        capabilities=Capabilities(),
        experimental=True,
    )


SOURCE = make_source(
    source_id="opencode",
    label="OpenCode",
    app="opencode",
    db_env="OPENCODE_DB",
    display_path="$XDG_DATA_HOME/opencode/opencode.db (or %APPDATA%\\opencode)",
)
