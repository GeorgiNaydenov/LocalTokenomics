from __future__ import annotations

from datetime import UTC, datetime

from ai_usage_cost.models import TokenUsage
from ai_usage_cost.pricing import RateTable
from ai_usage_cost.trace import Span, economics_of, insights_of

TABLE = RateTable.load()
WHEN = datetime(2026, 8, 20, 10, 0, tzinfo=UTC)


def turn_span(turn_id: str) -> Span:
    return Span(
        span_id=turn_id, turn_id=turn_id, source="claude-code", session_id="s1", seq=0,
        kind="turn", started_at=WHEN, source_file="f", record_offset=0, record_length=0,
    )


def call_span(span_id: str, turn_id: str, *, uncached_input: int, output: int) -> Span:
    return Span(
        span_id=span_id, turn_id=turn_id, source="claude-code", session_id="s1", seq=1,
        kind="model_call", model="claude-opus-5", started_at=WHEN,
        tokens=TokenUsage(uncached_input=uncached_input, output=output),
        tokens_provenance="measured",
        source_file="f", record_offset=0, record_length=0,
    )


def amplifying_turn(turn_id: str, ratio: int) -> list[Span]:
    call = call_span(f"{turn_id}-call", turn_id, uncached_input=ratio * 100, output=100)
    return [turn_span(turn_id), call]


def insights_for(spans: list[Span]) -> list:
    return insights_of(spans, economics_of(spans, TABLE))


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
                span_id=span_id, turn_id="t0", source="claude-code", session_id="s1", seq=2 + index,
                kind="model_call", model="claude-opus-5", started_at=WHEN,
                tokens=TokenUsage(
                    uncached_input=100 - ratio_pct, cache_read=ratio_pct, output=100,
                ),
                tokens_provenance="measured",
                source_file="f", record_offset=0, record_length=0,
            )
        )
    found = insights_for(spans)
    miss = next(i for i in found if i.kind == "cache_miss")
    assert miss.count == 3
    assert miss.span_id == "call1"
    assert "5%" in miss.message
