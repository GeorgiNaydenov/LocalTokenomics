from __future__ import annotations

from pathlib import Path

from ai_usage_cost.models import UsageEvent
from ai_usage_cost.sources.jan import jan_files, parse

FIXTURES = Path(__file__).parent / "fixtures"
JAN_BASIC = FIXTURES / "jan" / "threads"


def scan(root: Path) -> list[UsageEvent]:
    events: list[UsageEvent] = []
    for path in jan_files(root):
        events.extend(parse(path, []))
    return events


def test_only_assistant_messages_become_events() -> None:
    events = scan(JAN_BASIC)
    assert len(events) == 2


def test_client_and_provider_and_model_come_from_thread_json() -> None:
    events = scan(JAN_BASIC)
    event = events[0]
    assert event.source == "jan"
    assert event.client == "jan"
    assert event.provider == "local"
    assert event.model == "llama3.1-8b-instruct"


def test_tokens_are_none() -> None:
    events = scan(JAN_BASIC)
    assert all(event.tokens is None for event in events)


def test_session_id_matches_thread_id() -> None:
    events = scan(JAN_BASIC)
    assert all(event.session_id == "thread-1" for event in events)


def test_missing_thread_json_yields_events_with_no_model(tmp_path: Path) -> None:
    thread_dir = tmp_path / "thread-2"
    thread_dir.mkdir(parents=True)
    messages = thread_dir / "messages.jsonl"
    messages.write_text(
        '{"id": "msg-1", "role": "assistant", "thread_id": "thread-2", "created": 1755680000000}\n',
        encoding="utf-8",
    )
    events = scan(tmp_path)
    assert len(events) == 1
    assert events[0].model is None
    assert events[0].provider is None
    assert events[0].session_id == "thread-2"


def test_thread_json_title_becomes_the_tool_title() -> None:
    events = scan(JAN_BASIC)
    assert events[0].title == "Local model chat"
    assert events[0].title_source == "tool"


def test_missing_thread_json_falls_back_to_the_folder_title(tmp_path: Path) -> None:
    thread_dir = tmp_path / "thread-2"
    thread_dir.mkdir(parents=True)
    messages = thread_dir / "messages.jsonl"
    messages.write_text(
        '{"id": "msg-1", "role": "assistant", "thread_id": "thread-2", "created": 1755680000000}\n',
        encoding="utf-8",
    )
    events = scan(tmp_path)
    assert events[0].title_source == "folder"
    assert events[0].title == "(no project)_thread-2"
