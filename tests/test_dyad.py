from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from ai_usage_cost.models import UsageEvent
from ai_usage_cost.sources.dyad import parse

FIXTURES = Path(__file__).parent / "fixtures" / "dyad"


def build_db(tmp_path: Path, sql_file: str) -> Path:
    db_path = tmp_path / "sqlite.db"
    sql = (FIXTURES / sql_file).read_text(encoding="utf-8")
    with sqlite3.connect(db_path) as conn:
        conn.executescript(sql)
    return db_path


@pytest.fixture
def basic(tmp_path: Path) -> list[UsageEvent]:
    db_path = build_db(tmp_path, "basic.sql")
    return list(parse(db_path, []))


def test_only_assistant_rows_produce_events(basic: list[UsageEvent]) -> None:
    assert len(basic) == 2


def test_repo_populated_app_maps_org_and_repo(basic: list[UsageEvent]) -> None:
    event = next(e for e in basic if e.session_id == "1")
    assert event.client == "dyad"
    assert event.source == "dyad"
    assert event.project == "alpha"
    assert event.working_directory == "/home/user/alpha"
    assert event.repository == "acme/alpha-app"
    assert event.branch == "main"
    assert event.model is None
    assert event.tokens is None
    assert event.request_id == "dyad:2"


def test_repo_missing_app_maps_repository_to_none(basic: list[UsageEvent]) -> None:
    event = next(e for e in basic if e.session_id == "2")
    assert event.project == "beta"
    assert event.working_directory == "/home/user/beta"
    assert event.repository is None
    assert event.branch is None
    assert event.model is None
    assert event.tokens is None
    assert event.request_id == "dyad:3"


def test_chat_title_becomes_the_tool_title(basic: list[UsageEvent]) -> None:
    first = next(e for e in basic if e.session_id == "1")
    assert first.title == "first chat"
    assert first.title_source == "tool"

    second = next(e for e in basic if e.session_id == "2")
    assert second.title == "second chat"
    assert second.title_source == "tool"


def test_null_chat_title_falls_back_to_the_folder_title(tmp_path: Path) -> None:
    db_path = build_db(tmp_path, "null_title.sql")
    event = list(parse(db_path, []))[0]
    assert event.title_source == "folder"
    assert event.title == "gamma_1"
