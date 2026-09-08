from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from ai_usage_cost.models import UsageEvent
from ai_usage_cost.sources.cursor import cursor_files, parse

FIXTURES = Path(__file__).parent / "fixtures" / "cursor"


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


def test_each_composer_yields_one_event(basic: list[UsageEvent]) -> None:
    assert len(basic) == 2


def test_composer_id_and_timestamp_come_from_the_row(basic: list[UsageEvent]) -> None:
    event = next(e for e in basic if e.session_id == "11111111-1111-1111-1111-111111111111")
    assert event.source == "cursor"
    assert event.client == "cursor"
    assert event.request_id == "cursor:11111111-1111-1111-1111-111111111111"
    assert event.model is None
    assert event.tokens is None
    assert event.timestamp.isoformat() == "2025-08-20T08:53:20+00:00"


def test_second_composer_gets_its_own_request_id(basic: list[UsageEvent]) -> None:
    event = next(e for e in basic if e.session_id == "22222222-2222-2222-2222-222222222222")
    assert event.request_id == "cursor:22222222-2222-2222-2222-222222222222"
    assert event.timestamp.isoformat() == "2025-08-20T09:53:20+00:00"


def test_empty_database_yields_no_events_and_no_warnings(tmp_path: Path) -> None:
    db_path = build_db(tmp_path, "empty.sql")
    warnings: list[str] = []
    assert list(parse(db_path, warnings)) == []
    assert warnings == []


def test_missing_cursor_disk_kv_table_yields_no_events_and_no_warnings(tmp_path: Path) -> None:
    db_path = build_db(tmp_path, "no_table.sql")
    warnings: list[str] = []
    assert list(parse(db_path, warnings)) == []
    assert warnings == []


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

    files = cursor_files(tmp_path)

    assert len(files) == 2
    assert files[0].parent.name == "globalStorage"
    assert files[1].parent.name == "abc123"


def test_no_installation_yields_no_files(tmp_path: Path) -> None:
    assert cursor_files(tmp_path) == []
