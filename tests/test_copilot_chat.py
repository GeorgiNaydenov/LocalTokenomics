from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from ai_usage_cost.models import UsageEvent
from ai_usage_cost.sources.copilot_chat import parse

FIXTURES = Path(__file__).parent / "fixtures" / "copilot_chat"


def build_db(tmp_path: Path, sql_file: str) -> Path:
    db_path = tmp_path / "session-store.db"
    sql = (FIXTURES / sql_file).read_text(encoding="utf-8")
    with sqlite3.connect(db_path) as conn:
        conn.executescript(sql)
    return db_path


@pytest.fixture
def basic(tmp_path: Path) -> list[UsageEvent]:
    db_path = build_db(tmp_path, "basic.sql")
    return list(parse(db_path, []))


def test_each_turn_yields_one_event(basic: list[UsageEvent]) -> None:
    assert len(basic) == 3


def test_populated_session_carries_cwd_repository_branch_and_project(
    basic: list[UsageEvent],
) -> None:
    event = next(e for e in basic if e.request_id == "copilot-chat:sess-alpha:0")
    assert event.provider == "github"
    assert event.client == "copilot-chat"
    assert event.source == "copilot-chat"
    assert event.session_id == "sess-alpha"
    assert event.working_directory == "/home/user/alpha"
    assert event.repository == "user/alpha"
    assert event.branch == "main"
    assert event.project == "alpha"
    assert event.model is None
    assert event.tokens is None


def test_second_turn_in_same_session_gets_its_own_request_id(
    basic: list[UsageEvent],
) -> None:
    event = next(e for e in basic if e.request_id == "copilot-chat:sess-alpha:1")
    assert event.session_id == "sess-alpha"
    assert event.project == "alpha"


def test_null_cwd_falls_back_to_no_project(basic: list[UsageEvent]) -> None:
    event = next(e for e in basic if e.session_id == "sess-null-cwd")
    assert event.working_directory is None
    assert event.repository is None
    assert event.branch is None
    assert event.project is None


def test_empty_database_yields_no_events_and_no_warnings(tmp_path: Path) -> None:
    db_path = build_db(tmp_path, "empty.sql")
    warnings: list[str] = []
    events = list(parse(db_path, warnings))
    assert events == []
    assert warnings == []
