from __future__ import annotations

from pathlib import Path

from ai_usage_cost.models import UsageEvent
from ai_usage_cost.sources.antigravity import antigravity_files, parse

FIXTURES = Path(__file__).parent / "fixtures"
ANTIGRAVITY_BRAIN = FIXTURES / "antigravity" / "brain"


def scan(root: Path) -> list[UsageEvent]:
    events: list[UsageEvent] = []
    for path in antigravity_files(root):
        events.extend(parse(path, []))
    return events


def test_only_planner_response_records_become_events() -> None:
    events = scan(ANTIGRAVITY_BRAIN)
    basic = [e for e in events if e.session_id == "test-uuid-1234"]
    assert len(basic) == 2


def test_model_carries_forward_from_settings_change_text() -> None:
    events = scan(ANTIGRAVITY_BRAIN)
    basic = [e for e in events if e.session_id == "test-uuid-1234"]
    assert all(event.model == "Gemini 3.5 Flash" for event in basic)
    assert all(event.provider == "google" for event in basic)


def test_cwd_carries_forward_to_the_next_planner_response() -> None:
    events = scan(ANTIGRAVITY_BRAIN)
    basic = [e for e in events if e.session_id == "test-uuid-1234"]
    assert all(event.working_directory == "/home/user/myproject" for event in basic)
    assert all(event.project == "myproject" for event in basic)


def test_session_id_comes_from_the_brain_directory_name() -> None:
    events = scan(ANTIGRAVITY_BRAIN)
    basic = [e for e in events if e.session_id == "test-uuid-1234"]
    assert basic[0].session_id == "test-uuid-1234"


def test_tokens_are_always_none() -> None:
    events = scan(ANTIGRAVITY_BRAIN)
    assert all(event.tokens is None for event in events)


def test_a_session_with_no_model_selection_message_stays_unavailable_not_broken(
    tmp_path: Path,
) -> None:
    session = tmp_path / "short-session" / ".system_generated" / "logs"
    session.mkdir(parents=True)
    transcript = session / "transcript_full.jsonl"
    transcript.write_text(
        '{"type": "PLANNER_RESPONSE", "step_index": 0, '
        '"created_at": "2026-08-21T09:00:00Z"}\n',
        encoding="utf-8",
    )
    warnings: list[str] = []
    events = list(parse(transcript, warnings))
    assert len(events) == 1
    assert events[0].model is None
    assert warnings == []


def test_transcript_full_is_preferred_over_transcript(tmp_path: Path) -> None:
    conv = tmp_path / "conv-1" / ".system_generated" / "logs"
    conv.mkdir(parents=True)
    conv.parent.parent.mkdir(parents=True, exist_ok=True)
    (conv / "transcript.jsonl").write_text(
        '{"step_index": 0, "type": "USER_INPUT", "created_at": "2026-08-20T11:00:00Z", '
        '"content": "The user changed setting `Model Selection` from None to Truncated."}\n'
        '{"step_index": 1, "type": "PLANNER_RESPONSE", "created_at": "2026-08-20T11:00:05Z", '
        '"content": "truncated response"}\n',
        encoding="utf-8",
    )
    (conv / "transcript_full.jsonl").write_text(
        '{"step_index": 0, "type": "USER_INPUT", "created_at": "2026-08-20T11:00:00Z", '
        '"content": "The user changed setting `Model Selection` from None to Full."}\n'
        '{"step_index": 1, "type": "PLANNER_RESPONSE", "created_at": "2026-08-20T11:00:05Z", '
        '"content": "full untruncated response"}\n',
        encoding="utf-8",
    )
    files = antigravity_files(tmp_path)
    assert len(files) == 1
    assert files[0].name == "transcript_full.jsonl"
    events = list(parse(files[0], []))
    assert events[0].model == "Full"


def test_real_fixture_prefers_transcript_full() -> None:
    files = antigravity_files(ANTIGRAVITY_BRAIN)
    chosen = next(p for p in files if p.parent.parent.parent.name == "test-uuid-full")
    assert chosen.name == "transcript_full.jsonl"
    events = list(parse(chosen, []))
    assert events[0].model == "Full Model"
