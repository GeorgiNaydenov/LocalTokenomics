"""Source registry -- the extension point.

To support another CLI, add a module here that subclasses :class:`JsonlSource`,
implements ``default_roots`` and ``iter_file``, and calls :func:`register`. Pricing,
aggregation, the API and the dashboard all work on :class:`UsageEvent` and pick the new
source up with no further changes.
"""

from __future__ import annotations

import json
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from ..models import UsageEvent


@dataclass
class ScanResult:
    events: list[UsageEvent] = field(default_factory=list)
    files: int = 0
    warnings: list[str] = field(default_factory=list)

    def extend(self, other: ScanResult) -> None:
        self.events.extend(other.events)
        self.files += other.files
        self.warnings.extend(other.warnings)


class JsonlSource:
    """Base class for CLIs that log one JSON object per line."""

    id: str = ""
    label: str = ""

    def default_roots(self) -> list[Path]:
        raise NotImplementedError

    def iter_file(self, path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
        raise NotImplementedError

    def files(self, root: Path) -> list[Path]:
        return sorted(p for p in root.rglob("*.jsonl") if p.is_file())

    def scan(self, roots: Sequence[Path] | None = None) -> ScanResult:
        result = ScanResult()
        for root in roots if roots is not None else self.default_roots():
            if not root.exists():
                continue
            for path in self.files(root):
                result.files += 1
                try:
                    result.events.extend(self.iter_file(path, result.warnings))
                except OSError as exc:
                    result.warnings.append(f"{self.id}: cannot read {path}: {exc}")
        return result


def read_json_lines(path: Path, warnings: list[str]) -> Iterator[dict]:
    """Yield parsed objects, skipping blank and malformed lines.

    Logs are appended to while a session is live, so a truncated final line is normal
    and is not worth a warning; anything else malformed is counted once per file.
    """
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


def parse_timestamp(value: object, fallback: Path | None = None) -> datetime:
    if isinstance(value, str) and value:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            parsed = None
        if parsed is not None:
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
    if fallback is not None:
        return datetime.fromtimestamp(fallback.stat().st_mtime, tz=UTC)
    return datetime.now(tz=UTC)


_REGISTRY: dict[str, JsonlSource] = {}


def register(source: JsonlSource) -> JsonlSource:
    _REGISTRY[source.id] = source
    return source


def registry() -> dict[str, JsonlSource]:
    from . import claude_code, codex  # noqa: F401  -- import for side-effect registration

    return dict(_REGISTRY)


def scan_all(
    only: Sequence[str] | None = None,
    roots: dict[str, list[Path]] | None = None,
) -> ScanResult:
    combined = ScanResult()
    for source_id, source in registry().items():
        if only and source_id not in only:
            continue
        combined.extend(source.scan((roots or {}).get(source_id)))
    combined.events.sort(key=lambda e: e.timestamp)
    return combined
