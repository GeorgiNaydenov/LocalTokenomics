from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from ai_usage_cost.models import TokenUsage
from ai_usage_cost.pricing import RateTable
from ai_usage_cost.sources.claude_code import SOURCE, spans
from ai_usage_cost.trace import UNATTRIBUTED_TURN_KEY, Span, context_of, economics_of
from conftest import CLAUDE_TRACE

SESSION = CLAUDE_TRACE / "-home-user-gamma" / "sess-trace.jsonl"
AGENT = CLAUDE_TRACE / "-home-user-gamma" / "sess-trace" / "subagents" / "agent-ag1.jsonl"

TABLE = RateTable.load()


def collect(path: Path) -> list[Span]:
    return list(spans(path, []))


def one(items: list[Span], **fields: object) -> Span:
    matches = [
        span for span in items if all(getattr(span, key) == value for key, value in fields.items())
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


def test_session_duration_does_not_add_a_nested_subagent_turn(
    session: list[Span], agent: list[Span]
) -> None:
    combined = sorted(session + agent, key=lambda span: (span.started_at, span.seq))
    econ = economics_of(combined, TABLE)
    assert econ.totals.duration_ms == 80_200


def test_turn_rows_carry_ordinal_started_at_and_sidechain(
    session: list[Span], agent: list[Span]
) -> None:
    combined = sorted(session + agent, key=lambda span: (span.started_at, span.seq))
    econ = economics_of(combined, TABLE)
    by_key = {row.key: row for row in econ.by_turn}

    assert by_key["p1"].ordinal == 1
    assert by_key["p1"].is_sidechain is False
    assert by_key["p1"].started_at is not None

    assert by_key["ap1"].ordinal == 2
    assert by_key["ap1"].is_sidechain is True

    assert by_key["p2"].ordinal == 3
    assert by_key["p2"].is_sidechain is False


def test_the_model_call_after_a_compaction_is_flagged(session: list[Span]) -> None:
    snapshots = context_of(session, TABLE)
    before = next(item for item in snapshots if item.span_id == "msg_c")
    after = next(item for item in snapshots if item.span_id == "msg_d")
    assert before.compacted_before is False
    assert after.compacted_before is True


def test_retries_counts_attempts_not_the_sum_of_their_indices() -> None:
    when = datetime(2026, 9, 5, 10, 0, tzinfo=UTC)
    turn = Span(
        span_id="t1",
        turn_id="t1",
        source="claude-code",
        session_id="s1",
        seq=0,
        kind="turn",
        started_at=when,
        source_file="f",
        record_offset=0,
        record_length=0,
    )
    errors = [
        Span(
            span_id=f"e{index}",
            turn_id="t1",
            source="claude-code",
            session_id="s1",
            seq=index + 1,
            kind="error",
            status="error",
            started_at=when,
            retry_attempt=attempt,
            source_file="f",
            record_offset=0,
            record_length=0,
        )
        for index, attempt in enumerate((1, 2, 3))
    ]
    econ = economics_of([turn, *errors], TABLE)
    assert econ.totals.retries == 3


def test_retries_combines_index_max_and_count_sum_in_one_turn() -> None:
    # One turn can carry both retry shapes at once: api_error records (an attempt index,
    # take the max) for one request, and a model_call's usage-iterations count (already a
    # genuine extra-attempts number, sum it) for a different request. 1/2/3 -> max 3, plus
    # a count of 2, must read 5 -- not 3+3=6, and not either figure alone.
    when = datetime(2026, 9, 5, 10, 0, tzinfo=UTC)
    turn = Span(
        span_id="t1",
        turn_id="t1",
        source="claude-code",
        session_id="s1",
        seq=0,
        kind="turn",
        started_at=when,
        source_file="f",
        record_offset=0,
        record_length=0,
    )
    errors = [
        Span(
            span_id=f"e{index}",
            turn_id="t1",
            source="claude-code",
            session_id="s1",
            seq=index + 1,
            kind="error",
            status="error",
            started_at=when,
            retry_attempt=attempt,
            source_file="f",
            record_offset=0,
            record_length=0,
        )
        for index, attempt in enumerate((1, 2, 3))
    ]
    model_call = Span(
        span_id="mc1",
        turn_id="t1",
        source="claude-code",
        session_id="s1",
        seq=4,
        kind="model_call",
        model="m1",
        started_at=when,
        retry_attempt=2,
        source_file="f",
        record_offset=0,
        record_length=0,
    )
    econ = economics_of([turn, *errors, model_call], TABLE)
    assert econ.totals.retries == 5


def test_one_failed_tool_call_counts_as_one_error(tmp_path: Path) -> None:
    path = tmp_path / "sess-err.jsonl"
    records = [
        {
            "type": "user",
            "uuid": "u1",
            "promptId": "p1",
            "timestamp": "2026-09-05T10:00:00.000Z",
            "sessionId": "sess-err",
            "message": {"role": "user", "content": "hi"},
        },
        {
            "type": "assistant",
            "uuid": "a1",
            "timestamp": "2026-09-05T10:00:01.000Z",
            "sessionId": "sess-err",
            "message": {
                "id": "m1",
                "model": "claude-opus-5",
                "usage": {"input_tokens": 10, "output_tokens": 10},
                "content": [{"type": "tool_use", "id": "t1", "name": "Bash", "input": {}}],
            },
        },
        {
            "type": "user",
            "uuid": "u2",
            "timestamp": "2026-09-05T10:00:02.000Z",
            "sessionId": "sess-err",
            "toolUseResult": {"is_error": True},
            "message": {
                "role": "user",
                "content": [{"type": "tool_result", "tool_use_id": "t1", "is_error": True}],
            },
        },
    ]
    path.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")
    found = collect(path)
    econ = economics_of(found, TABLE)
    assert econ.totals.errors == 1


def test_spans_without_a_turn_id_appear_in_an_unattributed_row() -> None:
    when = datetime(2026, 9, 5, 10, 0, tzinfo=UTC)
    turnless_call = Span(
        span_id="pre1",
        source="claude-code",
        session_id="s1",
        seq=0,
        kind="model_call",
        model="claude-opus-5",
        started_at=when,
        tokens=TokenUsage(uncached_input=10, output=5),
        tokens_provenance="measured",
        source_file="f",
        record_offset=0,
        record_length=0,
    )
    turn = Span(
        span_id="t1",
        turn_id="t1",
        source="claude-code",
        session_id="s1",
        seq=1,
        kind="turn",
        started_at=when,
        source_file="f",
        record_offset=0,
        record_length=0,
    )
    call = Span(
        span_id="m1",
        turn_id="t1",
        source="claude-code",
        session_id="s1",
        seq=2,
        kind="model_call",
        model="claude-opus-5",
        started_at=when,
        tokens=TokenUsage(uncached_input=1, output=1),
        tokens_provenance="measured",
        source_file="f",
        record_offset=0,
        record_length=0,
    )
    econ = economics_of([turnless_call, turn, call], TABLE)

    unattributed = next(row for row in econ.by_turn if row.key == UNATTRIBUTED_TURN_KEY)
    assert unattributed.label == "Outside any turn"
    assert unattributed.ordinal is None
    assert unattributed.tokens is not None
    assert unattributed.tokens.total == 15

    assert sum(row.tokens.total for row in econ.by_turn if row.tokens) == econ.totals.tokens.total
