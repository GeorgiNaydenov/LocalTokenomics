from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_usage_cost.models import UsageEvent
from ai_usage_cost.sources.base import jsonl_files
from ai_usage_cost.sources.claude_code import parse, spans
from conftest import CLAUDE_BASIC, CLAUDE_DEDUP

MESSAGE_SPLIT = Path(__file__).parent / "fixtures" / "claude_code" / "message_split"


def scan(root: Path) -> list[UsageEvent]:
    events: list[UsageEvent] = []
    for path in jsonl_files(root):
        events.extend(parse(path, []))
    return events


def write_session(root: Path, name: str, records: list[dict]) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    path = root / name
    path.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")
    return path


def assistant(request_id: str, usage: dict, **extra: object) -> dict:
    record = {
        "type": "assistant",
        "timestamp": "2026-08-20T10:00:00Z",
        "sessionId": "sess-tmp",
        "requestId": request_id,
        "cwd": "/home/user/alpha",
        "message": {"id": f"msg_{request_id}", "model": "claude-opus-5", "usage": usage},
    }
    record.update(extra)
    return record


@pytest.fixture
def basic() -> dict[str, UsageEvent]:
    events = scan(CLAUDE_BASIC)
    result: dict[str, UsageEvent] = {}
    for event in events:
        result.setdefault(f"{event.model}:{event.tier}", event)
    return result


def test_four_token_buckets_map_straight_across(basic: dict[str, UsageEvent]) -> None:
    tokens = basic["claude-opus-5:standard"].tokens
    assert tokens.uncached_input == 120
    assert tokens.cache_read == 40_000
    assert tokens.cache_write_5m == 2_000
    assert tokens.cache_write_1h == 4_000
    assert tokens.output == 900


def test_input_tokens_is_taken_as_already_excluding_cache(
    basic: dict[str, UsageEvent],
) -> None:
    tokens = basic["claude-opus-5:standard"].tokens
    assert tokens.input_total == 120 + 40_000 + 2_000 + 4_000
    assert tokens.total == 47_020


def test_cache_creation_supplies_the_5m_1h_split(basic: dict[str, UsageEvent]) -> None:
    tokens = basic["claude-opus-5:standard"].tokens
    assert (tokens.cache_write_5m, tokens.cache_write_1h) == (2_000, 4_000)
    assert tokens.cache_write == 6_000


def test_missing_cache_creation_falls_back_to_the_5m_bucket(
    basic: dict[str, UsageEvent],
) -> None:
    tokens = basic["claude-sonnet-5:standard"].tokens
    assert tokens.cache_write_5m == 1_500
    assert tokens.cache_write_1h == 0


def test_usage_iterations_are_not_summed_on_top_of_the_top_level_block(
    basic: dict[str, UsageEvent],
) -> None:
    tokens = basic["claude-opus-5:standard"].tokens
    assert tokens.uncached_input == 120
    assert tokens.cache_read == 40_000
    assert tokens.output == 900
    assert tokens.total == 47_020


def test_thinking_tokens_are_recorded_but_not_billed(
    basic: dict[str, UsageEvent],
) -> None:
    tokens = basic["claude-opus-5:standard"].tokens
    assert tokens.reasoning_output == 300
    assert tokens.total == tokens.input_total + tokens.output
    assert tokens.total == 47_020


def test_synthetic_and_zero_token_records_are_skipped() -> None:
    events = scan(CLAUDE_BASIC)
    assert len(events) == 5
    assert "<synthetic>" not in {event.model for event in events}
    assert all(event.tokens.total > 0 for event in events)


def test_non_assistant_records_are_ignored(tmp_path: Path) -> None:
    write_session(
        tmp_path,
        "sess.jsonl",
        [
            {"type": "user", "timestamp": "2026-08-20T10:00:00Z", "message": {"role": "user"}},
            {"type": "summary", "summary": "did a thing"},
            assistant("r1", {"input_tokens": 10, "output_tokens": 10}),
        ],
    )
    assert len(scan(tmp_path)) == 1


def test_repeated_message_id_and_request_id_in_one_file_yields_two_events(
    basic: dict[str, UsageEvent],
) -> None:
    assert basic["claude-opus-5:standard"].tokens.uncached_input == 120


def test_the_same_record_in_two_files_has_the_same_request_id() -> None:
    events = scan(CLAUDE_DEDUP)
    request_ids = [event.request_id for event in events]
    assert len(request_ids) == len(set(request_ids)) + 1


def test_is_sidechain_and_fast_speed_are_carried_through(
    basic: dict[str, UsageEvent],
) -> None:
    event = basic["claude-opus-5:fast"]
    assert event.is_sidechain is True
    assert event.tier == "fast"


def test_service_tier_batch_becomes_the_batch_tier(basic: dict[str, UsageEvent]) -> None:
    event = basic["claude-haiku-4-5:batch"]
    assert event.tier == "batch"
    assert event.is_sidechain is False


def test_default_tier_is_standard(basic: dict[str, UsageEvent]) -> None:
    assert basic["claude-sonnet-5:standard"].tier == "standard"


def test_project_name_comes_from_cwd(tmp_path: Path) -> None:
    write_session(
        tmp_path / "-home-user-encoded-elsewhere",
        "sess.jsonl",
        [assistant("r1", {"input_tokens": 10, "output_tokens": 10}, cwd="/home/user/alpha")],
    )
    events = scan(tmp_path)
    assert [event.project for event in events] == ["alpha"]
    assert [event.working_directory for event in events] == ["/home/user/alpha"]


def test_custom_title_record_sets_the_title_and_tool_source(tmp_path: Path) -> None:
    write_session(
        tmp_path,
        "sess.jsonl",
        [
            {"type": "custom-title", "customTitle": "Application naming brainstorm"},
            assistant("r1", {"input_tokens": 10, "output_tokens": 10}),
        ],
    )
    events = scan(tmp_path)
    assert [event.title for event in events] == ["Application naming brainstorm"]
    assert [event.title_source for event in events] == ["tool"]


def test_a_later_custom_title_record_wins_over_an_earlier_one(tmp_path: Path) -> None:
    write_session(
        tmp_path,
        "sess.jsonl",
        [
            {"type": "custom-title", "customTitle": "first title"},
            assistant("r1", {"input_tokens": 10, "output_tokens": 10}),
            {"type": "custom-title", "customTitle": "renamed title"},
            assistant("r2", {"input_tokens": 10, "output_tokens": 10}),
        ],
    )
    events = scan(tmp_path)
    assert [event.title for event in events] == ["first title", "renamed title"]


def test_no_custom_title_falls_back_to_the_folder_title(tmp_path: Path) -> None:
    # sessionId=None forces the event's session id to fall back to the filename (path.stem),
    # matching how the folder-fallback title is expected to read: project_session-id.
    write_session(
        tmp_path / "-home-user-alpha",
        "sess-alpha.jsonl",
        [
            assistant(
                "r1",
                {"input_tokens": 10, "output_tokens": 10},
                cwd="/home/user/alpha",
                sessionId=None,
            )
        ],
    )
    events = scan(tmp_path)
    assert events[0].title == "alpha_sess-alpha"
    assert events[0].title_source == "folder"


def test_a_message_split_over_three_records_yields_three_parse_events() -> None:
    path = MESSAGE_SPLIT / "-home-user-delta" / "sess-split.jsonl"
    events = list(parse(path, []))
    assert [event.tokens.output for event in events] == [10, 50, 120]


def test_a_message_split_over_three_records_keeps_the_largest_output_in_the_trace() -> None:
    path = MESSAGE_SPLIT / "-home-user-delta" / "sess-split.jsonl"
    found = list(spans(path, []))
    calls = [span for span in found if span.kind == "model_call"]
    assert len(calls) == 1
    call = calls[0]
    assert call.tokens is not None
    assert call.tokens.output == 120
    assert call.tokens.reasoning_output == 0
    assert call.tokens.uncached_input == 200
    assert call.tokens.cache_read == 5_000


def test_session_id_and_timestamp_come_from_the_record(
    basic: dict[str, UsageEvent],
) -> None:
    event = basic["claude-opus-5:standard"]
    assert event.source == "claude-code"
    assert event.client == "claude-code"
    assert event.session_id == "sess-alpha"
    assert event.timestamp.isoformat() == "2026-08-20T10:00:05+00:00"
    assert event.source_file.endswith("sess-alpha.jsonl")
