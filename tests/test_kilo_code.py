from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from ai_usage_cost.sources import registry
from ai_usage_cost.sources.kilo_code import SOURCE
from test_opencode import add_message, add_part, add_session, build_db, populate, tokens

# Kilo adds migrations on top of the OpenCode schema: an unknown extra column must be harmless.
KILO_SCHEMA_EXTRA = "ALTER TABLE session ADD COLUMN kilo_org_id TEXT;"


def kilo_db(tmp_path: Path) -> Path:
    path = build_db(tmp_path, "kilo.db")

    def fill(conn: sqlite3.Connection) -> None:
        conn.execute(KILO_SCHEMA_EXTRA)
        add_session(conn, directory="/work/kilo-proj")
        add_message(conn, "m1", model="claude-sonnet-4-5", provider="kilo")
        add_part(conn, "p1", "m1", tok=tokens(10, 5, 2, 100, 20), cost=0.05)

    return populate(path, fill)


def test_kilo_events_use_kilo_source_and_same_mapping(tmp_path: Path) -> None:
    path = kilo_db(tmp_path)
    warnings: list[str] = []
    events = [e for f in SOURCE.files(path) for e in SOURCE.parse(f, warnings)]
    assert warnings == []
    assert len(events) == 1
    event = events[0]
    assert event.source == event.client == "kilo-code"
    assert event.request_id == "kilo-code:p1"
    assert event.provider == "kilo"
    assert event.project == "kilo-proj"
    assert (event.tokens.uncached_input, event.tokens.output) == (10, 7)
    assert event.reported_cost == pytest.approx(0.05)


def test_kilo_roots_and_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("KILO_DB", str(tmp_path / "k.db"))
    assert SOURCE.default_roots() == [tmp_path / "k.db"]
    monkeypatch.delenv("KILO_DB")
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    assert SOURCE.default_roots()[0] == tmp_path / "kilo"


def test_kilo_finds_channel_dbs_not_opencode_dbs(tmp_path: Path) -> None:
    for name in ("kilo.db", "kilo-dev.db", "opencode.db", "kilo.db-shm"):
        (tmp_path / name).write_bytes(b"")
    assert [p.name for p in SOURCE.files(tmp_path)] == ["kilo-dev.db", "kilo.db"]


def test_kilo_registered_experimental_and_missing_root_safe(tmp_path: Path) -> None:
    assert registry()["kilo-code"] is SOURCE
    assert SOURCE.experimental is True
    assert list(SOURCE.parse(tmp_path / "nope.db", [])) == []
