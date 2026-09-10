from __future__ import annotations

import json
import sqlite3
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from ..models import UsageEvent
from ..trace import Capabilities, Span

TokenData = Literal["full", "session"]


@dataclass(frozen=True)
class Source:
    id: str
    label: str
    clients: dict[str, str]
    default_roots: Callable[[], list[Path]]
    files: Callable[[Path], list[Path]]
    parse: Callable[[Path, list[str]], Iterator[UsageEvent]]
    token_data: TokenData
    display_path: str
    spans: Callable[[Path, list[str]], Iterator[Span]] | None = None
    capabilities: Capabilities = field(default_factory=Capabilities)
    # Most sources accumulate state across a whole file (a model or reconciliation total
    # discovered once and applied to many records later on) and must be re-read from the
    # start whenever the file changes -- `parse_resume` is an optional, source-declared
    # exception for a parser whose only cross-record state is small enough to hand back in:
    # given a byte offset already ingested and that state, it yields only the events found
    # after that offset, so a file that has only grown does not have to be parsed all over
    # again. A source that does not set this is unaffected; `ingest()` falls back to a full
    # reparse for it exactly as before.
    parse_resume: Callable[[Path, list[str], int, str | None], Iterator[UsageEvent]] | None = None

    @property
    def root_hint(self) -> str:
        return f"--root {self.id}=PATH"


def present_roots(source: Source, roots: Sequence[Path] | None) -> list[Path]:
    chosen = roots if roots is not None else source.default_roots()
    return [root for root in chosen if root.exists()]


def scan(
    source: Source, roots: Sequence[Path] | None
) -> Iterator[tuple[Path, list[UsageEvent], list[Span], list[str]]]:
    for root in roots if roots is not None else source.default_roots():
        if not root.exists():
            continue
        for path in source.files(root):
            warnings: list[str] = []
            try:
                events = list(source.parse(path, warnings))
                spans = list(source.spans(path, warnings)) if source.spans else []
            except OSError as exc:
                yield path, [], [], [f"{source.id}: cannot read {path}: {exc}"]
                continue
            yield path, events, spans, warnings


def read_json_lines(path: Path, warnings: list[str]) -> Iterator[dict]:
    bad = 0
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                bad += 1
                continue
            if isinstance(obj, dict):
                yield obj
    if bad > 0:
        warnings.append(f"{path.name}: skipped {bad} unparsable lines")


def read_json_records(
    path: Path, warnings: list[str], start_offset: int = 0
) -> Iterator[tuple[int, int, dict]]:
    bad = 0
    offset = start_offset
    with path.open("rb") as handle:
        if start_offset:
            # Binary-mode seeking is byte-exact, unlike a text-mode handle's seek (which
            # Python only guarantees for offsets earlier obtained from that same handle's
            # own tell(), not an arbitrary size recorded on a previous scan). A resume
            # offset always sits right after a `\n` an earlier full read consumed, so a
            # raw byte seek lands exactly on the next record's first byte.
            handle.seek(start_offset)
        for raw in handle:
            start = offset
            offset += len(raw)
            line = raw.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                bad += 1
                continue
            if isinstance(obj, dict):
                yield start, len(raw), obj
    if bad > 0:
        warnings.append(f"{path.name}: skipped {bad} unparsable lines")


def read_sqlite(
    path: Path, sql: str, params: Sequence[object] = (), *, warnings: list[str] | None = None
) -> list[tuple]:
    if not path.is_file():
        return []
    try:
        uri = f"file:{path.as_posix()}?mode=ro"
        with sqlite3.connect(uri, uri=True) as conn:
            return conn.execute(sql, params).fetchall()
    except sqlite3.Error as exc:
        if warnings is not None:
            warnings.append(f"{path}: cannot read database: {exc}")
        return []


def jsonl_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.jsonl") if p.is_file())


def single_file(root: Path) -> list[Path]:
    return [root] if root.is_file() else []


def parse_timestamp(value: object, fallback: Path | None = None) -> datetime:
    if isinstance(value, int | float) and not isinstance(value, bool):
        seconds = value / 1000 if value > 10_000_000_000 else value
        try:
            return datetime.fromtimestamp(seconds, tz=UTC)
        except (OverflowError, OSError, ValueError):
            pass
    if isinstance(value, str) and value:
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            parsed = None
        if parsed is not None:
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
    if fallback is not None:
        return datetime.fromtimestamp(fallback.stat().st_mtime, tz=UTC)
    return datetime.now(tz=UTC)


def project_of(cwd: object) -> str | None:
    if isinstance(cwd, str) and cwd:
        return Path(cwd.replace("\\", "/")).name or cwd
    return None


def as_int(value: object) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def title_of(project: str | None, session_id: str) -> str:
    """Folder-fallback display title: ``f"{project or '(no project)'}_{session_id}"``.

    This is the last rung of the title fallback chain (``title_source="folder"``),
    shared by every source so the string is identical to what
    ``web/src/format.ts``'s ``sessionDisplayName`` used to build client-side.
    """
    return f"{project or '(no project)'}_{session_id}"
