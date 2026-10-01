from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from ai_usage_cost.models import UsageEvent
from ai_usage_cost.sources import registry
from ai_usage_cost.sources.opencode import SOURCE, make_files
from conftest import analyze_roots

SCHEMA = """
CREATE TABLE session (
  id TEXT PRIMARY KEY, project_id TEXT, parent_id TEXT, slug TEXT, directory TEXT, title TEXT,
  version TEXT, cost REAL, tokens_input INTEGER, tokens_output INTEGER,
  tokens_reasoning INTEGER, tokens_cache_read INTEGER, tokens_cache_write INTEGER,
  time_created INTEGER, time_updated INTEGER);
CREATE TABLE message (
  id TEXT PRIMARY KEY, session_id TEXT, time_created INTEGER, time_updated INTEGER, data TEXT);
CREATE TABLE part (
  id TEXT PRIMARY KEY, message_id TEXT, session_id TEXT, time_created INTEGER,
  time_updated INTEGER, data TEXT);
"""

T0 = 1_790_000_000_000


def tokens(inp: int, out: int, reasoning: int = 0, read: int = 0, write: int = 0) -> dict:
    return {
        "input": inp,
        "output": out,
        "reasoning": reasoning,
        "cache": {"read": read, "write": write},
    }


def add_session(
    conn: sqlite3.Connection,
    sid: str = "ses_1",
    *,
    parent: str | None = None,
    directory: str | None = "/work/demo",
    title: str | None = "Demo",
    totals: tuple[int, int, int, int, int] = (0, 0, 0, 0, 0),
) -> None:
    conn.execute(
        "INSERT INTO session (id, parent_id, directory, title, tokens_input, tokens_output, "
        "tokens_reasoning, tokens_cache_read, tokens_cache_write) VALUES (?,?,?,?,?,?,?,?,?)",
        (sid, parent, directory, title, *totals),
    )


def add_message(
    conn: sqlite3.Connection,
    mid: str,
    sid: str = "ses_1",
    *,
    role: str = "assistant",
    model: str | None = "claude-sonnet-4-5",
    provider: str | None = "anthropic",
    msg_tokens: dict | None = None,
    cost: float | None = None,
    completed: int | None = T0 + 5_000,
    extra: dict | None = None,
) -> None:
    data: dict = {"role": role, "time": {"created": T0}}
    if completed is not None:
        data["time"]["completed"] = completed
    if model:
        data["modelID"] = model
    if provider:
        data["providerID"] = provider
    if msg_tokens is not None:
        data["tokens"] = msg_tokens
    if cost is not None:
        data["cost"] = cost
    data.update(extra or {})
    conn.execute(
        "INSERT INTO message (id, session_id, time_created, data) VALUES (?,?,?,?)",
        (mid, sid, T0, json.dumps(data)),
    )


def add_part(
    conn: sqlite3.Connection,
    pid: str,
    mid: str,
    sid: str = "ses_1",
    *,
    kind: str = "step-finish",
    tok: dict | None = None,
    cost: float | None = None,
    at: int = T0 + 1_000,
    text: str | None = None,
) -> None:
    data: dict = {"type": kind}
    if tok is not None:
        data["tokens"] = tok
    if cost is not None:
        data["cost"] = cost
    if text is not None:
        data["text"] = text
    conn.execute(
        "INSERT INTO part (id, message_id, session_id, time_created, data) VALUES (?,?,?,?,?)",
        (pid, mid, sid, at, json.dumps(data)),
    )


def build_db(tmp_path: Path, name: str = "opencode.db", *, schema: str = SCHEMA) -> Path:
    path = tmp_path / name
    conn = sqlite3.connect(path)
    conn.executescript(schema)
    conn.commit()
    conn.close()
    return path


def populate(path: Path, fn) -> Path:  # type: ignore[no-untyped-def]
    conn = sqlite3.connect(path)
    fn(conn)
    conn.commit()
    conn.close()
    return path


def parse_all(path: Path) -> tuple[list[UsageEvent], list[str]]:
    warnings: list[str] = []
    events: list[UsageEvent] = []
    for file in SOURCE.files(path):
        events.extend(SOURCE.parse(file, warnings))
    return events, warnings


def three_step_db(tmp_path: Path) -> Path:
    def fill(conn: sqlite3.Connection) -> None:
        add_session(conn, totals=(0, 0, 0, 0, 0))
        # Message tokens are the LAST step only; message cost is the sum of all three.
        add_message(conn, "msg_1", msg_tokens=tokens(30, 40, 4, 500, 0), cost=0.06)
        add_part(conn, "prt_1", "msg_1", tok=tokens(10, 20, 5, 100, 50), cost=0.01, at=T0 + 1)
        add_part(conn, "prt_2", "msg_1", tok=tokens(20, 30, 0, 300, 0), cost=0.02, at=T0 + 2)
        add_part(conn, "prt_3", "msg_1", tok=tokens(30, 40, 4, 500, 0), cost=0.03, at=T0 + 3)
        add_part(conn, "prt_t", "msg_1", kind="text", text="SECRET PROMPT TEXT")
        add_part(conn, "prt_s", "msg_1", kind="step-start")

    return populate(build_db(tmp_path), fill)


def test_step_finish_parts_are_summed_not_the_overwritten_message_tokens(tmp_path: Path) -> None:
    events, warnings = parse_all(three_step_db(tmp_path))
    assert warnings == []
    assert len(events) == 3
    assert sum(e.tokens.uncached_input for e in events) == 60
    assert sum(e.tokens.cache_read for e in events) == 900
    assert sum(e.tokens.cache_write_5m for e in events) == 50
    assert sum(e.tokens.output for e in events) == (20 + 5) + 30 + (40 + 4)
    assert sum(e.tokens.reasoning_output for e in events) == 9
    assert sum(e.reported_cost or 0 for e in events) == pytest.approx(0.06)


def test_field_mapping_of_one_event(tmp_path: Path) -> None:
    events, _ = parse_all(three_step_db(tmp_path))
    first = next(e for e in events if e.request_id == "opencode:prt_1")
    assert first.tokens.uncached_input == 10  # input is exclusive of cache
    assert first.tokens.cache_read == 100
    assert first.tokens.cache_write_5m == 50
    assert first.tokens.output == 25  # output + reasoning
    assert first.tokens.reasoning_output == 5
    assert first.tokens.input_total == 160
    assert first.provider == "anthropic"
    assert first.model == "claude-sonnet-4-5"
    assert first.source == first.client == "opencode"
    assert first.session_id == "ses_1"
    assert first.project == "demo"
    assert first.working_directory == "/work/demo"
    assert first.title == "Demo"
    assert first.title_source == "tool"
    assert first.is_sidechain is False
    assert first.reported_cost == pytest.approx(0.01)
    assert first.timestamp.timestamp() == pytest.approx((T0 + 1) / 1000)


def test_text_content_never_reaches_events(tmp_path: Path) -> None:
    events, _ = parse_all(three_step_db(tmp_path))
    assert "SECRET PROMPT TEXT" not in "".join(e.model_dump_json() for e in events)


def test_message_without_step_finish_falls_back_to_message_tokens(tmp_path: Path) -> None:
    def fill(conn: sqlite3.Connection) -> None:
        add_session(conn)
        add_message(conn, "msg_a", msg_tokens=tokens(7, 3, 1, 20, 2), cost=0.5)
        add_message(conn, "msg_user", role="user", msg_tokens=tokens(999, 999))
        # in flight (not completed): skipped to avoid double counting once parts land
        add_message(conn, "msg_live", completed=None, msg_tokens=tokens(5, 5))

    events, _ = parse_all(populate(build_db(tmp_path), fill))
    assert [e.request_id for e in events] == ["opencode:msg:msg_a"]
    tok = events[0].tokens
    assert (tok.uncached_input, tok.cache_read, tok.cache_write_5m) == (7, 20, 2)
    assert (tok.output, tok.reasoning_output) == (4, 1)
    assert events[0].reported_cost == pytest.approx(0.5)


def test_message_with_parts_is_not_also_counted_at_message_level(tmp_path: Path) -> None:
    events, _ = parse_all(three_step_db(tmp_path))
    assert not any(e.request_id.startswith("opencode:msg:") for e in events)


def test_compaction_summary_message_is_counted(tmp_path: Path) -> None:
    def fill(conn: sqlite3.Connection) -> None:
        add_session(conn)
        add_message(conn, "msg_c", extra={"summary": True})
        add_part(conn, "prt_c", "msg_c", tok=tokens(100, 10), cost=0.002)

    events, _ = parse_all(populate(build_db(tmp_path), fill))
    assert len(events) == 1 and events[0].tokens.output == 10


def test_child_session_is_sidechain_and_placeholder_title_falls_back(tmp_path: Path) -> None:
    def fill(conn: sqlite3.Connection) -> None:
        add_session(conn, "ses_p", title="Real title")
        add_session(conn, "ses_c", parent="ses_p", title="Child session - 2026-10-01T00:00")
        add_message(conn, "m1", "ses_c")
        add_part(conn, "p1", "m1", "ses_c", tok=tokens(1, 1))

    events, _ = parse_all(populate(build_db(tmp_path), fill))
    assert events[0].is_sidechain is True
    assert events[0].title_source == "folder"
    assert events[0].title == "demo_ses_c"


def test_zero_token_zero_cost_step_is_skipped_but_cost_only_step_kept(tmp_path: Path) -> None:
    def fill(conn: sqlite3.Connection) -> None:
        add_session(conn)
        add_message(conn, "m1")
        add_part(conn, "p0", "m1", tok=tokens(0, 0), cost=0)
        add_part(conn, "p1", "m1", tok=tokens(0, 0), cost=0.01)

    events, _ = parse_all(populate(build_db(tmp_path), fill))
    assert [e.request_id for e in events] == ["opencode:p1"]


def test_missing_model_stays_none(tmp_path: Path) -> None:
    def fill(conn: sqlite3.Connection) -> None:
        add_session(conn)
        add_message(conn, "m1", model=None, provider=None)
        add_part(conn, "p1", "m1", tok=tokens(5, 5))

    events, _ = parse_all(populate(build_db(tmp_path), fill))
    assert events[0].model is None and events[0].provider is None


def test_provider_and_model_are_not_joined(tmp_path: Path) -> None:
    def fill(conn: sqlite3.Connection) -> None:
        add_session(conn)
        add_message(conn, "m1", model="anthropic/claude-sonnet-4.5", provider="openrouter")
        add_part(conn, "p1", "m1", tok=tokens(5, 5))

    events, _ = parse_all(populate(build_db(tmp_path), fill))
    assert (events[0].provider, events[0].model) == ("openrouter", "anthropic/claude-sonnet-4.5")


def test_malformed_json_rows_do_not_crash(tmp_path: Path) -> None:
    def fill(conn: sqlite3.Connection) -> None:
        add_session(conn)
        add_message(conn, "m1")
        add_part(conn, "p1", "m1", tok=tokens(5, 5))
        conn.execute(
            "INSERT INTO part (id, message_id, session_id, data) "
            "VALUES ('bad', 'm1', 'ses_1', '{oops')"
        )

    events, warnings = parse_all(populate(build_db(tmp_path), fill))
    assert [e.request_id for e in events] == ["opencode:p1"]
    assert sum("malformed JSON" in w and "1 rows" in w for w in warnings) == 1


def test_negative_token_fields_are_clamped_to_zero(tmp_path: Path) -> None:
    def fill(conn: sqlite3.Connection) -> None:
        add_session(conn)
        add_message(conn, "m1")
        add_part(conn, "p1", "m1", tok=tokens(-500, -3, -2, 100, -7))

    tok = parse_all(populate(build_db(tmp_path), fill))[0][0].tokens
    assert (tok.uncached_input, tok.cache_read, tok.cache_write_5m) == (0, 100, 0)
    assert (tok.output, tok.reasoning_output, tok.total) == (0, 0, 100)


def test_db_and_wal_pass_parse_the_database_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from ai_usage_cost.sources import opencode

    path = three_step_db(tmp_path)
    (tmp_path / "opencode.db-wal").write_bytes(b"")
    calls: list[Path] = []
    real = opencode._parse_db
    monkeypatch.setattr(opencode, "_parse_db", lambda db, *a: (calls.append(db), real(db, *a))[1])
    opencode._MEMO.clear()
    events, _ = parse_all(path)
    assert len(events) == 6 and len(calls) == 1


def test_non_numeric_token_values_count_as_zero(tmp_path: Path) -> None:
    def fill(conn: sqlite3.Connection) -> None:
        add_session(conn)
        add_message(conn, "m1")
        add_part(conn, "p1", "m1", tok={"input": "x", "output": 5, "cache": None})

    events, _ = parse_all(populate(build_db(tmp_path), fill))
    assert events[0].tokens.uncached_input == 0 and events[0].tokens.output == 5


def test_missing_session_columns_degrade_without_exception(tmp_path: Path) -> None:
    schema = """
    CREATE TABLE session (id TEXT PRIMARY KEY);
    CREATE TABLE message (id TEXT PRIMARY KEY, session_id TEXT, data TEXT);
    CREATE TABLE part (id TEXT PRIMARY KEY, message_id TEXT, data TEXT);
    """

    def fill(conn: sqlite3.Connection) -> None:
        conn.execute("INSERT INTO session (id) VALUES ('ses_1')")
        add_message_no_time(conn)

    def add_message_no_time(conn: sqlite3.Connection) -> None:
        data = json.dumps({"role": "assistant", "modelID": "m", "providerID": "p"})
        conn.execute("INSERT INTO message (id, session_id, data) VALUES ('m1','ses_1',?)", (data,))
        part = json.dumps({"type": "step-finish", "tokens": tokens(5, 5), "cost": 0.1})
        conn.execute("INSERT INTO part (id, message_id, data) VALUES ('p1','m1',?)", (part,))

    path = populate(build_db(tmp_path, schema=schema), fill)
    events, warnings = parse_all(path)
    assert warnings == []
    assert len(events) == 1
    assert events[0].project is None
    assert events[0].title_source == "folder"
    assert events[0].is_sidechain is False


def test_missing_part_table_uses_message_level_with_warning(tmp_path: Path) -> None:
    schema = SCHEMA.split("CREATE TABLE part")[0]

    def fill(conn: sqlite3.Connection) -> None:
        add_session(conn)
        add_message(conn, "m1", msg_tokens=tokens(5, 5), cost=0.2)

    events, warnings = parse_all(populate(build_db(tmp_path, schema=schema), fill))
    assert len(events) == 1
    assert any("`part`" in w for w in warnings)


def test_unsupported_schema_warns_and_yields_nothing(tmp_path: Path) -> None:
    path = tmp_path / "opencode.db"
    sqlite3.connect(path).close()
    events, warnings = parse_all(path)
    assert events == []
    assert any("message" in w for w in warnings)


def test_not_a_database_warns_instead_of_raising(tmp_path: Path) -> None:
    path = tmp_path / "opencode.db"
    path.write_bytes(b"not sqlite at all" * 50)
    events, warnings = parse_all(path)
    assert events == [] and warnings


def test_session_total_drift_emits_warning(tmp_path: Path) -> None:
    def fill(conn: sqlite3.Connection) -> None:
        add_session(conn, totals=(100_000, 5_000, 0, 0, 0))
        add_message(conn, "m1")
        add_part(conn, "p1", "m1", tok=tokens(100, 50))

    _, warnings = parse_all(populate(build_db(tmp_path), fill))
    assert any("session ses_1" in w for w in warnings)


def test_session_totals_matching_requests_do_not_warn(tmp_path: Path) -> None:
    events, warnings = parse_all(
        populate(
            build_db(tmp_path),
            lambda c: (
                add_session(c, totals=(1_000, 400, 100, 0, 0)),
                add_message(c, "m1"),
                add_part(c, "p1", "m1", tok=tokens(1_000, 300, 100)),
            ),
        )
    )
    assert len(events) == 1 and warnings == []


def test_reparse_is_idempotent_by_request_id(tmp_path: Path) -> None:
    from ai_usage_cost import store

    path = three_step_db(tmp_path)
    first, _ = parse_all(path)
    second, _ = parse_all(path)
    assert [store.fingerprint_of(e) for e in first] == [store.fingerprint_of(e) for e in second]
    assert len({store.fingerprint_of(e) for e in first}) == 3


def test_files_returns_db_channel_dbs_and_wal_but_not_shm(tmp_path: Path) -> None:
    for name in ("opencode.db", "opencode-beta.db", "opencode.db-wal", "opencode.db-shm", "x.db"):
        (tmp_path / name).write_bytes(b"")
    names = [p.name for p in SOURCE.files(tmp_path)]
    assert names == ["opencode-beta.db", "opencode.db", "opencode.db-wal"]
    assert [p.name for p in SOURCE.files(tmp_path / "opencode.db")] == [
        "opencode.db",
        "opencode.db-wal",
    ]
    assert make_files("kilo")(tmp_path) == []
    assert SOURCE.files(tmp_path / "missing") == []


def test_wal_path_parse_reads_the_main_database(tmp_path: Path) -> None:
    path = three_step_db(tmp_path)
    wal = tmp_path / "opencode.db-wal"
    wal.write_bytes(b"")
    events = list(SOURCE.parse(wal, []))
    assert len(events) == 3
    assert {e.source_file for e in events} == {str(path)}


def test_live_wal_changes_are_picked_up_on_next_ingest(tmp_path: Path) -> None:
    from ai_usage_cost import store

    path = three_step_db(tmp_path)
    writer = sqlite3.connect(path)
    writer.execute("PRAGMA journal_mode=WAL")
    writer.commit()
    writer.execute("PRAGMA wal_autocheckpoint=0")
    conn = store.open_store(tmp_path / "s.db")
    first = store.ingest(conn, [SOURCE], {"opencode": [path]})
    assert first.files_parsed >= 1
    add_part(writer, "prt_new", "msg_1", tok=tokens(1, 1), at=T0 + 9)
    writer.commit()
    try:
        store.ingest(conn, [SOURCE], {"opencode": [path]})
        events, _, _ = store.load(conn)
        assert len(events) == 4
    finally:
        writer.close()
        conn.close()


def test_default_roots_env_override_and_xdg(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("OPENCODE_DB", str(tmp_path / "custom.db"))
    assert SOURCE.default_roots() == [tmp_path / "custom.db"]
    monkeypatch.delenv("OPENCODE_DB")
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "xdg"))
    monkeypatch.setenv("APPDATA", str(tmp_path / "roaming"))
    roots = SOURCE.default_roots()
    assert roots[0] == tmp_path / "xdg" / "opencode"
    assert all(r.name == "opencode" for r in roots)


def test_missing_root_yields_no_events_and_no_exception(tmp_path: Path) -> None:
    events, warnings = parse_all(tmp_path / "nope" / "opencode.db")
    assert events == [] and warnings == []
    assert list(SOURCE.parse(tmp_path / "nope" / "opencode.db", [])) == []


def test_source_metadata_and_discovery() -> None:
    assert SOURCE.experimental is True
    assert SOURCE.token_data == "full"
    assert registry()["opencode"] is SOURCE
    assert "opencode" in registry()["opencode"].clients


def test_end_to_end_priced_through_analyze(tmp_path: Path) -> None:
    analysis = analyze_roots(tmp_path, opencode=three_step_db(tmp_path))
    events = [p for p in analysis.events if p.event.source == "opencode"]
    assert len(events) == 3
    assert all(p.state == "priced" and p.cost is not None for p in events)
    assert sum(p.event.reported_cost or 0 for p in events) == pytest.approx(0.06)


def test_end_to_end_unknown_model_does_not_crash(tmp_path: Path) -> None:
    def fill(conn: sqlite3.Connection) -> None:
        add_session(conn)
        add_message(conn, "m1", model="totally-unknown-model-9", provider="acme")
        add_part(conn, "p1", "m1", tok=tokens(10, 10), cost=0.01)

    analysis = analyze_roots(tmp_path, opencode=populate(build_db(tmp_path), fill))
    events = [p for p in analysis.events if p.event.source == "opencode"]
    assert len(events) == 1 and events[0].state != "priced"
