from __future__ import annotations

from datetime import UTC, datetime

from ai_usage_cost.models import TokenUsage
from ai_usage_cost.pricing import RateTable
from ai_usage_cost.sources.claude_code import spans as claude_code_spans
from ai_usage_cost.trace import Span, context_of, economics_of, insights_of
from conftest import CLAUDE_TRACE

TABLE = RateTable.load()
WHEN = datetime(2026, 8, 20, 10, 0, tzinfo=UTC)


def turn_span(turn_id: str) -> Span:
    return Span(
        span_id=turn_id,
        turn_id=turn_id,
        source="claude-code",
        session_id="s1",
        seq=0,
        kind="turn",
        started_at=WHEN,
        source_file="f",
        record_offset=0,
        record_length=0,
    )


def call_span(span_id: str, turn_id: str, *, uncached_input: int, output: int) -> Span:
    return Span(
        span_id=span_id,
        turn_id=turn_id,
        source="claude-code",
        session_id="s1",
        seq=1,
        kind="model_call",
        model="claude-opus-5",
        started_at=WHEN,
        tokens=TokenUsage(uncached_input=uncached_input, output=output),
        tokens_provenance="measured",
        source_file="f",
        record_offset=0,
        record_length=0,
    )


def amplifying_turn(turn_id: str, ratio: int) -> list[Span]:
    call = call_span(f"{turn_id}-call", turn_id, uncached_input=ratio * 100, output=100)
    return [turn_span(turn_id), call]


def insights_for(spans: list[Span]) -> list:
    return insights_of(spans, economics_of(spans, TABLE), TABLE)


def test_a_single_hit_keeps_its_own_sentence() -> None:
    spans = amplifying_turn("t1", ratio=50)
    found = insights_for(spans)
    amp = next(i for i in found if i.kind == "amplification")
    assert amp.count == 1
    assert amp.span_id == "t1"
    assert "50" in amp.message
    assert amp.message.startswith("This turn read")


def test_many_hits_of_the_same_kind_collapse_into_one_insight() -> None:
    spans: list[Span] = []
    for index in range(40):
        spans += amplifying_turn(f"t{index}", ratio=25 + index)
    found = insights_for(spans)
    amplification_insights = [i for i in found if i.kind == "amplification"]
    assert len(amplification_insights) == 1
    amp = amplification_insights[0]
    assert amp.count == 40
    assert amp.span_id == "t39"
    assert "40 turns" in amp.message
    assert "64" in amp.message


def test_no_em_dash_in_any_generated_message() -> None:
    spans: list[Span] = []
    for index in range(5):
        spans += amplifying_turn(f"t{index}", ratio=25 + index)
    for insight in insights_for(spans):
        assert "—" not in insight.message


def test_a_quiet_session_has_no_amplification_insight() -> None:
    spans = amplifying_turn("t1", ratio=2)
    found = insights_for(spans)
    assert not any(i.kind == "amplification" for i in found)


def test_cache_miss_worst_pick_is_the_lowest_ratio_not_the_highest() -> None:
    spans: list[Span] = []
    turn = turn_span("t0")
    spans.append(turn)
    spans.append(call_span("first", "t0", uncached_input=1, output=1))
    for index, ratio_pct in enumerate([10, 5, 15]):
        span_id = f"call{index}"
        spans.append(
            Span(
                span_id=span_id,
                turn_id="t0",
                source="claude-code",
                session_id="s1",
                seq=2 + index,
                kind="model_call",
                model="claude-opus-5",
                started_at=WHEN,
                tokens=TokenUsage(
                    uncached_input=100 - ratio_pct,
                    cache_read=ratio_pct,
                    output=100,
                ),
                tokens_provenance="measured",
                source_file="f",
                record_offset=0,
                record_length=0,
            )
        )
    found = insights_for(spans)
    miss = next(i for i in found if i.kind == "cache_miss")
    assert miss.count == 3
    assert miss.span_id == "call1"
    assert "5%" in miss.message


def test_amplification_insight_uses_paid_tokens_not_cached_reads() -> None:
    # 10,005 input tokens per output token would trip the old (input_total / output)
    # amplification check, but almost all of it is a cheap cache read; only 5 uncached
    # tokens were actually paid at full rate, well under the limit.
    turn = turn_span("t1")
    call = Span(
        span_id="c1",
        turn_id="t1",
        source="claude-code",
        session_id="s1",
        seq=1,
        kind="model_call",
        model="claude-opus-5",
        started_at=WHEN,
        tokens=TokenUsage(uncached_input=5, cache_read=10_000, output=100),
        tokens_provenance="measured",
        source_file="f",
        record_offset=0,
        record_length=0,
    )
    econ = economics_of([turn, call], TABLE)
    row = econ.by_turn[0]
    assert row.tokens is not None
    # Displayed amplification is unchanged: input_total (including the cache read) / output.
    assert row.amplification == (5 + 10_000) / 100

    found = insights_of([turn, call], econ, TABLE)
    assert not any(insight.kind == "amplification" for insight in found)


def test_the_shipped_claude_code_trace_fixture_produces_no_amplification_insight() -> None:
    session_path = CLAUDE_TRACE / "-home-user-gamma" / "sess-trace.jsonl"
    agent_path = CLAUDE_TRACE / "-home-user-gamma" / "sess-trace" / "subagents" / "agent-ag1.jsonl"
    found_spans = [
        *claude_code_spans(session_path, []),
        *claude_code_spans(agent_path, []),
    ]
    econ = economics_of(found_spans, TABLE)
    found = insights_of(found_spans, econ, TABLE)
    assert not any(insight.kind == "amplification" for insight in found)


def test_context_pressure_fires_from_the_rate_table_capacity() -> None:
    # Claude Code only logs a measured context_capacity for [1m]-suffixed models; an
    # ordinary model call must fall back to the rate table the same way context_of does,
    # or the insight is dead for every Claude Code session.
    turn = turn_span("t1")
    call = Span(
        span_id="c1",
        turn_id="t1",
        source="claude-code",
        session_id="s1",
        seq=1,
        kind="model_call",
        model="claude-opus-5",
        started_at=WHEN,
        tokens=TokenUsage(uncached_input=900_000, output=10),
        tokens_provenance="measured",
        source_file="f",
        record_offset=0,
        record_length=0,
    )
    assert call.context_capacity is None
    assert call.capacity_provenance == "unavailable"

    found = insights_for([turn, call])
    pressure = next(insight for insight in found if insight.kind == "context_pressure")
    assert pressure.span_id == "c1"
    assert "90%" in pressure.message


def test_a_contributor_from_an_earlier_turn_is_not_lost_across_an_intervening_call() -> None:
    # B20: pending contributors used to be popped wholesale on every model call, so a
    # contributor from turn A that arrived before any call from A was destroyed the
    # moment an intervening call from a different turn B was processed. Partitioning
    # instead of popping keeps it pending until a call from its own turn consumes it.
    contributor = Span(
        span_id="c1",
        turn_id="A",
        source="claude-code",
        session_id="s1",
        seq=0,
        kind="user",
        started_at=WHEN,
        source_file="f",
        record_offset=0,
        record_length=0,
    )
    call_b = call_span("m-b", "B", uncached_input=10, output=10)
    call_a = call_span("m-a", "A", uncached_input=10, output=10)

    snapshots = context_of([contributor, call_b, call_a], TABLE)

    for_b = next(item for item in snapshots if item.span_id == "m-b")
    for_a = next(item for item in snapshots if item.span_id == "m-a")
    assert for_b.added_span_ids == []
    assert for_a.added_span_ids == ["c1"]
