from __future__ import annotations

from pathlib import Path

from ai_usage_cost.models import UsageEvent
from ai_usage_cost.sources.base import jsonl_files
from ai_usage_cost.sources.openai_compat import SOURCE, parse
from conftest import FIXTURES

OPENAI_COMPAT_A = FIXTURES / "openai_compat" / "a"
OPENAI_COMPAT_B = FIXTURES / "openai_compat" / "b"
OPENAI_COMPAT_BASIC = FIXTURES / "openai_compat" / "basic"


def scan(root: Path) -> list[UsageEvent]:
    events: list[UsageEvent] = []
    for path in jsonl_files(root):
        events.extend(parse(path, []))
    return events


def test_default_roots_is_empty() -> None:
    assert SOURCE.default_roots() == []


def test_cached_tokens_are_a_subset_of_prompt_tokens() -> None:
    events = scan(OPENAI_COMPAT_BASIC)
    event = next(e for e in events if e.request_id == "chatcmpl-basic-001")
    tokens = event.tokens
    assert tokens.uncached_input == 800
    assert tokens.cache_read == 200
    assert tokens.uncached_input + tokens.cache_read == 1000


def test_reasoning_tokens_are_a_subset_of_completion_tokens_and_output_stays_full() -> None:
    events = scan(OPENAI_COMPAT_BASIC)
    event = next(e for e in events if e.request_id == "chatcmpl-basic-001")
    tokens = event.tokens
    assert tokens.output == 500
    assert tokens.reasoning_output == 150


def test_record_missing_usage_entirely_yields_nothing() -> None:
    events = scan(OPENAI_COMPAT_BASIC)
    assert "chatcmpl-basic-002" not in {e.request_id for e in events}


def test_record_with_zero_usage_yields_nothing() -> None:
    events = scan(OPENAI_COMPAT_BASIC)
    assert "chatcmpl-basic-005" not in {e.request_id for e in events}


def test_provider_field_is_lowercased() -> None:
    events = scan(OPENAI_COMPAT_BASIC)
    event = next(e for e in events if e.request_id == "chatcmpl-basic-003")
    assert event.provider == "openrouter"


def test_provider_defaults_to_none() -> None:
    events = scan(OPENAI_COMPAT_BASIC)
    event = next(e for e in events if e.request_id == "chatcmpl-basic-001")
    assert event.provider is None


def test_response_nested_under_response_key_is_parsed() -> None:
    events = scan(OPENAI_COMPAT_BASIC)
    event = next(e for e in events if e.request_id == "chatcmpl-basic-004")
    assert event.model == "gpt-4o-mini"
    assert event.session_id == "sess-nested"
    assert event.tokens.uncached_input == 30
    assert event.tokens.output == 15


def test_request_id_matches_the_record_id() -> None:
    events = scan(OPENAI_COMPAT_BASIC)
    event = next(e for e in events if e.request_id == "chatcmpl-basic-001")
    assert event.request_id == "chatcmpl-basic-001"
    assert event.source == "openai-compat"
    assert event.client == "openai-compat"


def test_session_id_falls_back_to_file_stem() -> None:
    events = scan(OPENAI_COMPAT_BASIC)
    event = next(e for e in events if e.request_id == "chatcmpl-basic-001")
    assert event.session_id == "requests"


def test_files_a_and_b_each_yield_one_event_with_the_same_request_id() -> None:
    events_a = scan(OPENAI_COMPAT_A)
    events_b = scan(OPENAI_COMPAT_B)
    assert len(events_a) == 1
    assert len(events_b) == 1
    assert events_a[0].request_id == events_b[0].request_id == "chatcmpl-shared-001"
