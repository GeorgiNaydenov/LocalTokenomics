from __future__ import annotations

import os
import platform
from collections.abc import Iterator
from pathlib import Path

from ..models import UsageEvent
from .base import Source, parse_timestamp, read_sqlite, single_file


def default_roots() -> list[Path]:
    home = Path.home()
    roots = []
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        roots.append(Path(local_app_data) / "Ollama" / "db.sqlite")
    roots.append(home / "Library" / "Application Support" / "Ollama" / "db.sqlite")
    roots.append(home / ".config" / "Ollama" / "db.sqlite")
    roots.append(home / ".local" / "share" / "Ollama" / "db.sqlite")
    return roots


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    rows = read_sqlite(
        path,
        "SELECT id, chat_id, model_name, model_cloud, created_at FROM messages "
        "WHERE role = 'assistant'",
        warnings=warnings,
    )
    for row_id, chat_id, model_name, model_cloud, created_at in rows:
        yield UsageEvent(
            source="ollama-app",
            client="ollama-app",
            provider="ollama" if model_cloud else "local",
            model=model_name,
            timestamp=parse_timestamp(created_at),
            session_id=str(chat_id),
            request_id=f"ollama-app:{row_id}",
            tokens=None,
            machine=platform.node(),
        )


SOURCE = Source(
    id="ollama-app",
    label="Ollama",
    clients={"ollama-app": "Ollama"},
    default_roots=default_roots,
    files=single_file,
    parse=parse,
)
