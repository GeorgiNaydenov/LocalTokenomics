from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from ai_usage_cost import store
from ai_usage_cost.models import UsageEvent
from ai_usage_cost.pipeline import analyze
from ai_usage_cost.sources import cline, kilo_legacy, registry, roo_code
from ai_usage_cost.sources.base import Source, scan
from conftest import FIXTURES

CLINE = FIXTURES / "cline"
CLINE_TASKS = CLINE / "cline" / "tasks"
ROO_TASKS = CLINE / "roo" / "tasks"
KILO_TASKS = CLINE / "kilo" / "tasks"
SDK_SESSIONS = CLINE / "sdk" / "sessions"


def run(source: Source, root: Path) -> tuple[list[UsageEvent], list[str]]:
    events: list[UsageEvent] = []
    warnings: list[str] = []
    for _path, found, _spans, warns in scan(source, [root]):
        events.extend(found)
        warnings.extend(warns)
    return events, warnings


def rid(event: UsageEvent) -> str:
    assert event.request_id is not None
    return event.request_id


def tokens_of(event: UsageEvent):
    assert event.tokens is not None
    return event.tokens


def task_file(root: Path, task: str, items: list, history: dict | None = None) -> Path:
    task_dir = root / "tasks" / task
    task_dir.mkdir(parents=True)
    path = task_dir / "ui_messages.json"
    path.write_text(json.dumps(items), encoding="utf-8")
    if history is not None:
        (task_dir / "history_item.json").write_text(json.dumps(history), encoding="utf-8")
    return path


def req(ts: int, say: str = "api_req_started", **usage: object) -> dict:
    return {"ts": ts, "type": "say", "say": say, "text": json.dumps(usage)}


# --- registration -----------------------------------------------------------------------


def test_sources_registered_and_experimental() -> None:
    sources = registry()
    for source_id in ("cline", "roo-code", "kilo-code-legacy"):
        assert source_id in sources
        assert sources[source_id].experimental is True
        assert sources[source_id].token_data == "full"
    assert sources["roo-code"].clients == {"roo-code": "Roo Code"}
    assert sources["kilo-code-legacy"].clients == {"kilo-code-legacy": "Kilo Code (legacy)"}
    assert cline.SOURCE.clients == {"cline": "Cline"}


# --- Cline legacy -----------------------------------------------------------------------


def test_cline_legacy_counted_records_and_skips() -> None:
    events, warnings = run(cline.SOURCE, CLINE_TASKS)
    assert warnings == []
    # the placeholder (no cost/cancelReason) and the partial entry are skipped
    assert sorted(rid(e) for e in events) == [
        "cline:task-c1:1790000001000",
        "cline:task-c1:1790000004000",
        "cline:task-c1:1790000005000:deleted_api_reqs",
        "cline:task-c1:1790000006000:subagent_usage",
        "cline:task-c1:1790000007000",
    ]


def test_cline_legacy_tokens_exclusive_policy_and_cost() -> None:
    events, _ = run(cline.SOURCE, CLINE_TASKS)
    first = next(e for e in events if rid(e) == "cline:task-c1:1790000001000")
    tokens = tokens_of(first)
    assert tokens.uncached_input == 3200  # exclusive: tokensIn taken as-is
    assert tokens.cache_read == 15000
    assert tokens.cache_write_5m == 2000
    assert tokens.output == 410
    assert first.reported_cost == pytest.approx(0.0431)
    assert first.model == "claude-sonnet-4-5"
    assert first.provider == "anthropic"
    assert first.session_id == "task-c1"
    assert first.timestamp.isoformat() == "2026-09-21T14:13:21+00:00"
    assert first.project == "clinedemo"
    assert first.working_directory == "/work/clinedemo"
    assert first.is_sidechain is False
    assert first.title == "clinedemo_task-c1"
    assert first.title_source == "folder"


def test_cancelled_request_without_cost_is_counted() -> None:
    events, _ = run(cline.SOURCE, CLINE_TASKS)
    cancelled = next(e for e in events if rid(e) == "cline:task-c1:1790000004000")
    assert tokens_of(cancelled).uncached_input == 500
    assert cancelled.reported_cost is None


def test_deleted_api_reqs_and_subagent_usage_counted() -> None:
    events, _ = run(cline.SOURCE, CLINE_TASKS)
    deleted = next(e for e in events if rid(e).endswith(":deleted_api_reqs"))
    sub = next(e for e in events if rid(e).endswith(":subagent_usage"))
    assert tokens_of(deleted).uncached_input == 1000
    assert deleted.is_sidechain is False
    assert sub.is_sidechain is True
    assert sub.reported_cost == pytest.approx(0.007)


def test_model_falls_back_to_nearest_earlier_task_metadata_entry() -> None:
    events, _ = run(cline.SOURCE, CLINE_TASKS)
    deleted = next(e for e in events if rid(e).endswith(":deleted_api_reqs"))
    assert deleted.model == "claude-opus-4-1"
    last = next(e for e in events if rid(e) == "cline:task-c1:1790000007000")
    assert (last.model, last.provider) == ("gpt-5", "openai")


def test_request_text_never_leaks() -> None:
    events, warnings = run(cline.SOURCE, CLINE_TASKS)
    blob = json.dumps([e.model_dump(mode="json") for e in events]) + " ".join(warnings)
    assert "SYNTHETIC" not in blob


def test_partial_entries_skipped(tmp_path: Path) -> None:
    items = [{**req(1, tokensIn=5, cost=0.1), "partial": True}, req(2, tokensIn=7, cost=0.1)]
    task_file(tmp_path, "t", items)
    events, _ = run(cline.SOURCE, tmp_path / "tasks")
    assert [rid(e) for e in events] == ["cline:t:2"]


def test_bad_json_text_and_missing_keys_do_not_crash(tmp_path: Path) -> None:
    items = [
        {"ts": 1, "type": "say", "say": "api_req_started", "text": "{not json"},
        {"ts": 2, "type": "say", "say": "api_req_started"},
        {"ts": 3, "type": "say", "say": "api_req_started", "text": "[1, 2]"},
        "junk",
        {"type": "ask", "ask": "tool"},
        req(4, tokensIn="many", tokensOut=2, cost=0.01),
    ]
    task_file(tmp_path, "t", items)
    events, warnings = run(cline.SOURCE, tmp_path / "tasks")
    assert len(events) == 1
    assert tokens_of(events[0]).uncached_input == 0
    assert tokens_of(events[0]).output == 2
    assert any("unparsable usage" in w for w in warnings)


def test_duplicate_task_and_timestamp_emitted_once(tmp_path: Path) -> None:
    task_file(tmp_path, "t", [req(9, tokensIn=1, cost=0.1), req(9, tokensIn=2, cost=0.2)])
    events, _ = run(cline.SOURCE, tmp_path / "tasks")
    assert len(events) == 1
    assert tokens_of(events[0]).uncached_input == 1


def test_truncated_array_is_salvaged_with_warning(tmp_path: Path) -> None:
    path = task_file(tmp_path, "t", [req(1, tokensIn=5, cost=0.1), req(2, tokensIn=6, cost=0.1)])
    text = path.read_text(encoding="utf-8")
    path.write_text(text[: text.rindex("{") + 10], encoding="utf-8")
    events, warnings = run(cline.SOURCE, tmp_path / "tasks")
    assert [rid(e) for e in events] == ["cline:t:1"]
    assert any("truncated" in w for w in warnings)


def test_non_array_file_warns(tmp_path: Path) -> None:
    path = task_file(tmp_path, "t", [])
    path.write_text('{"a": 1}', encoding="utf-8")
    events, warnings = run(cline.SOURCE, tmp_path / "tasks")
    assert events == []
    assert any("expected a JSON array" in w for w in warnings)


def test_missing_root_yields_nothing(tmp_path: Path) -> None:
    for source in (cline.SOURCE, roo_code.SOURCE, kilo_legacy.SOURCE):
        assert list(scan(source, [tmp_path / "nope"])) == []


# --- inclusive vs exclusive policy ------------------------------------------------------


def test_inclusive_policy_subtracts_cache_and_clamps() -> None:
    inclusive = cline._tokens(1000, 10, 100, 400, inclusive=True)
    assert (inclusive.uncached_input, inclusive.cache_read, inclusive.cache_write_5m) == (
        500,
        400,
        100,
    )
    assert inclusive.total == 1010
    assert cline._tokens(100, 0, 100, 400, inclusive=True).uncached_input == 0


def test_exclusive_policy_keeps_tokens_in() -> None:
    exclusive = cline._tokens(1000, 10, 100, 400, inclusive=False)
    assert exclusive.uncached_input == 1000
    assert exclusive.total == 1510


def test_policy_table_per_source() -> None:
    assert cline._TOKENS_IN_INCLUSIVE == {
        "cline": False,
        "roo-code": True,
        "kilo-code-legacy": True,
    }


# --- Roo / Kilo -------------------------------------------------------------------------


def test_roo_inclusive_no_model_with_cost_and_subtask() -> None:
    events, warnings = run(roo_code.SOURCE, ROO_TASKS)
    assert warnings == []
    assert len(events) == 3
    main = next(e for e in events if rid(e) == "roo-code:task-r1:1790000001000")
    tokens = tokens_of(main)
    assert tokens.uncached_input == 18200 - 15000 - 2000
    assert tokens.cache_read == 15000
    assert tokens.cache_write_5m == 2000
    assert main.model is None
    assert main.provider is None
    assert main.reported_cost == pytest.approx(0.0431)
    assert main.client == "roo-code"
    assert main.project == "demo"
    assert main.is_sidechain is False
    child = next(e for e in events if e.session_id == "task-r2")
    assert child.is_sidechain is True


def test_kilo_legacy_source_and_policy() -> None:
    events, _ = run(kilo_legacy.SOURCE, KILO_TASKS)
    assert len(events) == 1
    event = events[0]
    assert event.source == "kilo-code-legacy"
    assert event.client == "kilo-code-legacy"
    assert tokens_of(event).uncached_input == 500
    assert event.model is None
    assert event.project == "kilodemo"


# --- discovery --------------------------------------------------------------------------


def test_lowercase_directory_names_matched(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(sys, "platform", "win32")
    monkeypatch.setenv("APPDATA", str(tmp_path))
    storage = tmp_path / "Code" / "User" / "globalStorage"
    (storage / "saoudrizwan.claude-dev").mkdir(parents=True)
    (storage / "RooVeterinaryInc.Roo-Cline").mkdir()
    assert cline.task_roots("SaoudRizwan.Claude-Dev") == [
        storage / "saoudrizwan.claude-dev" / "tasks"
    ]
    assert roo_code.default_roots() == [storage / "RooVeterinaryInc.Roo-Cline" / "tasks"]
    # nothing installed -> canonical path of the first variant, so the UI shows where we look
    assert kilo_legacy.default_roots() == [storage / "kilocode.kilo-code" / "tasks"]


def test_default_roots_linux_variants(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    monkeypatch.setenv("CLINE_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.delenv("CLINE_SESSION_DATA_DIR", raising=False)
    storages = [tmp_path / ".config" / v / "User" / "globalStorage" for v in ("Code", "Cursor")]
    for storage in storages:
        (storage / "saoudrizwan.claude-dev").mkdir(parents=True)
    roots = cline.cline_roots()
    assert roots == [
        storages[0] / "saoudrizwan.claude-dev" / "tasks",
        storages[1] / "saoudrizwan.claude-dev" / "tasks",
        tmp_path / "data" / "sessions",
    ]


def test_sdk_root_env_overrides(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("CLINE_SESSION_DATA_DIR", raising=False)
    monkeypatch.delenv("CLINE_DATA_DIR", raising=False)
    monkeypatch.setenv("CLINE_DIR", str(tmp_path / "d"))
    assert cline.sdk_sessions_root() == tmp_path / "d" / "data" / "sessions"
    monkeypatch.setenv("CLINE_DATA_DIR", str(tmp_path / "x"))
    assert cline.sdk_sessions_root() == tmp_path / "x" / "sessions"
    monkeypatch.setenv("CLINE_SESSION_DATA_DIR", str(tmp_path / "s"))
    assert cline.sdk_sessions_root() == tmp_path / "s"


def test_files_finds_task_and_sdk_files() -> None:
    assert [p.parent.name for p in cline.data_files(CLINE_TASKS)] == ["task-c1"]
    assert [p.name for p in cline.data_files(SDK_SESSIONS)] == [
        "sess_01.messages.json",
        "sess_legacy.messages.json",
        "sess_sub.messages.json",
    ]


# --- SDK store --------------------------------------------------------------------------


def test_sdk_messages_inclusive_with_manifest_fallbacks() -> None:
    events, warnings = run(cline.SOURCE, SDK_SESSIONS)
    assert warnings == []
    main = [e for e in events if e.session_id == "sess_01"]
    assert [rid(e) for e in main] == ["cline:sdk:sess_01:1", "cline:sdk:sess_01:2"]
    first, second = main
    tokens = tokens_of(first)
    assert tokens.uncached_input == 18200 - 15000 - 2000
    assert tokens.cache_read == 15000
    assert tokens.cache_write_5m == 2000
    assert tokens.output == 410
    assert first.reported_cost == pytest.approx(0.0431)
    assert (first.model, first.provider) == ("claude-sonnet-4-5", "anthropic")
    assert first.project == "sdkdemo"
    assert first.is_sidechain is False
    # no modelInfo on the message -> manifest model
    assert second.model == "claude-haiku-4-5"
    assert tokens_of(second).uncached_input == 500


def test_sdk_legacy_migrated_session_skipped_and_subagent_flagged() -> None:
    events, _ = run(cline.SOURCE, SDK_SESSIONS)
    assert not any(e.session_id == "sess_legacy" for e in events)
    sub = [e for e in events if e.session_id == "sess_sub"]
    assert sub
    assert all(e.is_sidechain for e in sub)


def test_sdk_bad_file_warns(tmp_path: Path) -> None:
    session = tmp_path / "s1"
    session.mkdir()
    (session / "s1.messages.json").write_text('{"messages": [', encoding="utf-8")
    events, warnings = run(cline.SOURCE, tmp_path)
    assert events == []
    assert any("SDK messages file" in w for w in warnings)


# --- store + pipeline -------------------------------------------------------------------


def test_reparse_is_idempotent_through_the_store(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    roots = {"cline": [CLINE_TASKS, SDK_SESSIONS]}
    store.ingest(conn, [cline.SOURCE], roots)
    count = conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
    assert count == 5 + 2 + 2
    store.ingest(conn, [cline.SOURCE], roots, rebuild=True)
    assert conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0] == count
    store.ingest(conn, [cline.SOURCE], roots)
    assert conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0] == count


def test_pipeline_prices_known_model_and_tolerates_unpriced(tmp_path: Path) -> None:
    roots = {
        "cline": [CLINE_TASKS],
        "roo-code": [ROO_TASKS],
        "kilo-code-legacy": [KILO_TASKS],
    }
    analysis = analyze(db_path=tmp_path / "usage.db", roots=roots)
    mine = [p for p in analysis.events if p.event.source in roots]
    assert len(mine) == 5 + 3 + 1
    priced = [p for p in mine if p.event.model == "claude-sonnet-4-5"]
    assert priced
    assert all(p.state == "priced" and p.cost is not None for p in priced)
    # Roo/Kilo log no model: never priced, tokens still counted, tool cost still carried
    roo = [p for p in mine if p.event.source == "roo-code"]
    assert all(p.state in ("unpriced", "unavailable") and p.cost is None for p in roo)
    assert sum(p.event.reported_cost or 0 for p in roo) == pytest.approx(0.0431 + 0.001 + 0.0005)


def test_negative_token_fields_are_clamped(tmp_path: Path) -> None:
    for inclusive in (True, False):
        tokens = cline._tokens(-50, -3, -7, -9, inclusive=inclusive)
        assert (
            min(tokens.uncached_input, tokens.cache_read, tokens.cache_write_5m, tokens.output) == 0
        )
        assert tokens.total == 0
    task_file(tmp_path, "t", [req(1, tokensIn=-100, tokensOut=4, cacheReads=-5, cost=0.1)])
    events, _ = run(cline.SOURCE, tmp_path / "tasks")
    tokens = tokens_of(events[0])
    assert (tokens.uncached_input, tokens.cache_read, tokens.output) == (0, 0, 4)
    assert tokens.total == 4
