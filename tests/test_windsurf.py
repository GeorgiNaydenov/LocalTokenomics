from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from ai_usage_cost.models import UsageEvent
from ai_usage_cost.sources.windsurf import parse, windsurf_files

FIXTURES = Path(__file__).parent / "fixtures" / "windsurf"


def build_db(tmp_path: Path, sql_file: str) -> Path:
    db_path = tmp_path / "state.vscdb"
    sql = (FIXTURES / sql_file).read_text(encoding="utf-8")
    with sqlite3.connect(db_path) as conn:
        conn.executescript(sql)
    return db_path


@pytest.fixture
def basic(tmp_path: Path) -> list[UsageEvent]:
    db_path = build_db(tmp_path, "basic.sql")
    return list(parse(db_path, []))


def test_only_tabs_with_bubbles_yield_events(basic: list[UsageEvent]) -> None:
    assert len(basic) == 1


def test_tab_id_and_timestamp_come_from_the_row(basic: list[UsageEvent]) -> None:
    event = basic[0]
    assert event.source == "windsurf"
    assert event.client == "windsurf"
    assert event.session_id == "tab-1"
    assert event.request_id == "windsurf:tab-1"
    assert event.model is None
    assert event.tokens is None
    assert event.timestamp.isoformat() == "2025-08-20T08:53:20+00:00"


def test_chat_title_becomes_the_tool_title(basic: list[UsageEvent]) -> None:
    assert basic[0].title == "Add tests"
    assert basic[0].title_source == "tool"


def test_missing_chat_title_falls_back_to_the_folder_title(tmp_path: Path) -> None:
    db_path = tmp_path / "state.vscdb"
    with sqlite3.connect(db_path) as conn:
        conn.executescript(
            "CREATE TABLE ItemTable (key TEXT UNIQUE, value TEXT);"
            "INSERT INTO ItemTable (key, value) VALUES ('cascade.chatdata', "
            '\'{"tabs": [{"tabId": "tab-9", "lastSendTime": 1755680000000, '
            '"bubbles": [{"type": "user", "text": "hi"}]}]}\');'
        )
    event = list(parse(db_path, []))[0]
    assert event.title_source == "folder"
    assert event.title == "(no project)_tab-9"


def test_empty_database_yields_no_events_and_no_warnings(tmp_path: Path) -> None:
    db_path = build_db(tmp_path, "empty.sql")
    warnings: list[str] = []
    assert list(parse(db_path, warnings)) == []
    assert warnings == []


def test_missing_chat_key_yields_no_events_and_no_warnings(tmp_path: Path) -> None:
    db_path = build_db(tmp_path, "no_chat_key.sql")
    warnings: list[str] = []
    assert list(parse(db_path, warnings)) == []
    assert warnings == []


def test_malformed_value_warns_and_yields_no_events(tmp_path: Path) -> None:
    db_path = build_db(tmp_path, "malformed.sql")
    warnings: list[str] = []
    assert list(parse(db_path, warnings)) == []
    assert len(warnings) == 1


def test_missing_file_yields_no_events_and_no_warnings(tmp_path: Path) -> None:
    warnings: list[str] = []
    assert list(parse(tmp_path / "does-not-exist.vscdb", warnings)) == []
    assert warnings == []


def test_discovers_global_and_workspace_state_dbs(tmp_path: Path) -> None:
    global_dir = tmp_path / "User" / "globalStorage"
    global_dir.mkdir(parents=True)
    (global_dir / "state.vscdb").write_bytes(b"")
    ws_dir = tmp_path / "User" / "workspaceStorage" / "abc123"
    ws_dir.mkdir(parents=True)
    (ws_dir / "state.vscdb").write_bytes(b"")

    files = windsurf_files(tmp_path)

    assert len(files) == 2
    assert files[0].parent.name == "globalStorage"
    assert files[1].parent.name == "abc123"


def test_no_installation_yields_no_files(tmp_path: Path) -> None:
    assert windsurf_files(tmp_path) == []
