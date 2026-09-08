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

_APP_DIR = "Windsurf"
_CHAT_KEY = "cascade.chatdata"


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


def windsurf_files(root: Path) -> list[Path]:
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


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    rows = read_sqlite(
        path, "SELECT value FROM ItemTable WHERE key = ?", (_CHAT_KEY,), warnings=warnings
    )
    if not rows:
        return
    try:
        data = json.loads(rows[0][0])
    except (json.JSONDecodeError, TypeError):
        warnings.append(f"{path.name}: cannot parse {_CHAT_KEY}")
        return
    if not isinstance(data, dict):
        return
    for tab in data.get("tabs") or []:
        if not isinstance(tab, dict):
            continue
        tab_id = tab.get("tabId")
        bubbles = tab.get("bubbles")
        if not tab_id or not isinstance(bubbles, list) or not bubbles:
            continue
        yield UsageEvent(
            source="windsurf",
            client="windsurf",
            model=None,
            timestamp=parse_timestamp(tab.get("lastSendTime"), path),
            session_id=str(tab_id),
            request_id=f"windsurf:{tab_id}",
            tokens=None,
            machine=platform.node(),
            source_file=str(path),
        )


SOURCE = Source(
    id="windsurf",
    label="Windsurf",
    clients={"windsurf": "Windsurf"},
    default_roots=default_roots,
    files=windsurf_files,
    parse=parse,
    token_data="session",
    display_path="<vscode-data>/User/globalStorage/state.vscdb (ItemTable, cascade.chatdata)",
    capabilities=Capabilities(),
)
