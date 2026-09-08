from __future__ import annotations

from pathlib import Path

from ai_usage_cost.sources.antigravity import SOURCE, antigravity_files, spans
from ai_usage_cost.trace import Span

FIXTURES = Path(__file__).parent / "fixtures"
ANTIGRAVITY_TRACE = FIXTURES / "antigravity" / "trace"


def scan() -> list[Span]:
    collected: list[Span] = []
    for path in antigravity_files(ANTIGRAVITY_TRACE):
        collected.extend(spans(path, []))
    return collected


def by_id(span_id: str) -> Span:
    return next(span for span in scan() if span.span_id == span_id)


def test_typed_steps_become_tool_calls_with_derived_durations() -> None:
    view = by_id("test-uuid-trace:2")
    assert view.kind == "tool_call"
    assert view.name == "VIEW_FILE"
    assert view.status == "ok"
    assert view.duration_ms == 2000
    assert view.duration_provenance == "derived"
    assert view.detail["truncated_fields"] == "content"


def test_error_status_and_error_text_are_carried() -> None:
    command = by_id("test-uuid-trace:4")
    assert command.kind == "tool_call"
    assert command.status == "error"
    assert command.error == "sample command exited with a sample failure"
    assert command.duration_ms == 1000

    message = by_id("test-uuid-trace:5")
    assert message.kind == "error"
    assert message.error == "invalid sample tool call"
    assert message.duration_ms is None
    assert message.duration_provenance == "unavailable"


def test_no_span_reports_tokens() -> None:
    collected = scan()
    assert collected
    assert all(span.tokens is None for span in collected)
    assert all(span.tokens_provenance == "unavailable" for span in collected)


def test_model_call_carries_the_switched_model_and_its_children() -> None:
    call = by_id("test-uuid-trace:1")
    assert call.kind == "model_call"
    assert call.model == "Sample Model"
    assert call.parent_id == "test-uuid-trace:t0"
    assert by_id("test-uuid-trace:1:thinking").kind == "reasoning"
    assert by_id("test-uuid-trace:1:content").kind == "assistant"
    assert by_id("test-uuid-trace:2").parent_id == "test-uuid-trace:1"


def test_skipped_types_produce_no_span() -> None:
    assert not [span for span in scan() if span.span_id == "test-uuid-trace:3"]


def test_turn_detail_carries_project_and_working_directory() -> None:
    turn = by_id("test-uuid-trace:t6")
    assert turn.kind == "turn"
    assert turn.detail["project"] == "sample"
    assert turn.detail["working_directory"] == "/home/user/sample"


def test_spans_are_emitted_in_increasing_sequence() -> None:
    collected = scan()
    assert [span.seq for span in collected] == sorted(span.seq for span in collected)
    assert len(set(span.span_id for span in collected)) == len(collected)


def test_source_declares_its_capabilities() -> None:
    assert SOURCE.spans is spans
    assert SOURCE.capabilities.trace == "measured"
    assert SOURCE.capabilities.latency == "derived"
    assert SOURCE.capabilities.tokens == "unavailable"
    assert SOURCE.capabilities.cost == "unavailable"
    assert SOURCE.capabilities.context == "unavailable"


def test_web_search_becomes_a_retrieval_span() -> None:
    search = by_id("test-uuid-trace:8")
    assert search.kind == "retrieval"
    assert search.name == "SEARCH_WEB"
    assert search.duration_ms == 4000
    assert search.duration_provenance == "derived"


def test_invoking_a_subagent_records_the_child_conversation() -> None:
    invoke = by_id("test-uuid-trace:9")
    assert invoke.kind == "subagent"
    assert invoke.agent_id == "aaaaaaaa-1111-2222-3333-bbbbbbbbbbbb"
    assert invoke.detail["child_session_id"] == "aaaaaaaa-1111-2222-3333-bbbbbbbbbbbb"
    assert invoke.duration_ms == 2000


def test_asking_the_user_a_question_is_an_assistant_span() -> None:
    question = by_id("test-uuid-trace:10")
    assert question.kind == "assistant"
    assert question.name == "ASK_QUESTION"
    assert question.duration_ms == 6000


def test_a_failed_command_records_its_exit_code() -> None:
    failed = by_id("test-uuid-trace:11")
    assert failed.kind == "tool_call"
    assert failed.status == "error"
    assert failed.detail["exit_code"] == 2


def test_a_command_without_a_reported_exit_code_records_none() -> None:
    earlier = by_id("test-uuid-trace:4")
    assert "exit_code" not in earlier.detail
