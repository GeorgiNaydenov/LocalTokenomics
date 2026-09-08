from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from ai_usage_cost.models import UsageEvent
from ai_usage_cost.sources.ollama_app import parse

FIXTURES = Path(__file__).parent / "fixtures" / "ollama_app"


def build_db(tmp_path: Path, sql_file: str) -> Path:
    db_path = tmp_path / "db.sqlite"
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


def test_local_model_resolves_to_local_provider(basic: list[UsageEvent]) -> None:
    event = next(e for e in basic if e.model == "llama3.1:8b")
    assert event.provider == "local"
    assert event.client == "ollama-app"
    assert event.source == "ollama-app"
    assert event.tokens is None
    assert event.request_id == "ollama-app:2"
    assert event.session_id == "chat-1"


def test_cloud_model_resolves_to_ollama_provider(basic: list[UsageEvent]) -> None:
    event = next(e for e in basic if e.model == "gpt-oss:120b-cloud")
    assert event.provider == "ollama"
    assert event.tokens is None
    assert event.request_id == "ollama-app:3"
    assert event.session_id == "chat-2"
