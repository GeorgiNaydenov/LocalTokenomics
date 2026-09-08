from __future__ import annotations

import json
import os
import platform
import sys
from collections.abc import Iterator
from pathlib import Path

from ..models import UsageEvent
from ..trace import Capabilities
from .base import Source, parse_timestamp, read_sqlite

_APP_DIR = "Cursor"


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
    return [base / _APP_DIR]


def cursor_files(root: Path) -> list[Path]:
    found: list[Path] = []
    global_db = root / "User" / "globalStorage" / "state.vscdb"
    if global_db.is_file():
        found.append(global_db)
    workspace_root = root / "User" / "workspaceStorage"
    if workspace_root.is_dir():
        for workspace in sorted(workspace_root.iterdir()):
            db = workspace / "state.vscdb"
            if db.is_file():
                found.append(db)
    return found


def _has_table(path: Path, table: str, warnings: list[str]) -> bool:
    rows = read_sqlite(
        path,
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
        warnings=warnings,
    )
    return bool(rows)


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    if not _has_table(path, "cursorDiskKV", warnings):
        return
    rows = read_sqlite(
        path,
        "SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'",
        warnings=warnings,
    )
    for key, value in rows:
        composer_id = key.split(":", 1)[1]
        try:
            data = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(data, dict):
            continue
        yield UsageEvent(
            source="cursor",
            client="cursor",
            model=None,
            timestamp=parse_timestamp(data.get("createdAt"), path),
            session_id=composer_id,
            request_id=f"cursor:{composer_id}",
            tokens=None,
            machine=platform.node(),
            source_file=str(path),
        )


SOURCE = Source(
    id="cursor",
    label="Cursor",
    clients={"cursor": "Cursor"},
    default_roots=default_roots,
    files=cursor_files,
    parse=parse,
    token_data="session",
    display_path="<vscode-data>/User/globalStorage/state.vscdb (cursorDiskKV, composerData:*)",
    capabilities=Capabilities(),
)
