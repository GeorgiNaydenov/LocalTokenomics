from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_usage_cost import store
from ai_usage_cost.models import UsageEvent
from ai_usage_cost.pipeline import analyze
from ai_usage_cost.sources import registry
from ai_usage_cost.sources.gemini_cli import SOURCE, default_roots, parse, session_files
from conftest import FIXTURES, NO_ROOT

BASIC = FIXTURES / "gemini_cli" / "basic" / "tmp"
META = {
    "sessionId": "sess-1",
    "kind": "main",
    "directories": ["/work/demo"],
    "startTime": "2026-09-30T10:00:00.000Z",
}


def scan(root: Path) -> tuple[list[UsageEvent], list[str]]:
    warnings: list[str] = []
    events: list[UsageEvent] = []
    for path in session_files(root):
        events.extend(parse(path, warnings))
    return events, warnings


def gemini(mid: str, tokens: dict | None, model: str = "gemini-2.5-pro") -> dict:
    return {
        "id": mid,
        "timestamp": "2026-09-30T10:00:05.000Z",
        "type": "gemini",
        "model": model,
        "tokens": tokens,
    }


def write(tmp_path: Path, lines: list[object], name: str = "session-x.jsonl") -> Path:
    chats = tmp_path / "tmp" / "demo" / "chats"
    chats.mkdir(parents=True, exist_ok=True)
    path = chats / name
    path.write_text("\n".join(json.dumps(line) for line in lines) + "\n", encoding="utf-8")
    return path


def one(tmp_path: Path, tokens: dict) -> UsageEvent:
    write(tmp_path, [META, gemini("m1", tokens)])
    events, _ = scan(tmp_path / "tmp")
    assert len(events) == 1
    return events[0]


def test_basic_fixture_totals_and_metadata() -> None:
    events, warnings = scan(BASIC)
    assert warnings == []
    main = [e for e in events if not e.is_sidechain]
    # m2 is re-emitted (first without tokens, then with): counted once; m3 was rewound but
    # still billed, so it is counted too.
    assert [e.request_id for e in main] == [
        "gemini-cli:a1b2c3d4-0000-4000-8000-000000000001:m2",
        "gemini-cli:a1b2c3d4-0000-4000-8000-000000000001:m3",
    ]
    first, rewound = main
    assert first.tokens is not None and rewound.tokens is not None
    assert (first.tokens.uncached_input, first.tokens.cache_read) == (3000, 9000)
    assert (first.tokens.output, first.tokens.reasoning_output) == (450, 150)
    # m3: total reconciles with tool (5000+100+200), so tool joins the uncached input
    assert rewound.tokens.uncached_input == 5200
    assert first.provider == "google" and first.model == "gemini-2.5-pro"
    assert first.client == "gemini-cli" and first.source == "gemini-cli"
    assert first.title == "Demo session" and first.title_source == "tool"
    # projects.json reverse lookup wins over metadata directories
    assert first.project == "demo" and first.working_directory == "/work/demo"
    assert first.timestamp.isoformat() == "2026-09-30T10:15:09+00:00"


def test_subagent_file_is_sidechain() -> None:
    events, _ = scan(BASIC)
    (sub,) = [e for e in events if e.is_sidechain]
    assert sub.session_id == "sub-0001" and sub.model == "gemini-2.5-flash"


def test_tool_added_only_when_total_reconciles(tmp_path: Path) -> None:
    good = {"input": 1000, "cached": 0, "output": 10, "thoughts": 5, "tool": 40, "total": 1055}
    ok = one(tmp_path, good)
    assert ok.tokens is not None and ok.tokens.uncached_input == 1040
    bad = one(tmp_path / "b", {**good, "total": 1015})
    assert bad.tokens is not None and bad.tokens.uncached_input == 1000


def test_inclusive_cached_never_negative(tmp_path: Path) -> None:
    event = one(tmp_path, {"input": 100, "cached": 500, "output": 1, "total": 101})
    assert event.tokens is not None
    assert event.tokens.uncached_input == 0 and event.tokens.cache_read == 100


def test_null_tokens_skipped_and_missing_keys_tolerated(tmp_path: Path) -> None:
    write(
        tmp_path,
        [META, gemini("m1", None), {"id": "m2", "type": "gemini", "tokens": {}}, ["not a dict"]],
    )
    events, _ = scan(tmp_path / "tmp")
    assert events == []


def test_title_falls_back_to_folder_and_session_to_filename(tmp_path: Path) -> None:
    write(tmp_path, [gemini("m1", {"input": 10, "output": 1, "cached": 0, "total": 11})])
    (event,) = scan(tmp_path / "tmp")[0]
    assert event.session_id == "session-x" and event.title_source == "folder"
    assert event.project == "demo"  # slug fallback


def test_project_root_marker(tmp_path: Path) -> None:
    path = write(
        tmp_path, [{"sessionId": "s"}, gemini("m1", {"input": 10, "output": 1, "total": 11})]
    )
    (path.parent.parent / ".project_root").write_text("/srv/markerproj\n", encoding="utf-8")
    (event,) = scan(tmp_path / "tmp")[0]
    assert event.project == "markerproj"


def test_set_messages_checkpoint_and_last_summary_wins(tmp_path: Path) -> None:
    write(
        tmp_path,
        [
            META,
            {"$set": {"summary": "one"}},
            {"$set": {"messages": [gemini("m1", {"input": 10, "output": 1, "total": 11})]}},
            {"$set": {"summary": "two"}},
        ],
    )
    (event,) = scan(tmp_path / "tmp")[0]
    assert event.title == "two"


def test_malformed_and_truncated_lines_warn(tmp_path: Path) -> None:
    path = write(tmp_path, [META, gemini("m1", {"input": 10, "output": 1, "total": 11})])
    with path.open("a", encoding="utf-8") as handle:
        handle.write('{"id":"m2","type":"gem')
    events, warnings = scan(tmp_path / "tmp")
    assert len(events) == 1 and any("unparsable" in w for w in warnings)


def test_legacy_whole_file_json(tmp_path: Path) -> None:
    chats = tmp_path / "tmp" / "demo" / "chats"
    chats.mkdir(parents=True)
    doc = {
        **META,
        "summary": "Old",
        "messages": [gemini("m1", {"input": 10, "output": 1, "total": 11})],
    }
    (chats / "session-old.json").write_text(json.dumps(doc), encoding="utf-8")
    (event,) = scan(tmp_path / "tmp")[0]
    assert event.session_id == "sess-1" and event.title == "Old"


def test_files_ignore_unrelated_antigravity_data(tmp_path: Path) -> None:
    tmp = tmp_path / ".gemini" / "tmp"
    (tmp_path / ".gemini" / "antigravity" / "brain").mkdir(parents=True)
    (tmp_path / ".gemini" / "antigravity" / "brain" / "session-1.jsonl").write_text("{}\n")
    (tmp / "demo").mkdir(parents=True)
    (tmp / "demo" / "notes.jsonl").write_text("{}\n")
    assert session_files(tmp) == []
    assert session_files(tmp_path / ".gemini") == []
    assert session_files(tmp_path / "missing") == []


def test_env_override(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("GEMINI_CLI_HOME", str(tmp_path))
    assert default_roots()[0] == tmp_path / ".gemini" / "tmp"


def test_reparse_is_idempotent_through_the_store(tmp_path: Path) -> None:
    write(tmp_path, [META, gemini("m1", {"input": 10, "output": 1, "total": 11})])
    events, _ = scan(tmp_path / "tmp")
    again, _ = scan(tmp_path / "tmp")
    assert [store.fingerprint_of(e) for e in events] == [store.fingerprint_of(e) for e in again]
    assert len({store.fingerprint_of(e) for e in events}) == len(events)


def test_source_is_experimental_and_discovered() -> None:
    assert SOURCE.experimental is True
    assert "gemini-cli" in registry()


def test_pipeline_prices_known_model_and_survives_unknown(tmp_path: Path) -> None:
    write(
        tmp_path,
        [
            META,
            gemini("m1", {"input": 1000, "cached": 0, "output": 100, "total": 1100}),
            gemini("m2", {"input": 1000, "cached": 0, "output": 100, "total": 1100}, "mystery-9"),
        ],
    )
    roots = {sid: [NO_ROOT] for sid in registry()}
    roots["gemini-cli"] = [tmp_path / "tmp"]
    found = analyze(db_path=tmp_path / "u.db", roots=roots)
    states = {p.event.model: p.state for p in found.events if p.event.source == "gemini-cli"}
    assert states["gemini-2.5-pro"] == "priced"
    assert states["mystery-9"] == "unpriced"


def test_negative_token_fields_clamp_to_zero(tmp_path: Path) -> None:
    event = one(tmp_path, {"input": -50, "cached": -5, "output": 10, "thoughts": -3, "total": 7})
    assert event.tokens is not None
    assert event.tokens.uncached_input == 0 and event.tokens.cache_read == 0
    assert event.tokens.output == 10 and event.tokens.reasoning_output == 0


def test_id_less_identical_lines_dedup(tmp_path: Path) -> None:
    line = {
        "timestamp": "2026-09-30T10:00:05.000Z",
        "type": "gemini",
        "tokens": {"input": 10, "output": 1, "total": 11},
    }
    other = {**line, "tokens": {"input": 20, "output": 1, "total": 21}}
    write(tmp_path, [META, line, line, other])
    events, _ = scan(tmp_path / "tmp")
    assert len(events) == 2
