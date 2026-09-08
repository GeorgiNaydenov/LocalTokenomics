from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from ai_usage_cost.models import UsageEvent
from ai_usage_cost.sources.grok_build import default_roots, parse, session_files
from conftest import GROK_BUILD_BASIC


@dataclass
class Scanned:
    events: list[UsageEvent] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def scan(root: Path) -> Scanned:
    result = Scanned()
    for path in session_files(root):
        result.events.extend(parse(path, result.warnings))
    return result


def write_session(
    tmp_path: Path,
    lines: list[dict],
    *,
    project: str = "%2Fhome%2Fuser%2Fproj",
    session: str = "session-1",
    summary: dict | None = None,
) -> Path:
    session_dir = tmp_path / project / session
    session_dir.mkdir(parents=True, exist_ok=True)
    updates = session_dir / "updates.jsonl"
    updates.write_text("\n".join(json.dumps(line) for line in lines) + "\n", encoding="utf-8")
    if summary is not None:
        (session_dir / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
    return updates


def turn(usage: dict, *, event_id: str = "evt-1", session_id: str | None = "session-1") -> dict:
    params: dict = {
        "update": {"sessionUpdate": "turn_completed", "usage": usage},
        "_meta": {"eventId": event_id},
    }
    if session_id is not None:
        params["sessionId"] = session_id
    return {"timestamp": 1755590000, "params": params}


@pytest.fixture
def basic() -> list[UsageEvent]:
    return scan(GROK_BUILD_BASIC).events


def test_basic_fixture_yields_only_turn_completed_events_with_nonzero_tokens(
    basic: list[UsageEvent],
) -> None:
    assert len(basic) == 4
    assert all(event.tokens.total > 0 for event in basic)
    assert all(event.source == "grok-build" for event in basic)
    assert all(event.client == "grok-build" for event in basic)


def test_cached_input_is_split_out_of_input_tokens(basic: list[UsageEvent]) -> None:
    tokens = basic[0].tokens
    assert tokens.cache_read == 15_000
    assert tokens.uncached_input == 20_000 - 15_000
    assert tokens.output == 800
    assert tokens.reasoning_output == 300


def test_top_level_usage_is_used_when_model_usage_map_is_absent(basic: list[UsageEvent]) -> None:
    top_level = basic[1]
    assert top_level.model == "grok-4.5-build"
    assert top_level.tokens.uncached_input == 1_000
    assert top_level.tokens.output == 50


def test_cache_creation_tokens_become_cache_write_and_are_not_double_counted(
    basic: list[UsageEvent],
) -> None:
    tokens = basic[2].tokens
    assert tokens.cache_read == 40
    assert tokens.cache_write == 25
    assert tokens.uncached_input == 100 - 40 - 25
    assert tokens.total == 120


def test_session_and_project_come_from_summary_json(basic: list[UsageEvent]) -> None:
    beta_events = basic[:3]
    assert {event.session_id for event in beta_events} == {"019fa1b1-0000-7000-8000-000000000001"}
    assert {event.project for event in beta_events} == {"beta"}
    assert {event.working_directory for event in beta_events} == {"/home/user/beta"}


def test_session_and_project_fall_back_to_url_decoded_directory_names(
    basic: list[UsageEvent],
) -> None:
    gamma_event = basic[3]
    assert gamma_event.session_id == "session-no-summary"
    assert gamma_event.project == "gamma"
    assert gamma_event.working_directory == "/tmp/gamma"
    assert gamma_event.model == "grok-4.3-build"


def test_non_turn_completed_updates_are_skipped(tmp_path: Path) -> None:
    lines = [
        {"timestamp": 1755590000, "params": {"update": {"sessionUpdate": "tool_call"}}},
        turn({"inputTokens": 10, "outputTokens": 1, "cachedReadTokens": 0, "reasoningTokens": 0}),
    ]
    write_session(tmp_path, lines)
    assert len(scan(tmp_path).events) == 1


def test_turn_completed_without_usage_is_skipped(tmp_path: Path) -> None:
    lines = [
        {
            "timestamp": 1755590000,
            "params": {
                "update": {"sessionUpdate": "turn_completed"},
                "_meta": {"eventId": "evt-1"},
            },
        },
    ]
    write_session(tmp_path, lines)
    assert scan(tmp_path).events == []


def test_all_zero_token_turns_are_skipped(tmp_path: Path) -> None:
    usage = {"inputTokens": 0, "outputTokens": 0, "cachedReadTokens": 0, "reasoningTokens": 0}
    write_session(tmp_path, [turn(usage)])
    assert scan(tmp_path).events == []


def test_multiple_models_in_one_turn_emit_one_event_each(tmp_path: Path) -> None:
    usage = {
        "modelUsage": {
            "grok-4.5-build": {
                "inputTokens": 10,
                "outputTokens": 2,
                "cachedReadTokens": 0,
                "reasoningTokens": 1,
            },
            "grok-4.3-build": {
                "inputTokens": 20,
                "outputTokens": 4,
                "cachedReadTokens": 5,
                "reasoningTokens": 0,
            },
        }
    }
    write_session(tmp_path, [turn(usage)])
    events = sorted(scan(tmp_path).events, key=lambda e: e.model or "")
    assert [event.model for event in events] == ["grok-4.3-build", "grok-4.5-build"]
    assert events[0].tokens.uncached_input == 15
    assert events[0].tokens.cache_read == 5


def test_request_id_includes_event_id_and_model_for_dedup(tmp_path: Path) -> None:
    usage = {"inputTokens": 10, "outputTokens": 1, "cachedReadTokens": 0, "reasoningTokens": 0}
    write_session(tmp_path, [turn(usage, event_id="evt-42")])
    event = scan(tmp_path).events[0]
    assert event.request_id == "grok-build:evt-42:unknown"


def test_model_is_unknown_without_summary_or_model_usage_map(tmp_path: Path) -> None:
    usage = {"inputTokens": 10, "outputTokens": 1, "cachedReadTokens": 0, "reasoningTokens": 0}
    write_session(tmp_path, [turn(usage)])
    assert scan(tmp_path).events[0].model == "unknown"


def test_agent_timestamp_ms_takes_priority_over_envelope_seconds(tmp_path: Path) -> None:
    line = turn({"inputTokens": 10, "outputTokens": 1, "cachedReadTokens": 0, "reasoningTokens": 0})
    line["params"]["_meta"]["agentTimestampMs"] = 1785328986355
    write_session(tmp_path, [line])
    event = scan(tmp_path).events[0]
    assert event.timestamp.isoformat() == "2026-07-29T12:43:06.355000+00:00"


def test_envelope_seconds_are_used_when_agent_timestamp_is_absent(tmp_path: Path) -> None:
    line = turn({"inputTokens": 10, "outputTokens": 1, "cachedReadTokens": 0, "reasoningTokens": 0})
    line["timestamp"] = 1750000000
    write_session(tmp_path, [line])
    event = scan(tmp_path).events[0]
    assert event.timestamp.isoformat() == "2025-06-15T15:06:40+00:00"


def test_line_session_id_wins_over_summary_id(tmp_path: Path) -> None:
    usage = {"inputTokens": 10, "outputTokens": 1, "cachedReadTokens": 0, "reasoningTokens": 0}
    write_session(
        tmp_path,
        [turn(usage, session_id="line-session")],
        summary={"info": {"id": "summary-session", "cwd": "/repo"}},
    )
    assert scan(tmp_path).events[0].session_id == "line-session"


def test_summary_session_id_is_used_when_line_omits_it(tmp_path: Path) -> None:
    usage = {"inputTokens": 10, "outputTokens": 1, "cachedReadTokens": 0, "reasoningTokens": 0}
    write_session(
        tmp_path,
        [turn(usage, session_id=None)],
        summary={"info": {"id": "summary-session", "cwd": "/repo"}},
    )
    assert scan(tmp_path).events[0].session_id == "summary-session"


def test_default_roots_uses_grok_home_when_set(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("GROK_HOME", str(tmp_path))
    assert default_roots() == [tmp_path / "sessions"]


def test_default_roots_falls_back_to_home_dot_grok(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GROK_HOME", raising=False)
    assert default_roots() == [Path.home() / ".grok" / "sessions"]
