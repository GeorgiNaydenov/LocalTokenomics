from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_usage_cost.sources.claude_code import SOURCE, spans
from ai_usage_cost.trace import Span
from conftest import CLAUDE_TRACE

SESSION = CLAUDE_TRACE / "-home-user-gamma" / "sess-trace.jsonl"
AGENT = CLAUDE_TRACE / "-home-user-gamma" / "sess-trace" / "subagents" / "agent-ag1.jsonl"


def collect(path: Path) -> list[Span]:
    return list(spans(path, []))


def one(items: list[Span], **fields: object) -> Span:
    matches = [
        span
        for span in items
        if all(getattr(span, key) == value for key, value in fields.items())
    ]
    assert len(matches) == 1, f"expected exactly one span for {fields}, got {len(matches)}"
    return matches[0]


@pytest.fixture
def session() -> list[Span]:
    return collect(SESSION)


@pytest.fixture
def agent() -> list[Span]:
    return collect(AGENT)


def test_the_source_declares_its_capabilities() -> None:
    assert SOURCE.spans is spans
    assert SOURCE.capabilities.model_dump() == {
        "trace": "measured",
        "tokens": "measured",
        "cost": "derived",
        "context": "estimated",
        "latency": "derived",
    }


def test_turns_are_delimited_by_prompt_id(session: list[Span]) -> None:
    turns = [span for span in session if span.kind == "turn"]
    assert [span.span_id for span in turns] == ["p1", "p2"]
    assert all(span.turn_id == span.span_id for span in turns)
    assert turns[0].duration_ms == 69_200
    assert turns[0].duration_provenance == "derived"


def test_a_compact_summary_does_not_open_a_new_turn(session: list[Span]) -> None:
    summary = one(session, name="compact_summary")
    assert summary.kind == "user"
    assert summary.turn_id == "p1"


def test_an_interruption_marks_the_turn_aborted(session: list[Span]) -> None:
    assert one(session, span_id="p2").status == "aborted"
    assert one(session, span_id="u14").status == "interrupted"


def test_one_model_call_per_message_id_with_tokens_counted_once(session: list[Span]) -> None:
    calls = [span for span in session if span.kind == "model_call"]
    assert [span.span_id for span in calls] == ["msg_a", "msg_b", "msg_c", "msg_d"]
    tokens = one(session, span_id="msg_a").tokens
    assert tokens is not None
    assert (tokens.uncached_input, tokens.cache_read, tokens.output) == (100, 20_000, 500)
    assert one(session, span_id="msg_a").tokens_provenance == "measured"


def test_the_blocks_of_one_message_share_the_model_call_parent(session: list[Span]) -> None:
    assert one(session, span_id="u2").kind == "reasoning"
    assert one(session, span_id="u2").parent_id == "msg_a"
    assert one(session, span_id="u3").parent_id == "msg_a"
    assert one(session, span_id="u3").record_parent == "u2"


def test_retry_attempt_comes_from_the_usage_iterations(session: list[Span]) -> None:
    assert one(session, span_id="msg_a").retry_attempt == 1
    assert one(session, span_id="msg_b").retry_attempt == 0
    assert one(session, span_id="msg_c").retry_attempt is None


def test_a_tool_call_is_closed_by_its_result(session: list[Span]) -> None:
    call = one(session, span_id="u3")
    result = one(session, span_id="u4")
    assert call.kind == "tool_call"
    assert call.name == "Bash"
    assert (call.duration_ms, call.duration_provenance) == (3_500, "derived")
    assert call.status == "ok"
    assert result.parent_id == call.span_id
    assert result.content_path == "toolUseResult.stdout"


def test_an_interrupted_result_is_copied_onto_its_tool_call(session: list[Span]) -> None:
    assert one(session, span_id="u12").status == "interrupted"
    assert one(session, span_id="u13").status == "interrupted"


def test_an_unclosed_tool_call_keeps_no_duration(session: list[Span]) -> None:
    for span in session:
        if span.duration_provenance == "unavailable":
            assert span.duration_ms is None


def test_the_subagent_span_carries_the_measured_agent_duration(session: list[Span]) -> None:
    subagent = one(session, kind="subagent")
    assert subagent.span_id == "u5"
    assert subagent.name == "Agent"
    assert (subagent.duration_ms, subagent.duration_provenance) == (45_000, "measured")
    assert subagent.agent_id == "ag1"
    assert subagent.detail["total_tokens"] == 12_345
    assert subagent.detail["tool_use_count"] == 3


def test_the_agent_file_spans_carry_the_parent_session(agent: list[Span]) -> None:
    assert {span.session_id for span in agent} == {"sess-trace"}
    assert {span.agent_id for span in agent} == {"ag1"}
    assert all(span.is_sidechain for span in agent)


def test_the_agent_file_root_carries_the_meta_json_fields(agent: list[Span]) -> None:
    root = one(agent, parent_id=None)
    assert root.kind == "turn"
    assert root.detail["agent_type"] == "general-purpose"
    assert root.detail["spawn_depth"] == 1
    assert root.detail["tool_use_id"] == "toolu_2"


def test_a_missing_meta_file_is_not_fatal(tmp_path: Path) -> None:
    target = tmp_path / "subagents" / "agent-ag9.jsonl"
    target.parent.mkdir(parents=True)
    target.write_bytes(AGENT.read_bytes())
    root = one(collect(target), parent_id=None)
    assert root.agent_id == "ag1"
    assert "agent_type" not in root.detail


def test_an_api_error_becomes_an_error_span(session: list[Span]) -> None:
    error = one(session, name="api_error")
    assert error.kind == "error"
    assert error.status == "error"
    assert error.retry_attempt == 1
    assert error.error == "500 status code (no body)"
    assert error.turn_id == "p1"


def test_the_compaction_is_measured_and_owns_the_summary(session: list[Span]) -> None:
    compaction = one(session, kind="compaction")
    assert compaction.name == "auto"
    assert (compaction.duration_ms, compaction.duration_provenance) == (4_200, "measured")
    assert compaction.detail["pre_tokens"] == 150_000
    assert one(session, name="compact_summary").parent_id == compaction.span_id


def test_a_one_million_model_infers_its_capacity(session: list[Span]) -> None:
    long_context = one(session, span_id="msg_b")
    assert long_context.model == "claude-sonnet-5[1m]"
    assert (long_context.context_capacity, long_context.capacity_provenance) == (
        1_000_000,
        "inferred",
    )


def test_an_ordinary_model_leaves_capacity_unavailable(session: list[Span]) -> None:
    ordinary = one(session, span_id="msg_a")
    assert ordinary.context_capacity is None
    assert ordinary.capacity_provenance == "unavailable"


def test_every_span_carries_the_project_and_working_directory(session: list[Span]) -> None:
    assert {span.detail["project"] for span in session} == {"gamma"}
    assert {span.detail["working_directory"] for span in session} == {"/home/user/gamma"}


def test_seq_increases_in_emission_order(session: list[Span]) -> None:
    assert [span.seq for span in session] == list(range(len(session)))


def test_the_offset_and_length_re_read_the_source_record(session: list[Span]) -> None:
    error = one(session, name="api_error")
    with SESSION.open("rb") as handle:
        handle.seek(error.record_offset)
        record = json.loads(handle.read(error.record_length))
    assert record["uuid"] == "u7"
    assert record["subtype"] == "api_error"
