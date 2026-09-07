from __future__ import annotations

import json
import sqlite3
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from ..models import UsageEvent


@dataclass(frozen=True)
class Source:
    id: str
    label: str
    clients: dict[str, str]
    default_roots: Callable[[], list[Path]]
    files: Callable[[Path], list[Path]]
    parse: Callable[[Path, list[str]], Iterator[UsageEvent]]


def scan(
    source: Source, roots: Sequence[Path] | None
) -> Iterator[tuple[Path, list[UsageEvent], list[str]]]:
    for root in roots if roots is not None else source.default_roots():
        if not root.exists():
            continue
        for path in source.files(root):
            warnings: list[str] = []
            try:
                events = list(source.parse(path, warnings))
            except OSError as exc:
                yield path, [], [f"{source.id}: cannot read {path}: {exc}"]
                continue
            yield path, events, warnings


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
    if bad > 1:
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
