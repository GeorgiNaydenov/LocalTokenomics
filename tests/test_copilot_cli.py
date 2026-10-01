from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from ai_usage_cost import pricing
from ai_usage_cost.models import UsageEvent
from ai_usage_cost.pipeline import analyze
from ai_usage_cost.pricing import RateTable, price_event
from ai_usage_cost.sources import copilot_cli, registry
from ai_usage_cost.sources.copilot_cli import SOURCE, default_roots, parse, session_files
from ai_usage_cost.store import fingerprint_of
from conftest import FIXTURES

BASIC = FIXTURES / "copilot_cli" / "basic"
SID = "sess-1"


@dataclass
class Scanned:
    events: list[UsageEvent] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def scan(root: Path) -> Scanned:
    result = Scanned()
    for path in session_files(root):
        result.events.extend(parse(path, result.warnings))
    return result


def write_session(root: Path, lines: list[dict | str], *, sid: str = SID) -> Path:
    folder = root / sid
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "events.jsonl"
    path.write_text(
        "\n".join(line if isinstance(line, str) else json.dumps(line) for line in lines) + "\n",
        encoding="utf-8",
    )
    return path


def start(sid: str = SID) -> dict:
    return {
        "id": "s0",
        "timestamp": "2026-09-30T10:00:00.000Z",
        "type": "session.start",
        "data": {"sessionId": sid, "context": {"cwd": "/work/proj"}},
    }


def usage(inp: int, out: int, cr: int = 0, cw: int = 0, reasoning: int = 0) -> dict:
    return {
        "inputTokens": inp,
        "outputTokens": out,
        "cacheReadTokens": cr,
        "cacheWriteTokens": cw,
        "reasoningTokens": reasoning,
    }


def shutdown(event_id: str, stamp: str, metrics: dict[str, dict], **extra: object) -> dict:
    return {
        "id": event_id,
        "timestamp": stamp,
        "type": "session.shutdown",
        "data": {
            "modelMetrics": {model: {"usage": u} for model, u in metrics.items()},
            **extra,
        },
    }


def test_basic_fixture_maps_tokens_and_metadata() -> None:
    result = scan(BASIC)
    assert result.warnings == []
    (event,) = result.events
    assert event.source == event.client == "copilot-cli"
    assert event.provider == "github-copilot"
    assert event.model == "claude-sonnet-4.6"
    assert event.session_id == "0f0e0d0c-0000-4000-8000-000000000001"
    assert event.timestamp.isoformat() == "2026-09-30T10:05:00+00:00"
    assert event.project == "demo"
    assert event.repository == "acme/demo"
    assert event.branch == "main"
    assert event.working_directory == "/work/demo"
    assert event.is_sidechain is False
    assert event.reported_cost is None
    tokens = event.tokens
    assert tokens is not None
    assert tokens.cache_read == 15_000
    assert tokens.cache_write_5m == 2_000
    assert tokens.uncached_input == 18_200 - 15_000 - 2_000
    assert tokens.output == 410
    assert tokens.reasoning_output == 90
    assert tokens.input_total == 18_200


def test_title_comes_from_workspace_yaml_name() -> None:
    (event,) = scan(BASIC).events
    assert (event.title, event.title_source) == ("Demo session", "tool")


def test_title_falls_back_to_summary_then_folder(tmp_path: Path) -> None:
    path = write_session(
        tmp_path, [start(), shutdown("e1", "2026-09-30T10:05:00Z", {"m": usage(5, 1)})]
    )
    (event,) = scan(tmp_path).events
    assert event.title_source == "folder"
    assert event.title == f"proj_{SID}"
    (path.parent / "workspace.yaml").write_text("summary: 'Did a thing' # note\n", encoding="utf-8")
    (event,) = scan(tmp_path).events
    assert (event.title, event.title_source) == ("Did a thing", "summary")


def test_workspace_yaml_supplies_cwd_when_start_has_no_context(tmp_path: Path) -> None:
    bare = {"id": "s0", "timestamp": "2026-09-30T10:00:00Z", "type": "session.start", "data": {}}
    path = write_session(
        tmp_path, [bare, shutdown("e1", "2026-09-30T10:05:00Z", {"m": usage(5, 1)})]
    )
    (path.parent / "workspace.yaml").write_text("cwd: C:\\work\\winproj\nbranch: dev\n", "utf-8")
    (event,) = scan(tmp_path).events
    assert event.project == "winproj"
    assert event.branch == "dev"
    assert event.session_id == SID  # directory name when session.start lacks sessionId


def test_ephemeral_usage_events_are_ignored() -> None:
    # The basic fixture carries an ephemeral assistant.usage with absurd numbers.
    (event,) = scan(BASIC).events
    assert event.tokens.output == 410  # type: ignore[union-attr]


def test_ephemeral_shutdown_is_skipped(tmp_path: Path) -> None:
    line = shutdown("e1", "2026-09-30T10:05:00Z", {"m": usage(100, 10)})
    line["ephemeral"] = True
    write_session(tmp_path, [start(), line])
    assert scan(tmp_path).events == []


def test_resume_emits_deltas_between_cumulative_shutdowns(tmp_path: Path) -> None:
    write_session(
        tmp_path,
        [
            start(),
            shutdown("e1", "2026-09-30T10:05:00Z", {"m": usage(1000, 100, 600, 200, 10)}),
            shutdown("e2", "2026-09-30T11:05:00Z", {"m": usage(2500, 260, 1500, 300, 25)}),
        ],
    )
    first, second = scan(tmp_path).events
    assert first.tokens.input_total == 1000 and first.tokens.output == 100  # type: ignore[union-attr]
    assert second.tokens is not None
    assert second.tokens.cache_read == 900
    assert second.tokens.cache_write_5m == 100
    assert second.tokens.uncached_input == 1500 - 900 - 100
    assert second.tokens.output == 160
    assert second.tokens.reasoning_output == 15
    assert first.request_id != second.request_id
    assert second.request_id == f"copilot-cli:{SID}:e2:m"
    assert second.timestamp.isoformat() == "2026-09-30T11:05:00+00:00"


def test_deltas_are_tracked_per_model(tmp_path: Path) -> None:
    write_session(
        tmp_path,
        [
            start(),
            shutdown("e1", "2026-09-30T10:05:00Z", {"a": usage(100, 10)}),
            shutdown("e2", "2026-09-30T11:05:00Z", {"a": usage(100, 10), "b": usage(50, 5)}),
        ],
    )
    events = scan(tmp_path).events
    # a unchanged in shutdown 2 (zero delta, no event); b is new and taken whole.
    assert [(e.model, e.tokens.total) for e in events] == [("a", 110), ("b", 55)]  # type: ignore[union-attr]


def test_smaller_total_is_a_counter_reset_and_taken_whole(tmp_path: Path) -> None:
    write_session(
        tmp_path,
        [
            start(),
            shutdown("e1", "2026-09-30T10:05:00Z", {"m": usage(1000, 100)}),
            shutdown("e2", "2026-09-30T11:05:00Z", {"m": usage(300, 40)}),
        ],
    )
    first, second = scan(tmp_path).events
    assert second.tokens.input_total == 300  # type: ignore[union-attr]
    assert second.tokens.output == 40  # type: ignore[union-attr]
    assert first.tokens.input_total == 1000  # type: ignore[union-attr]


def test_crashed_session_without_shutdown_warns_and_emits_nothing(tmp_path: Path) -> None:
    message = {
        "id": "m",
        "timestamp": "2026-09-30T10:00:07Z",
        "type": "assistant.message",
        "data": {"model": "claude-sonnet-4.6", "outputTokens": 410},
    }
    write_session(tmp_path, [start(), message])
    result = scan(tmp_path)
    assert result.events == []
    assert any("without a usage summary" in w for w in result.warnings)


def test_output_after_last_shutdown_warns_but_keeps_earlier_events(tmp_path: Path) -> None:
    message = {
        "id": "m",
        "timestamp": "2026-09-30T12:00:07Z",
        "type": "assistant.message",
        "data": {"outputTokens": 5},
    }
    write_session(
        tmp_path, [start(), shutdown("e1", "2026-09-30T10:05:00Z", {"m": usage(10, 2)}), message]
    )
    result = scan(tmp_path)
    assert len(result.events) == 1
    assert any("without a usage summary" in w for w in result.warnings)


def test_idle_session_without_shutdown_does_not_warn(tmp_path: Path) -> None:
    write_session(tmp_path, [start()])
    result = scan(tmp_path)
    assert result.events == [] and result.warnings == []


def test_compaction_complete_is_its_own_event_when_enabled(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(copilot_cli, "_COUNT_COMPACTION", True)
    compaction = {
        "id": "c1",
        "timestamp": "2026-09-30T10:30:00Z",
        "type": "session.compaction_complete",
        "data": {
            "tokenLimit": 200_000,
            "compactionTokensUsed": {
                "model": "gpt-5-mini",
                "inputTokens": 9000,
                "outputTokens": 700,
                "cacheReadTokens": 4000,
                "cacheWriteTokens": 0,
                "copilotUsage": {"totalNanoAiu": 5_000_000},
            },
        },
    }
    write_session(
        tmp_path, [start(), compaction, shutdown("e1", "2026-09-30T10:35:00Z", {"m": usage(10, 2)})]
    )
    events = scan(tmp_path).events
    comp = next(e for e in events if e.raw["kind"] == "compaction")
    assert comp.model == "gpt-5-mini"
    assert comp.request_id == f"copilot-cli:{SID}:c1:compaction"
    assert comp.tokens.uncached_input == 5000  # type: ignore[union-attr]
    assert comp.tokens.cache_read == 4000  # type: ignore[union-attr]
    assert comp.tokens.output == 700  # type: ignore[union-attr]
    assert comp.raw["copilot_credits"] == pytest.approx(0.005)
    assert len(events) == 2


def test_agent_metrics_are_not_double_counted() -> None:
    # The basic fixture repeats its totals under agentMetrics.main; only top level counts.
    (event,) = scan(BASIC).events
    assert event.tokens.total == 18_200 + 410  # type: ignore[union-attr]


def test_copilot_credits_in_raw_and_no_reported_cost() -> None:
    (event,) = scan(BASIC).events
    assert event.reported_cost is None
    assert event.raw["copilot_credits"] == pytest.approx(0.043)


def test_dotted_model_passes_through_and_prices_via_matcher() -> None:
    (event,) = scan(BASIC).events
    assert event.model == "claude-sonnet-4.6"
    cost, state = price_event(event, RateTable.load())
    assert state == "priced"
    assert cost is not None and cost.total > 0


def test_negative_and_odd_values_never_go_negative(tmp_path: Path) -> None:
    write_session(
        tmp_path,
        [start(), shutdown("e1", "2026-09-30T10:05:00Z", {"m": usage(10, 2, cr=30, cw=5)})],
    )
    (event,) = scan(tmp_path).events
    assert event.tokens.uncached_input == 0  # type: ignore[union-attr]


def test_malformed_lines_and_missing_keys_do_not_crash(tmp_path: Path) -> None:
    write_session(
        tmp_path,
        [
            "{not json",
            start(),
            {"type": "session.shutdown"},
            {"id": "e0", "type": "session.shutdown", "data": {"modelMetrics": []}},
            {"id": "e9", "type": "session.shutdown", "data": {"modelMetrics": {"m": 5, "n": {}}}},
            {"id": "ea", "type": "session.compaction_complete", "data": {}},
            shutdown("e1", "2026-09-30T10:05:00Z", {"m": usage(10, 2)}),
        ],
    )
    result = scan(tmp_path)
    assert len(result.events) == 1
    assert any("unparsable" in w for w in result.warnings)


def test_missing_root_yields_nothing(tmp_path: Path) -> None:
    assert session_files(tmp_path / "nope") == []
    assert scan(tmp_path / "nope").events == []


def test_copilot_home_env_override(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("COPILOT_HOME", str(tmp_path))
    assert default_roots() == [tmp_path / "session-state"]
    monkeypatch.delenv("COPILOT_HOME")
    assert default_roots() == [Path.home() / ".copilot" / "session-state"]


def test_reparse_is_idempotent_and_fingerprints_are_unique(tmp_path: Path) -> None:
    write_session(
        tmp_path,
        [
            start(),
            shutdown("e1", "2026-09-30T10:05:00Z", {"a": usage(100, 10), "b": usage(5, 1)}),
            shutdown("e2", "2026-09-30T11:05:00Z", {"a": usage(150, 15)}),
        ],
    )
    first = [fingerprint_of(e) for e in scan(tmp_path).events]
    second = [fingerprint_of(e) for e in scan(tmp_path).events]
    assert first == second
    assert len(set(first)) == len(first) == 3


def test_source_is_experimental_and_discovered() -> None:
    assert SOURCE.experimental is True
    assert SOURCE.token_data == "session"
    assert registry()["copilot-cli"] is SOURCE


def test_end_to_end_pipeline_prices_known_and_tolerates_unknown_model(tmp_path: Path) -> None:
    root = tmp_path / "session-state"
    write_session(
        root,
        [
            start(),
            shutdown(
                "e1",
                "2026-09-30T10:05:00Z",
                {
                    "claude-sonnet-4.6": usage(1_000_000, 100_000, 400_000, 100_000),
                    "totally-unknown-model": usage(10, 1),
                },
            ),
        ],
    )
    roots = {source_id: [tmp_path / "none"] for source_id in registry()}
    roots["copilot-cli"] = [root]
    result = analyze(db_path=tmp_path / "t.db", roots=roots, rates_path=pricing.DEFAULT_RATES_PATH)
    mine = [p for p in result.events if p.event.source == "copilot-cli"]
    assert len(mine) == 2
    by_model = {p.event.model: p for p in mine}
    assert by_model["claude-sonnet-4.6"].state == "priced"
    assert by_model["claude-sonnet-4.6"].cost is not None
    assert by_model["totally-unknown-model"].state == "unpriced"
    again = analyze(db_path=tmp_path / "t.db", roots=roots)
    assert len([p for p in again.events if p.event.source == "copilot-cli"]) == 2


def test_compaction_is_not_counted_by_default(tmp_path: Path) -> None:
    compaction = {
        "id": "c1",
        "timestamp": "2026-09-30T10:30:00Z",
        "type": "session.compaction_complete",
        "data": {"compactionTokensUsed": {"model": "m", "inputTokens": 9000, "outputTokens": 7}},
    }
    write_session(
        tmp_path, [start(), compaction, shutdown("e1", "2026-09-30T10:35:00Z", {"m": usage(10, 2)})]
    )
    (event,) = scan(tmp_path).events
    assert event.raw["kind"] == "shutdown"


def test_negative_inputs_are_clamped_to_zero(tmp_path: Path) -> None:
    write_session(
        tmp_path,
        [start(), shutdown("e1", "2026-09-30T10:05:00Z", {"m": usage(-50, 7, -3, -4, -1)})],
    )
    (event,) = scan(tmp_path).events
    tokens = event.tokens
    assert tokens is not None
    assert (tokens.uncached_input, tokens.cache_read, tokens.cache_write) == (0, 0, 0)
    assert tokens.output == 7
    assert tokens.reasoning_output == 0
