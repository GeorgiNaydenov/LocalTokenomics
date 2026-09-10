from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from ai_usage_cost.models import UsageEvent
from ai_usage_cost.sources.base import jsonl_files
from ai_usage_cost.sources.codex import parse
from conftest import CODEX_BASIC, CODEX_DRIFT

ROLLOUT = "rollout-2026-08-21T09-00-00-11111111-2222-3333-4444-555555555555.jsonl"


@dataclass
class Scanned:
    events: list[UsageEvent] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def scan(root: Path) -> Scanned:
    result = Scanned()
    for path in jsonl_files(root):
        result.events.extend(parse(path, result.warnings))
    return result


def usage(inp: int, cached: int, out: int, reasoning: int = 0) -> dict:
    return {
        "input_tokens": inp,
        "cached_input_tokens": cached,
        "cache_write_input_tokens": 0,
        "output_tokens": out,
        "reasoning_output_tokens": reasoning,
        "total_tokens": inp + out,
    }


def token_count(last: dict, total: dict, ts: str = "2026-08-21T09:01:00Z") -> dict:
    return {
        "timestamp": ts,
        "type": "event_msg",
        "payload": {
            "type": "token_count",
            "info": {"last_token_usage": last, "total_token_usage": total},
        },
    }


def token_usage_record(
    usage_dict: dict, response_id: str = "resp-1", ts: str = "2026-08-21T09:01:00Z"
) -> dict:
    return {
        "timestamp": ts,
        "type": "token_usage_record",
        "payload": {
            "thread_id": "thread-1",
            "turn_id": "turn-1",
            "session_id": "11111111-2222-3333-4444-555555555555",
            "root_turn_id": "turn-1",
            "response_id": response_id,
            "usage": usage_dict,
            "turn_token_usage": usage_dict,
            "thread_token_usage": usage_dict,
        },
    }


def write_rollout(root: Path, records: list[dict], name: str = ROLLOUT) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    path = root / name
    path.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")
    return path


@pytest.fixture
def basic() -> list[UsageEvent]:
    return scan(CODEX_BASIC).events


def test_cached_input_is_a_subset_of_input_tokens(basic: list[UsageEvent]) -> None:
    tokens = basic[1].tokens
    assert tokens.cache_read == 15_000
    assert tokens.uncached_input == 20_000 - 15_000
    assert tokens.input_total == 20_000


def test_uncached_input_is_the_whole_input_when_nothing_was_cached(
    basic: list[UsageEvent],
) -> None:
    tokens = basic[0].tokens
    assert tokens.cache_read == 0
    assert tokens.uncached_input == 10_000
    assert tokens.input_total == 10_000


def test_reasoning_output_is_a_subset_of_output_and_not_double_counted(
    basic: list[UsageEvent],
) -> None:
    tokens = basic[1].tokens
    assert tokens.reasoning_output == 300
    assert tokens.output == 800
    assert tokens.total == 20_000 + 800


def test_cached_input_greater_than_input_is_clamped(tmp_path: Path) -> None:
    write_rollout(tmp_path, [token_count(usage(1_000, 5_000, 100), usage(1_000, 5_000, 100))])
    tokens = scan(tmp_path).events[0].tokens
    assert tokens.cache_read == 1_000
    assert tokens.uncached_input == 0


def test_model_comes_from_session_meta(basic: list[UsageEvent]) -> None:
    assert [event.model for event in basic[:2]] == ["gpt-5-codex", "gpt-5-codex"]


def test_mid_session_model_change_applies_only_to_later_events(
    basic: list[UsageEvent],
) -> None:
    assert [event.model for event in basic] == [
        "gpt-5-codex",
        "gpt-5-codex",
        "gpt-5.6-terra",
        "gpt-5.6-terra",
    ]


def test_session_id_and_project_come_from_session_meta(basic: list[UsageEvent]) -> None:
    assert {event.session_id for event in basic} == {"11111111-2222-3333-4444-555555555555"}
    assert {event.project for event in basic} == {"beta"}
    assert {event.source for event in basic} == {"codex"}


def test_model_is_none_when_the_rollout_never_names_one(tmp_path: Path) -> None:
    write_rollout(tmp_path, [token_count(usage(100, 0, 10), usage(100, 0, 10))])
    assert scan(tmp_path).events[0].model is None


def test_events_before_the_first_model_record_are_backfilled(tmp_path: Path) -> None:
    write_rollout(
        tmp_path,
        [
            token_count(usage(100, 0, 10), usage(100, 0, 10), ts="2026-08-21T09:00:00Z"),
            token_count(usage(100, 0, 10), usage(200, 0, 20), ts="2026-08-21T09:01:00Z"),
            {
                "timestamp": "2026-08-21T09:02:00Z",
                "type": "session_meta",
                "payload": {"id": "s1", "model": "gpt-5.6-terra"},
            },
            token_count(usage(100, 0, 10), usage(300, 0, 30), ts="2026-08-21T09:03:00Z"),
        ],
    )
    events = scan(tmp_path).events
    assert len(events) == 3
    assert [event.model for event in events] == ["gpt-5.6-terra", "gpt-5.6-terra", "gpt-5.6-terra"]
    assert [event.timestamp.isoformat() for event in events] == [
        "2026-08-21T09:00:00+00:00",
        "2026-08-21T09:01:00+00:00",
        "2026-08-21T09:03:00+00:00",
    ]


def test_all_zero_last_token_usage_events_are_skipped(basic: list[UsageEvent]) -> None:
    assert len(basic) == 4
    assert all(event.tokens.total > 0 for event in basic)


def test_records_without_last_token_usage_are_skipped(tmp_path: Path) -> None:
    write_rollout(
        tmp_path,
        [
            {
                "timestamp": "2026-08-21T09:01:00Z",
                "type": "event_msg",
                "payload": {"type": "token_count", "info": {"total_token_usage": usage(0, 0, 0)}},
            },
            token_count(usage(100, 0, 10), usage(100, 0, 10)),
        ],
    )
    assert len(scan(tmp_path).events) == 1


def test_token_count_at_the_top_level_is_still_parsed(basic: list[UsageEvent]) -> None:
    tokens = basic[3].tokens
    assert tokens.uncached_input == 1_000
    assert tokens.output == 50
    assert basic[3].timestamp.isoformat() == "2026-08-21T09:06:00+00:00"


def test_top_level_envelope_alone_parses(tmp_path: Path) -> None:
    write_rollout(
        tmp_path,
        [
            {
                "timestamp": "2026-08-21T09:00:00Z",
                "type": "session_meta",
                "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                "cwd": "/home/user/legacy",
                "model": "gpt-5-codex",
            },
            {
                "timestamp": "2026-08-21T09:01:00Z",
                "type": "token_count",
                "info": {
                    "last_token_usage": usage(2_000, 500, 60),
                    "total_token_usage": usage(2_000, 500, 60),
                },
            },
        ],
    )
    events = scan(tmp_path).events
    assert len(events) == 1
    assert events[0].model == "gpt-5-codex"
    assert events[0].project == "legacy"
    assert events[0].tokens.uncached_input == 1_500
    assert events[0].tokens.cache_read == 500


def test_originator_maps_to_the_codex_desktop_client(tmp_path: Path) -> None:
    write_rollout(
        tmp_path,
        [
            {
                "timestamp": "2026-08-21T09:00:00Z",
                "type": "session_meta",
                "payload": {
                    "id": "s1",
                    "cwd": "/home/user/alpha",
                    "originator": "Codex Desktop",
                    "model_provider": "openai",
                    "git": {"repository_url": "https://github.com/x/y.git", "branch": "main"},
                },
            },
            token_count(usage(100, 0, 10), usage(100, 0, 10)),
        ],
    )
    event = scan(tmp_path).events[0]
    assert event.client == "codex-desktop"
    assert event.provider == "openai"
    assert event.repository == "https://github.com/x/y.git"
    assert event.branch == "main"


def test_unknown_originator_is_slugified_not_dropped(tmp_path: Path) -> None:
    write_rollout(
        tmp_path,
        [
            {
                "timestamp": "2026-08-21T09:00:00Z",
                "type": "session_meta",
                "payload": {"id": "s1", "originator": "Some New Client!"},
            },
            token_count(usage(100, 0, 10), usage(100, 0, 10)),
        ],
    )
    assert scan(tmp_path).events[0].client == "some-new-client"


def test_subagent_source_marks_is_sidechain(tmp_path: Path) -> None:
    write_rollout(
        tmp_path,
        [
            {
                "timestamp": "2026-08-21T09:00:00Z",
                "type": "session_meta",
                "payload": {"id": "s1", "source": {"subagent": {"other": "guardian"}}},
            },
            token_count(usage(100, 0, 10), usage(100, 0, 10)),
        ],
    )
    assert scan(tmp_path).events[0].is_sidechain is True


def test_no_session_meta_still_parses_with_default_client(tmp_path: Path) -> None:
    write_rollout(tmp_path, [token_count(usage(100, 0, 10), usage(100, 0, 10))])
    event = scan(tmp_path).events[0]
    assert event.client == "codex-cli"
    assert event.is_sidechain is False


def test_matching_session_total_produces_no_warning() -> None:
    result = scan(CODEX_BASIC)
    assert result.warnings == []
    assert sum(event.tokens.total for event in result.events) == 37_450


def test_disagreeing_session_total_warns_and_names_the_file() -> None:
    result = scan(CODEX_DRIFT)
    assert len(result.warnings) == 1
    warning = result.warnings[0]
    assert "rollout-2026-08-22T09-00-00-99999999-8888-7777-6666-555555555555.jsonl" in warning
    assert "10,500" in warning
    assert "50,000" in warning
    assert len(result.events) == 1


def test_a_real_total_with_an_all_zero_breakdown_still_counts_toward_reconciliation(
    tmp_path: Path,
) -> None:
    zero_breakdown_but_real_total = {
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "cache_write_input_tokens": 0,
        "output_tokens": 0,
        "reasoning_output_tokens": 0,
        "total_tokens": 50_000,
    }
    write_rollout(
        tmp_path,
        [
            token_count(zero_breakdown_but_real_total, usage(50_000, 0, 0)),
        ],
    )
    result = scan(tmp_path)
    assert result.events == []
    assert result.warnings == []


def test_drift_within_tolerance_is_not_warned_about(tmp_path: Path) -> None:
    write_rollout(
        tmp_path,
        [
            token_count(usage(90_000, 0, 10_000), usage(90_000, 0, 10_900)),
        ],
    )
    result = scan(tmp_path)
    assert result.events[0].tokens.total == 100_000
    assert result.warnings == []


def test_large_absolute_drift_under_one_percent_is_not_warned_about(tmp_path: Path) -> None:
    reported = dict(usage(9_000_000, 0, 1_005_000))
    reported["total_tokens"] = 10_005_000
    write_rollout(tmp_path, [token_count(usage(9_000_000, 0, 1_000_000), reported)])
    assert scan(tmp_path).warnings == []


def test_duplicate_token_count_events_with_an_unchanged_total_are_not_double_counted(
    tmp_path: Path,
) -> None:
    write_rollout(
        tmp_path,
        [
            token_count(usage(10_000, 0, 500), usage(10_000, 0, 500), ts="2026-08-21T09:01:00Z"),
            # Codex re-emits token_count on rate-limit-only updates with an unchanged
            # total_token_usage snapshot -- this second copy must not add another 10,500.
            token_count(usage(10_000, 0, 500), usage(10_000, 0, 500), ts="2026-08-21T09:01:01Z"),
            token_count(usage(5_000, 0, 200), usage(15_000, 0, 700), ts="2026-08-21T09:02:00Z"),
        ],
    )
    result = scan(tmp_path)
    assert len(result.events) == 2
    assert sum(event.tokens.total for event in result.events) == 10_500 + 5_200
    assert result.warnings == []


def test_token_usage_record_is_parsed_and_preferred_exclusively_over_token_count(
    tmp_path: Path,
) -> None:
    write_rollout(
        tmp_path,
        [
            {
                "timestamp": "2026-08-21T09:00:00Z",
                "type": "session_meta",
                "payload": {
                    "id": "11111111-2222-3333-4444-555555555555",
                    "model": "gpt-5.3-codex",
                },
            },
            # A token_count event with a wildly different total -- once the file has any
            # token_usage_record, token_count must be ignored for token accounting entirely.
            token_count(usage(999_000, 0, 999), usage(999_000, 0, 999), ts="2026-08-21T09:00:30Z"),
            token_usage_record(usage(10_000, 2_000, 500, reasoning=100), ts="2026-08-21T09:01:00Z"),
            token_usage_record(
                usage(5_000, 0, 200), response_id="resp-2", ts="2026-08-21T09:02:00Z"
            ),
        ],
    )
    result = scan(tmp_path)
    assert [event.tokens.output for event in result.events] == [500, 200]
    assert sum(event.tokens.total for event in result.events) == 10_500 + 5_200
    assert result.events[0].tokens.cache_read == 2_000
    assert result.events[0].tokens.reasoning_output == 100


def test_a_file_without_token_usage_records_still_uses_token_count(basic: list[UsageEvent]) -> None:
    # The CODEX_BASIC fixture has no token_usage_record lines -- token_count must still work.
    assert len(basic) == 4


def test_forked_thread_reconciliation_subtracts_inherited_history(tmp_path: Path) -> None:
    write_rollout(
        tmp_path,
        [
            {
                "timestamp": "2026-08-22T09:00:00Z",
                "type": "session_meta",
                "payload": {
                    "id": "22222222-3333-4444-5555-666666666666",
                    "model": "gpt-5-codex",
                    "forked_from_id": "parent-thread-id",
                },
            },
            # This turn's own usage is 10,500 tokens, but the cumulative total jumps straight
            # to 1,010,000 -- 999,500 tokens of history inherited from the forked-from parent.
            token_count(
                usage(10_000, 0, 500), usage(1_000_000, 0, 10_000), ts="2026-08-22T09:01:00Z"
            ),
        ],
    )
    result = scan(tmp_path)
    assert result.warnings == []
    assert len(result.events) == 1
    assert result.events[0].tokens.total == 10_500


def test_the_same_shape_without_forked_from_id_still_warns(tmp_path: Path) -> None:
    write_rollout(
        tmp_path,
        [
            {
                "timestamp": "2026-08-22T09:00:00Z",
                "type": "session_meta",
                "payload": {"id": "33333333-4444-5555-6666-777777777777", "model": "gpt-5-codex"},
            },
            token_count(
                usage(10_000, 0, 500), usage(1_000_000, 0, 10_000), ts="2026-08-22T09:01:00Z"
            ),
        ],
    )
    result = scan(tmp_path)
    assert len(result.warnings) == 1
    assert "forked thread" not in result.warnings[0]
    assert "drift" in result.warnings[0]


def test_a_counter_reset_gets_its_own_warning_kind_not_a_drift_percentage(tmp_path: Path) -> None:
    write_rollout(
        tmp_path,
        [
            {
                "timestamp": "2026-08-23T09:00:00Z",
                "type": "session_meta",
                "payload": {"id": "44444444-5555-6666-7777-888888888888", "model": "gpt-5-codex"},
            },
            token_count(
                usage(30_000, 0, 1_000), usage(30_000, 0, 1_000), ts="2026-08-23T09:01:00Z"
            ),
            token_count(usage(20_000, 0, 900), usage(50_000, 0, 1_900), ts="2026-08-23T09:02:00Z"),
            # The cumulative counter resets mid-session (e.g. a context-window sentinel).
            token_count(usage(5_000, 0, 100), usage(5_100, 0, 100), ts="2026-08-23T09:03:00Z"),
        ],
    )
    result = scan(tmp_path)
    assert len(result.warnings) == 1
    assert "counter reset" in result.warnings[0]
    assert "drift" not in result.warnings[0]
    assert len(result.events) == 3


def write_session_index(codex_root: Path, entries: list[dict]) -> Path:
    path = codex_root / "session_index.jsonl"
    path.write_text("\n".join(json.dumps(e) for e in entries) + "\n", encoding="utf-8")
    return path


def test_thread_name_from_session_index_sets_the_tool_title(tmp_path: Path) -> None:
    # session_index.jsonl lives one level above sessions/ -- the real layout is
    # ~/.codex/sessions/**/rollout-*.jsonl next to ~/.codex/session_index.jsonl.
    sessions_root = tmp_path / "sessions"
    write_session_index(
        tmp_path,
        [
            {
                "id": "11111111-2222-3333-4444-555555555555",
                "thread_name": "Run Prisma db pull and update schema",
                "updated_at": "2026-08-21T09:00:00Z",
            }
        ],
    )
    write_rollout(
        sessions_root,
        [
            {
                "timestamp": "2026-08-21T09:00:00Z",
                "type": "session_meta",
                "payload": {"id": "11111111-2222-3333-4444-555555555555", "model": "gpt-5-codex"},
            },
            token_count(usage(100, 0, 10), usage(100, 0, 10)),
        ],
    )
    event = scan(sessions_root).events[0]
    assert event.title == "Run Prisma db pull and update schema"
    assert event.title_source == "tool"


def test_a_command_name_wrapper_thread_name_falls_through_to_folder(tmp_path: Path) -> None:
    sessions_root = tmp_path / "sessions"
    write_session_index(
        tmp_path,
        [
            {
                "id": "22222222-3333-4444-5555-666666666666",
                "thread_name": "<command-name>/model</command-name>",
                "updated_at": "2026-08-21T09:00:00Z",
            }
        ],
    )
    write_rollout(
        sessions_root,
        [
            {
                "timestamp": "2026-08-21T09:00:00Z",
                "type": "session_meta",
                "payload": {
                    "id": "22222222-3333-4444-5555-666666666666",
                    "model": "gpt-5-codex",
                    "cwd": "/home/user/beta",
                },
            },
            token_count(usage(100, 0, 10), usage(100, 0, 10)),
        ],
    )
    event = scan(sessions_root).events[0]
    assert event.title_source == "folder"
    assert event.title == "beta_22222222-3333-4444-5555-666666666666"


def test_no_session_index_file_falls_back_to_folder_title(basic: list[UsageEvent]) -> None:
    # CODEX_BASIC has no session_index.jsonl at all.
    assert basic[0].title_source == "folder"
    assert basic[0].title == "beta_11111111-2222-3333-4444-555555555555"


def test_session_index_is_shared_across_every_rollout_file_under_one_root(
    tmp_path: Path,
) -> None:
    sessions_root = tmp_path / "sessions"
    write_session_index(
        tmp_path,
        [
            {
                "id": "11111111-2222-3333-4444-555555555555",
                "thread_name": "first thread",
                "updated_at": "2026-08-21T09:00:00Z",
            },
            {
                "id": "99999999-8888-7777-6666-555555555555",
                "thread_name": "second thread",
                "updated_at": "2026-08-22T09:00:00Z",
            },
        ],
    )
    write_rollout(
        sessions_root,
        [
            {
                "timestamp": "2026-08-21T09:00:00Z",
                "type": "session_meta",
                "payload": {"id": "11111111-2222-3333-4444-555555555555", "model": "gpt-5-codex"},
            },
            token_count(usage(100, 0, 10), usage(100, 0, 10)),
        ],
        name="rollout-a.jsonl",
    )
    write_rollout(
        sessions_root,
        [
            {
                "timestamp": "2026-08-22T09:00:00Z",
                "type": "session_meta",
                "payload": {"id": "99999999-8888-7777-6666-555555555555", "model": "gpt-5-codex"},
            },
            token_count(usage(100, 0, 10), usage(100, 0, 10)),
        ],
        name="rollout-b.jsonl",
    )
    events = scan(sessions_root).events
    titles = {event.title for event in events}
    assert titles == {"first thread", "second thread"}


def test_fingerprint_disambiguates_duplicate_token_count_fallback_keys(tmp_path: Path) -> None:
    # Two token_count events with the same timestamp, model and total_tokens used to collapse
    # into one via store.fingerprint_of's fallback key; record_offset now keeps them apart.
    write_rollout(
        tmp_path,
        [
            token_count(usage(1_000, 0, 100), usage(1_000, 0, 100), ts="2026-08-21T09:01:00Z"),
            token_count(usage(1_000, 0, 100), usage(2_000, 0, 200), ts="2026-08-21T09:01:00Z"),
        ],
    )
    events = scan(tmp_path).events
    assert len(events) == 2
    assert events[0].record_offset != events[1].record_offset
