from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from ai_usage_cost import store
from ai_usage_cost.models import TokenUsage, UsageEvent


def _event(reported_cost: float | None, request_id: str = "req-1") -> UsageEvent:
    return UsageEvent(
        source="fake",
        client="fake-client",
        provider="unknown",
        model="m1",
        timestamp=datetime(2026, 8, 20, 10, 0, tzinfo=UTC),
        session_id="s1",
        request_id=request_id,
        tokens=TokenUsage(uncached_input=100, output=50),
        reported_cost=reported_cost,
    )


def test_parser_version_was_bumped_for_the_reported_cost_column() -> None:
    assert store.PARSER_VERSION == 6


def test_a_database_at_the_previous_schema_version_gains_reported_cost(tmp_path: Path) -> None:
    path = tmp_path / "usage.db"
    previous = len(store.MIGRATIONS) - 1
    conn = sqlite3.connect(path)
    for index, migration in enumerate(store.MIGRATIONS[:previous]):
        conn.executescript(migration)
        conn.execute(f"PRAGMA user_version = {index + 1}")
    conn.execute(
        "INSERT INTO requests (fingerprint, source, client, provider, model, session_id, "
        "timestamp, request_id, uncached_input, cache_read, cache_write_5m, cache_write_1h, "
        "output, reasoning_output, is_sidechain, tier, machine, source_file, raw) VALUES "
        "('old', 'fake', 'fake-client', 'unknown', 'm1', 's0', '2026-08-01T00:00:00+00:00', "
        "'old-req', 10, 0, 0, 0, 5, 0, 0, 'standard', 'm', 'f.jsonl', '{}')"
    )
    conn.commit()
    assert "reported_cost" not in {row[1] for row in conn.execute("PRAGMA table_info(requests)")}
    conn.close()

    migrated = store.open_store(path)
    assert migrated.execute("PRAGMA user_version").fetchone()[0] == len(store.MIGRATIONS)
    assert "reported_cost" in {row[1] for row in migrated.execute("PRAGMA table_info(requests)")}

    events, _, _ = store.load(migrated)
    assert [event.request_id for event in events] == ["old-req"]
    assert events[0].reported_cost is None


def test_reported_cost_round_trips_through_the_store(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    # pylint: disable=protected-access
    store._insert(conn, _event(1.2345, "with"))
    store._insert(conn, _event(None, "without"))
    conn.commit()

    by_request = {event.request_id: event for event in store.load(conn)[0]}
    assert by_request["with"].reported_cost == 1.2345
    assert by_request["without"].reported_cost is None


def test_a_later_streamed_record_keeps_its_reported_cost(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    first = _event(None, "stream")
    last = _event(0.5, "stream").model_copy(
        update={"tokens": TokenUsage(uncached_input=100, output=500)}
    )
    # pylint: disable=protected-access
    store._insert(conn, first)
    store._insert(conn, last)
    conn.commit()

    (event,) = store.load(conn)[0]
    assert event.tokens is not None and event.tokens.output == 500
    assert event.reported_cost == 0.5
