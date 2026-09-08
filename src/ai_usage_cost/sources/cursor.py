from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from ..models import UsageEvent
from ..trace import Capabilities
from .base import Source


def default_roots() -> list[Path]:
    return []


def cursor_files(root: Path) -> list[Path]:
    return []


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    yield from ()


SOURCE = Source(
    id="cursor",
    label="Cursor",
    clients={"cursor": "Cursor"},
    default_roots=default_roots,
    files=cursor_files,
    parse=parse,
    token_data="session",
    display_path="not audited; no adapter",
    capabilities=Capabilities(),
)
