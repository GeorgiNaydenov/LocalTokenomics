from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_usage_cost import store
from ai_usage_cost.models import UsageEvent
from ai_usage_cost.pipeline import analyze
from ai_usage_cost.sources import registry
from ai_usage_cost.sources.qwen_code import SOURCE, default_roots, parse, session_files, spans
from conftest import FIXTURES, NO_ROOT

BASIC = FIXTURES / "qwen_code" / "basic" / "projects"


def scan(root: Path) -> tuple[list[UsageEvent], list[str]]:
    warnings: list[str] = []
    events: list[UsageEvent] = []
    for path in session_files(root):
        events.extend(parse(path, warnings))
    return events, warnings


def assistant(uuid: str, usage: dict | None, **extra: object) -> dict:
    record: dict = {
        "uuid": uuid,
        "sessionId": "s1",
        "timestamp": "2026-09-30T10:00:04.000Z",
        "type": "assistant",
        "cwd": "/work/demo",
        "model": "qwen3-coder-plus",
    }
    if usage is not None:
        record["usageMetadata"] = usage
    record.update(extra)
    return record


def write(tmp_path: Path, lines: list[object], raw_tail: str = "") -> Path:
    chats = tmp_path / "projects" / "c--work-demo" / "chats"
    chats.mkdir(parents=True, exist_ok=True)
    path = chats / "s1.jsonl"
    path.write_text(
        "\n".join(json.dumps(line) for line in lines) + "\n" + raw_tail, encoding="utf-8"
    )
    return path


def usage(prompt: int, cand: int, cached: int, thoughts: int, total: int) -> dict:
    return {
        "promptTokenCount": prompt,
        "candidatesTokenCount": cand,
        "cachedContentTokenCount": cached,
        "thoughtsTokenCount": thoughts,
        "totalTokenCount": total,
    }


def test_basic_fixture_counts_assistant_records_only() -> None:
    events, warnings = scan(BASIC)
    assert warnings == []
    assert len(events) == 2  # the ui_telemetry duplicate is not counted
    main, side = events
    assert main.tokens is not None and side.tokens is not None
    assert (main.tokens.uncached_input, main.tokens.cache_read) == (2000, 6000)
    assert (main.tokens.output, main.tokens.reasoning_output) == (520, 120)
    assert main.model == "qwen3-coder-plus" and main.provider is None
    assert main.project == "demo" and main.working_directory == "/work/demo"
    assert main.branch == "main" and not main.is_sidechain and side.is_sidechain
    assert main.title == "Demo" and main.title_source == "tool"
    assert main.request_id == "qwen-code:s-0001:u2"
    assert main.client == "qwen-code"


def test_openai_compatible_candidates_already_include_reasoning(tmp_path: Path) -> None:
    write(tmp_path, [assistant("a", usage(1000, 300, 200, 100, 1300))])
    events, warnings = scan(tmp_path / "projects")
    (event,) = events
    assert event.tokens is not None
    assert event.tokens.output == 300 and event.tokens.reasoning_output == 100
    assert event.tokens.uncached_input == 800 and warnings == []


def test_gemini_native_thoughts_added(tmp_path: Path) -> None:
    write(tmp_path, [assistant("a", usage(1000, 300, 0, 100, 1400))])
    (event,), _ = scan(tmp_path / "projects")
    assert event.tokens is not None and event.tokens.output == 400


def test_unreconciled_total_ignores_thoughts_and_warns(tmp_path: Path) -> None:
    write(tmp_path, [assistant("a", usage(1000, 300, 0, 100, 9999))])
    (event,), warnings = scan(tmp_path / "projects")
    assert event.tokens is not None and event.tokens.output == 300
    assert any("reconcile" in w for w in warnings)


def test_dedup_by_uuid_last_wins_and_last_title(tmp_path: Path) -> None:
    title = {"uuid": "t", "type": "system", "subtype": "custom_title"}
    write(
        tmp_path,
        [
            assistant("a", usage(100, 10, 0, 0, 110)),
            assistant("a", usage(100, 20, 0, 0, 120)),
            {**title, "systemPayload": {"customTitle": "first"}},
            {**title, "systemPayload": {"customTitle": "second"}},
        ],
    )
    (event,), _ = scan(tmp_path / "projects")
    assert event.tokens is not None and event.tokens.output == 20
    assert event.title == "second"


def test_missing_keys_malformed_lines_and_no_model(tmp_path: Path) -> None:
    write(
        tmp_path,
        [
            assistant("a", None),
            {"type": "assistant", "usageMetadata": {"promptTokenCount": 5}},
            {"type": "assistant", "usageMetadata": "bad"},
        ],
        raw_tail='{"uuid":"x","type":"assi',
    )
    events, warnings = scan(tmp_path / "projects")
    assert len(events) == 1 and events[0].model is None
    assert events[0].session_id == "s1" and events[0].title_source == "folder"
    assert any("unparsable" in w for w in warnings)


def test_spans_carry_measured_context_capacity() -> None:
    (path,) = session_files(BASIC)
    found = list(spans(path, []))
    assert [s.kind for s in found] == ["model_call", "model_call"]
    assert all(s.context_capacity == 1_000_000 for s in found)
    assert all(s.capacity_provenance == "measured" for s in found)
    assert found[1].is_sidechain and found[0].tokens is not None


def test_missing_root_and_env_precedence(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    assert session_files(tmp_path / "nope") == []
    monkeypatch.delenv("QWEN_RUNTIME_DIR", raising=False)
    monkeypatch.setenv("QWEN_HOME", str(tmp_path / "home"))
    assert default_roots() == [tmp_path / "home" / "projects"]
    monkeypatch.setenv("QWEN_RUNTIME_DIR", str(tmp_path / "rt"))
    assert default_roots() == [tmp_path / "rt" / "projects"]


def test_reparse_is_idempotent_through_the_store(tmp_path: Path) -> None:
    write(tmp_path, [assistant("a", usage(100, 10, 0, 0, 110))])
    first, _ = scan(tmp_path / "projects")
    second, _ = scan(tmp_path / "projects")
    assert [store.fingerprint_of(e) for e in first] == [store.fingerprint_of(e) for e in second]


def test_source_is_experimental_and_discovered() -> None:
    assert SOURCE.experimental is True
    assert "qwen-code" in registry()


def test_pipeline_unknown_model_does_not_crash_and_spans_stored(tmp_path: Path) -> None:
    write(tmp_path, [assistant("a", usage(100, 10, 0, 0, 110), contextWindowSize=262144)])
    roots = {sid: [NO_ROOT] for sid in registry()}
    roots["qwen-code"] = [tmp_path / "projects"]
    found = analyze(db_path=tmp_path / "u.db", roots=roots)
    (priced,) = [p for p in found.events if p.event.source == "qwen-code"]
    assert priced.state in {"priced", "free", "unpriced"}
    conn = store.open_store(tmp_path / "u.db")
    try:
        assert len(store.load_spans(conn, "qwen-code", "s1")) == 1
    finally:
        conn.close()


def test_negative_token_fields_clamp_to_zero(tmp_path: Path) -> None:
    write(tmp_path, [assistant("a", usage(-50, 10, -5, -3, 7))])
    (event,), _ = scan(tmp_path / "projects")
    assert event.tokens is not None
    assert event.tokens.uncached_input == 0 and event.tokens.cache_read == 0
    assert event.tokens.output == 10 and event.tokens.reasoning_output == 0


def test_unreconciled_totals_warn_once_per_file(tmp_path: Path) -> None:
    write(tmp_path, [assistant(f"a{i}", usage(1000, 300, 0, 100, 9999)) for i in range(5)])
    events, warnings = scan(tmp_path / "projects")
    assert len(events) == 5
    assert len(warnings) == 1 and "5 records" in warnings[0]
