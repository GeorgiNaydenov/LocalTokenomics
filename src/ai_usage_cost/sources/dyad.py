from __future__ import annotations

import os
import platform
from collections.abc import Iterator
from pathlib import Path

from ..models import UsageEvent
from ..trace import Capabilities
from .base import Source, parse_timestamp, read_sqlite, single_file, title_of


def default_roots() -> list[Path]:
    home = Path.home()
    roots = []
    app_data = os.environ.get("APPDATA")
    if app_data:
        roots.append(Path(app_data) / "dyad" / "sqlite.db")
    roots.append(home / "Library" / "Application Support" / "dyad" / "sqlite.db")
    roots.append(home / ".config" / "dyad" / "sqlite.db")
    return roots


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    rows = read_sqlite(
        path,
        "SELECT messages.id, messages.chat_id, messages.created_at, apps.name, apps.path, "
        "apps.github_org, apps.github_repo, apps.github_branch, chats.title "
        "FROM messages JOIN chats ON messages.chat_id = chats.id "
        "JOIN apps ON chats.app_id = apps.id "
        "WHERE messages.role = 'assistant'",
        warnings=warnings,
    )
    for message_id, chat_id, created_at, app_name, app_path, org, repo, branch, chat_title in rows:
        title = chat_title.strip() if isinstance(chat_title, str) and chat_title.strip() else None
        yield UsageEvent(
            source="dyad",
            client="dyad",
            model=None,
            timestamp=parse_timestamp(created_at),
            session_id=str(chat_id),
            request_id=f"dyad:{message_id}",
            tokens=None,
            project=app_name,
            working_directory=app_path,
            repository=f"{org}/{repo}" if org and repo else None,
            branch=branch,
            title=title if title else title_of(app_name, str(chat_id)),
            title_source="tool" if title else "folder",
            machine=platform.node(),
        )


SOURCE = Source(
    id="dyad",
    label="Dyad",
    clients={"dyad": "Dyad"},
    default_roots=default_roots,
    files=single_file,
    parse=parse,
    token_data="session",
    display_path="<app-data>/dyad/sqlite.db",
    capabilities=Capabilities(),
)
