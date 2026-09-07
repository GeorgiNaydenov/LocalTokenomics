from __future__ import annotations

import os
import platform
import sys
from collections.abc import Iterator
from pathlib import Path

from ..models import UsageEvent
from .base import Source, parse_timestamp, project_of, read_sqlite, single_file

_VARIANTS = ["Code", "Code - Insiders", "VSCodium", "VSCodium - Insiders"]


def default_roots() -> list[Path]:
    if sys.platform == "win32":
        app_data = os.environ.get("APPDATA")
        base = Path(app_data) if app_data else None
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path.home() / ".config"
    if base is None:
        return []
    return [
        base / variant / "User" / "globalStorage" / "github.copilot-chat" / "session-store.db"
        for variant in _VARIANTS
    ]


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    rows = read_sqlite(
        path,
        "SELECT turns.id, turns.session_id, turns.turn_index, turns.timestamp, "
        "sessions.cwd, sessions.repository, sessions.branch "
        "FROM turns JOIN sessions ON turns.session_id = sessions.id",
        warnings=warnings,
    )
    for _turn_id, session_id, turn_index, timestamp, cwd, repository, branch in rows:
        yield UsageEvent(
            source="copilot-chat",
            client="copilot-chat",
            provider="github",
            model=None,
            timestamp=parse_timestamp(timestamp),
            session_id=str(session_id),
            request_id=f"copilot-chat:{session_id}:{turn_index}",
            tokens=None,
            working_directory=cwd if isinstance(cwd, str) else None,
            repository=repository if isinstance(repository, str) else None,
            branch=branch if isinstance(branch, str) else None,
            project=project_of(cwd),
            machine=platform.node(),
        )


SOURCE = Source(
    id="copilot-chat",
    label="GitHub Copilot Chat",
    clients={"copilot-chat": "GitHub Copilot Chat"},
    default_roots=default_roots,
    files=single_file,
    parse=parse,
)
