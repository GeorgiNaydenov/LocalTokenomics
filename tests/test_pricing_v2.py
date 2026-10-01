"""Schema v2 pricing: periods, bands, tiers, peak, cache resolution, match kinds.

Every table here is built inline, so none of it depends on the shipped rates.json (whose
contents change); the one exception is the frozen v1 fixture used to prove an old file still
loads and prices exactly as before.
"""

from __future__ import annotations

import json
from datetime import UTC, date, datetime, timedelta, timezone
from pathlib import Path

import pytest

from ai_usage_cost import trace as trace_module
from ai_usage_cost.aggregate import build_report, warning_groups_of
from ai_usage_cost.models import CostBreakdown, PricedEvent, TokenUsage, UsageEvent
from ai_usage_cost.pipeline import (
    Analysis,
    _sources_of,
    analyze,
    estimated_models,
    reported_cost_divergences,
    tier_unpriced_models,
)
from ai_usage_cost.pricing import (
    BUILTIN_PREFIXES,
    MILLION,
    PartialRules,
    Prefix,
    ProviderRules,
    RateTable,
    effective_prefixes,
    merge_rules,
    normalise_model,
    price_event,
    resolve_provider,
)
from ai_usage_cost.sources.base import Source
from ai_usage_cost.trace import Span
from conftest import FIXTURES, NO_ROOT

M = 1_000_000

PROVIDERS = {
    "acme": {"cache_read": 0.1, "cache_write_5m": 1.25, "cache_write_1h": 1.5, "batch": 0.4},
    "local": {"free": True},
}


def row(match: str = "m", **fields: object) -> dict[str, object]:
    base: dict[str, object] = {
        "match": match,
        "provider": "acme",
        "display": match.upper(),
        "input": 10.0,
        "output": 40.0,
    }
    return {**base, **fields}


def table(*models: dict[str, object], **extra: object) -> RateTable:
    return RateTable.model_validate(
        {"as_of": "2026-10-01", "providers": PROVIDERS, "models": list(models), **extra}
    )


def at(*args: int) -> datetime:
    return datetime(*args, tzinfo=UTC)


def make_event(
    model: str, when: datetime | None = None, tier: str = "standard", **tokens: int
) -> UsageEvent:
    return UsageEvent(
        source="claude-code",
        client="claude-code",
        model=model,
        timestamp=when or at(2026, 10, 1, 12),
        session_id="s1",
        tokens=TokenUsage(**tokens),
        tier=tier,
    )


def cost(
    rates: RateTable,
    model: str = "m",
    when: datetime | None = None,
    tier: str = "standard",
    **tokens: int,
) -> CostBreakdown:
    result, state = price_event(make_event(model, when, tier, **tokens), rates)
    assert state == "priced"
    assert result is not None
    return result


def input_per_m(rates: RateTable, tokens: int, **kwargs: object) -> float:
    """Effective input price per million for a request of `tokens` uncached tokens."""
    return cost(rates, uncached_input=tokens, **kwargs).uncached_input / tokens * MILLION  # type: ignore[arg-type]


# --- periods ---------------------------------------------------------------------------

PERIODS = table(
    row(
        periods=[
            {"until": "2026-07-01", "input": 20.0, "output": 80.0},
            {"from": "2026-07-01", "until": "2026-08-01", "input": 15.0, "output": 60.0},
        ]
    )
)


@pytest.mark.parametrize(
    "when,expected",
    [
        (at(2026, 1, 1), 20.0),
        (datetime(2026, 6, 30, 23, 59, 59, tzinfo=UTC), 20.0),
        (at(2026, 7, 1), 15.0),
        (datetime(2026, 7, 31, 23, 59, 59, tzinfo=UTC), 15.0),
        (at(2026, 8, 1), 10.0),
        (at(2027, 1, 1), 10.0),
    ],
)
def test_period_from_is_inclusive_until_is_exclusive_in_utc(
    when: datetime, expected: float
) -> None:
    assert cost(PERIODS, when=when, uncached_input=M).uncached_input == pytest.approx(expected)


def test_a_period_is_chosen_by_the_utc_date_not_the_local_one() -> None:
    # 01:00 on July 1st at +02:00 is still 23:00 on June 30th in UTC.
    local = datetime(2026, 7, 1, 1, 0, tzinfo=timezone(timedelta(hours=2)))
    assert cost(PERIODS, when=local, uncached_input=M).uncached_input == pytest.approx(20.0)


def test_a_naive_timestamp_is_read_as_utc() -> None:
    naive = datetime(2026, 6, 30, 23, 0)
    assert cost(PERIODS, when=naive, uncached_input=M).uncached_input == pytest.approx(20.0)


def test_a_period_replaces_only_the_fields_it_writes() -> None:
    rates = table(
        row(
            cache_read=1.0,
            periods=[{"until": "2026-07-01", "input": 20.0}],
        )
    )
    old = cost(rates, when=at(2026, 6, 1), uncached_input=M, cache_read=M, output=M)
    assert old.uncached_input == pytest.approx(20.0)
    assert old.output == pytest.approx(40.0)  # period omitted `output`: the row's value stays
    assert old.cache_read == pytest.approx(1.0)  # ...and so does its absolute cache_read


def test_a_period_can_swap_in_its_own_bands_and_variants() -> None:
    rates = table(
        row(
            variants={"fast": {"input": 20.0, "output": 80.0}},
            periods=[
                {
                    "until": "2026-07-01",
                    "variants": {"fast": {"input": 99.0, "output": 99.0}},
                    "bands": [{"min_input_tokens": 100, "input": 70.0, "output": 70.0}],
                }
            ],
        )
    )
    assert input_per_m(rates, 100, when=at(2026, 6, 1)) == pytest.approx(70.0)
    assert input_per_m(rates, 99, when=at(2026, 6, 1), tier="fast") == pytest.approx(99.0)
    assert input_per_m(rates, 100, when=at(2026, 8, 1)) == pytest.approx(10.0)
    assert input_per_m(rates, 99, when=at(2026, 8, 1), tier="fast") == pytest.approx(20.0)


def test_price_event_uses_the_event_timestamp() -> None:
    old, _ = price_event(make_event("m", at(2026, 6, 1), uncached_input=M), PERIODS)
    new, _ = price_event(make_event("m", at(2026, 9, 1), uncached_input=M), PERIODS)
    assert old is not None and new is not None
    assert old.uncached_input == pytest.approx(20.0)
    assert new.uncached_input == pytest.approx(10.0)


# --- bands ------------------------------------------------------------------------------

BANDS = table(row(bands=[{"min_input_tokens": 200_001, "input": 20.0, "output": 60.0}]))


def test_band_applies_from_its_threshold_not_one_token_before() -> None:
    below = cost(BANDS, uncached_input=200_000, output=M)
    at_threshold = cost(BANDS, uncached_input=200_001, output=M)
    assert below.uncached_input == pytest.approx(200_000 * 10 / M)
    assert below.output == pytest.approx(40.0)
    assert at_threshold.uncached_input == pytest.approx(200_001 * 20 / M)
    assert at_threshold.output == pytest.approx(60.0)  # whole request, output included


def test_band_threshold_counts_cached_input_tokens_too() -> None:
    result = cost(BANDS, uncached_input=100_000, cache_read=100_001)
    assert result.uncached_input == pytest.approx(100_000 * 20 / M)


def test_bands_are_sorted_so_file_order_does_not_matter() -> None:
    rates = table(
        row(
            bands=[
                {"min_input_tokens": 1000, "input": 40.0, "output": 1.0},
                {"min_input_tokens": 100, "input": 30.0, "output": 1.0},
            ]
        )
    )
    assert input_per_m(rates, 99) == pytest.approx(10.0)
    assert input_per_m(rates, 500) == pytest.approx(30.0)
    assert input_per_m(rates, 5000) == pytest.approx(40.0)


BAND_VARIANTS = table(
    row(
        variants={"fast": {"input": 20.0, "output": 80.0}},
        bands=[
            {
                "min_input_tokens": 100,
                "input": 30.0,
                "output": 90.0,
                "variants": {"fast": {"input": 50.0, "output": 150.0}},
            },
            {"min_input_tokens": 1000, "input": 40.0, "output": 100.0},
        ],
    )
)


@pytest.mark.parametrize(
    "tokens,tier,expected",
    [
        (99, "standard", 10.0),
        (99, "fast", 20.0),
        (100, "standard", 30.0),
        (100, "fast", 50.0),  # the band's own variants win inside the band
        (1000, "standard", 40.0),
        (1000, "fast", 20.0),  # a band without `variants` falls back to the row's
    ],
)
def test_band_and_variant_interaction(tokens: int, tier: str, expected: float) -> None:
    assert input_per_m(BAND_VARIANTS, tokens, tier=tier) == pytest.approx(expected)


# --- tiers ------------------------------------------------------------------------------


def test_missing_tier_falls_back_to_standard_and_is_recorded() -> None:
    rates = table(row())
    result = cost(rates, tier="priority", uncached_input=M)
    assert result.uncached_input == pytest.approx(10.0)
    assert result.tier_unpriced is True
    assert cost(rates, tier="standard", uncached_input=M).tier_unpriced is False


def test_tier_unpriced_flag_survives_summing_and_stays_out_of_the_json() -> None:
    flagged = cost(table(row()), tier="flex", uncached_input=M)
    assert (flagged + CostBreakdown()).tier_unpriced is True
    assert "tier_unpriced" not in flagged.model_dump()


def test_tier_unpriced_models_reports_one_entry_per_model_and_tier_with_volume() -> None:
    rates = table(row("a"), row("b", variants={"fast": {"input": 1.0, "output": 1.0}}))
    events = []
    for model, tier, n in [("a", "priority", 100), ("a", "priority", 50), ("a", "flex", 7)] + [
        ("b", "fast", 9),
        ("b", "priority", 3),
    ]:
        event = make_event(model, tier=tier, uncached_input=n)
        result, state = price_event(event, rates)
        events.append(PricedEvent(event=event, cost=result, state=state))
    assert tier_unpriced_models(events) == {
        ("a", "priority"): 150,
        ("a", "flex"): 7,
        ("b", "priority"): 3,
    }


def test_batch_without_an_explicit_variant_uses_the_merged_batch_multiplier() -> None:
    result = cost(table(row()), tier="batch", uncached_input=M, output=M)
    assert result.uncached_input == pytest.approx(4.0)  # provider batch 0.4, not the 0.5 default
    assert result.output == pytest.approx(16.0)
    assert result.tier_unpriced is False


def test_an_explicit_batch_variant_is_not_discounted_again() -> None:
    rates = table(row(variants={"batch": {"input": 6.0, "output": 25.0}}))
    result = cost(rates, tier="batch", uncached_input=M, output=M)
    assert (result.uncached_input, result.output) == (pytest.approx(6.0), pytest.approx(25.0))


# --- peak -------------------------------------------------------------------------------

PEAK = table(
    row(
        peak={
            "weekdays": [0, 1, 2, 3, 4],
            "utc_hours": [[1, 4], [6, 10]],
            "input": 5.0,
            "output": 20.0,
        }
    )
)
MONDAY = (2026, 10, 5)
SATURDAY = (2026, 10, 10)


def test_peak_fixture_dates_are_the_weekdays_the_tests_assume() -> None:
    assert date(*MONDAY).weekday() == 0
    assert date(*SATURDAY).weekday() == 5


@pytest.mark.parametrize(
    "day,hour,minute,expected",
    [
        (MONDAY, 0, 59, 10.0),
        (MONDAY, 1, 0, 5.0),  # start inclusive
        (MONDAY, 3, 59, 5.0),
        (MONDAY, 4, 0, 10.0),  # end exclusive
        (MONDAY, 5, 30, 10.0),
        (MONDAY, 6, 0, 5.0),  # second range
        (MONDAY, 9, 59, 5.0),
        (MONDAY, 10, 0, 10.0),
        (SATURDAY, 2, 0, 10.0),  # weekend
    ],
)
def test_peak_window_is_weekday_and_half_open_utc_hours(
    day: tuple[int, int, int], hour: int, minute: int, expected: float
) -> None:
    when = at(*day, hour, minute)
    assert cost(PEAK, when=when, uncached_input=M).uncached_input == pytest.approx(expected)


def test_peak_is_read_in_utc_even_for_a_local_timestamp() -> None:
    local = datetime(*MONDAY, 3, 0, tzinfo=timezone(timedelta(hours=5)))  # 22:00 UTC Sunday
    assert cost(PEAK, when=local, uncached_input=M).uncached_input == pytest.approx(10.0)


def test_peak_price_replaces_the_tier_price() -> None:
    rates = table(
        row(
            variants={"fast": {"input": 20.0, "output": 80.0}},
            peak={"weekdays": [0], "utc_hours": [[0, 24]], "input": 5.0, "output": 20.0},
        )
    )
    when = at(*MONDAY, 12)
    assert cost(rates, when=when, tier="fast", uncached_input=M).uncached_input == pytest.approx(
        5.0
    )


# --- cache rules and cache price resolution ---------------------------------------------


def test_partial_cache_rules_merge_over_the_provider_block_not_class_defaults() -> None:
    rates = table(row(cache_rules={"cache_read": 0.25}))
    result = cost(rates, cache_read=M, cache_write_1h=M)
    assert result.cache_read == pytest.approx(2.5)
    # the provider's 1.5x, not ProviderRules' class default of 2.0x (the old trap)
    assert result.cache_write == pytest.approx(15.0)
    assert cost(rates, tier="batch", uncached_input=M).uncached_input == pytest.approx(4.0)


def test_merge_rules_overrides_only_the_fields_that_are_set() -> None:
    base = ProviderRules(cache_read=0.1, cache_write_5m=1.25, cache_write_1h=1.5, batch=0.4)
    merged = merge_rules(base, PartialRules(batch=1.0))
    assert (merged.cache_read, merged.cache_write_1h, merged.batch) == (0.1, 1.5, 1.0)
    assert merge_rules(base, None) is base


def test_a_full_v1_style_cache_rules_block_still_replaces_every_field() -> None:
    rates = table(
        row(
            cache_rules={
                "cache_read": 0.5,
                "cache_write_5m": 2.0,
                "cache_write_1h": 3.0,
                "batch": 0.9,
            }
        )
    )
    result = cost(rates, cache_read=M, cache_write_5m=M, cache_write_1h=M)
    assert (result.cache_read, result.cache_write) == (pytest.approx(5.0), pytest.approx(20 + 30))


ABSOLUTE = table(
    row(
        cache_read=1.0,
        cache_write_5m=12.5,
        variants={
            "fast": {"input": 20.0, "output": 80.0},
            "flex": {"input": 5.0, "output": 20.0, "cache_read": 0.3},
        },
    ),
    row(
        "plain",
        variants={"fast": {"input": 20.0, "output": 80.0}},
    ),
)


def test_absolute_cache_prices_are_used_as_published() -> None:
    result = cost(ABSOLUTE, cache_read=M, cache_write_5m=M, cache_write_1h=M)
    assert result.cache_read == pytest.approx(1.0)
    assert result.cache_write == pytest.approx(12.5 + 15.0)  # 1h has no figure: 10 x 1.5


def test_a_variant_without_cache_fields_keeps_the_rows_cache_to_input_ratio() -> None:
    result = cost(ABSOLUTE, tier="fast", cache_read=M, cache_write_5m=M, cache_write_1h=M)
    assert result.cache_read == pytest.approx(1.0 / 10 * 20)
    assert result.cache_write == pytest.approx(12.5 / 10 * 20 + 20 * 1.5)


def test_a_variants_own_absolute_cache_price_beats_the_ratio() -> None:
    result = cost(ABSOLUTE, tier="flex", cache_read=M, cache_write_5m=M)
    assert result.cache_read == pytest.approx(0.3)
    assert result.cache_write == pytest.approx(12.5 / 10 * 5)


def test_a_row_without_any_absolute_cache_price_uses_the_merged_multipliers() -> None:
    result = cost(ABSOLUTE, "plain", tier="fast", cache_read=M, cache_write_1h=M)
    assert result.cache_read == pytest.approx(2.0)  # 20 x 0.1
    assert result.cache_write == pytest.approx(30.0)  # 20 x 1.5


def test_batch_halves_absolute_cache_prices_along_with_input_and_output() -> None:
    result = cost(ABSOLUTE, tier="batch", cache_read=M, cache_write_5m=M, cache_write_1h=M)
    assert result.cache_read == pytest.approx(1.0 * 0.4)
    assert result.cache_write == pytest.approx(12.5 * 0.4 + 10 * 0.4 * 1.5)


def test_band_cache_prices_derive_from_the_band_input_when_unset() -> None:
    rates = table(
        row(
            cache_read=1.0,
            bands=[{"min_input_tokens": 10, "input": 20.0, "output": 80.0}],
        )
    )
    result = cost(rates, cache_read=10)
    assert result.cache_read == pytest.approx(10 * 2.0 / M)


def test_no_cache_equivalent_bills_all_input_at_the_resolved_input_price() -> None:
    result = cost(BANDS, uncached_input=100_000, cache_read=100_001, output=M)
    assert result.no_cache_equivalent == pytest.approx(200_001 * 20 / M + 60.0)


# --- v1 file compatibility --------------------------------------------------------------


V1_PATH = FIXTURES / "rates_v1.json"


def _old_cost(
    raw: dict, rate: dict, providers: dict, tier: str, tokens: TokenUsage
) -> tuple[float, float, float, float]:
    """The pre-v2 arithmetic, re-stated independently of pricing.py."""
    base = providers.get(rate["provider"], {})
    defaults = {"cache_read": 0.1, "cache_write_5m": 1.25, "cache_write_1h": 2.0, "batch": 0.5}
    rules = {**defaults, **(rate.get("cache_rules") or base)}
    variant = rate.get("variants", {}).get(tier, {"input": rate["input"], "output": rate["output"]})
    discount = rules["batch"] if tier == "batch" else 1.0
    in_price = variant["input"] * discount / MILLION
    out_price = variant["output"] * discount / MILLION
    return (
        tokens.uncached_input * in_price,
        tokens.cache_read * in_price * rules["cache_read"],
        tokens.cache_write_5m * in_price * rules["cache_write_5m"]
        + tokens.cache_write_1h * in_price * rules["cache_write_1h"],
        tokens.output * out_price,
    )


def test_the_v1_rates_file_still_loads_and_prices_every_row_identically() -> None:
    raw = json.loads(V1_PATH.read_text("utf-8"))
    rates = RateTable.load(V1_PATH)
    tokens = TokenUsage(
        uncached_input=1_234_567,
        cache_read=2_345_678,
        cache_write_5m=345_678,
        cache_write_1h=456_789,
        output=567_890,
    )
    assert len(rates.models) == len(raw["models"])
    for source in raw["models"]:
        found = rates.lookup(source["match"])
        assert found is not None and found.match_kind == "exact"
        for tier in ("standard", "fast", "batch", "flex"):
            expected = _old_cost(raw, source, raw["providers"], tier, tokens)
            got = cost_for(rates, source["match"], tier, tokens)
            assert (
                got.uncached_input,
                got.cache_read,
                got.cache_write,
                got.output,
            ) == pytest.approx(expected), (source["match"], tier)


def cost_for(rates: RateTable, model: str, tier: str, tokens: TokenUsage) -> CostBreakdown:
    result, state = price_event(
        UsageEvent(
            source="s",
            client="c",
            model=model,
            timestamp=at(2026, 10, 1),
            session_id="s",
            tokens=tokens,
            tier=tier,
        ),
        rates,
    )
    assert state == "priced" and result is not None
    return result


def test_known_v1_totals_are_unchanged() -> None:
    rates = RateTable.load(V1_PATH)
    everything = TokenUsage(
        uncached_input=M, cache_read=M, cache_write_5m=M, cache_write_1h=M, output=M
    )
    assert cost_for(rates, "claude-opus-5", "standard", everything).total == pytest.approx(46.75)
    # gpt-5.6-sol: 4 input, 20 output, openai block 0.1 / 1.25 / 1.25
    assert cost_for(rates, "gpt-5.6-sol", "standard", everything).total == pytest.approx(
        4.0 + 0.4 + 5.0 + 5.0 + 20.0
    )
    assert cost_for(rates, "claude-opus-5", "fast", TokenUsage(output=M)).total == pytest.approx(
        50.0
    )


# --- matching ---------------------------------------------------------------------------

MATCH_TABLE = table(
    row("model-x"),
    row("claude-opus-4-5"),
    row("claude-sonnet-4-5"),
    row("claude-sonnet-4-6"),
    row("claude-opus-5-5"),
    row("gpt-5.6"),
    row("gpt-5.6-sol"),
    row("nova-pro"),
    row("qwen3.8-max"),
    row("glm-5.3"),
    row("minimax-m3"),
)

MATCH_CASES = [
    # exact
    ("claude-opus-4-5", "claude-opus-4-5", "exact"),
    ("  Claude-Opus-4-5  ", "claude-opus-4-5", "exact"),
    ("gpt-5.6-sol", "gpt-5.6-sol", "exact"),
    ("gpt-5.6", "gpt-5.6", "exact"),
    # benign suffixes
    ("claude-opus-4-5-20251101", "claude-opus-4-5", "suffix"),
    ("model-x[1m]", "model-x", "suffix"),
    ("model-x-v1:0", "model-x", "suffix"),
    ("model-x-v2", "model-x", "suffix"),
    ("model-x-latest", "model-x", "suffix"),
    ("model-x@20260101", "model-x", "suffix"),
    ("model-x-20260101", "model-x", "suffix"),
    ("model-x-2026-01-01", "model-x", "suffix"),
    ("model-x-20260101-v1:0", "model-x", "suffix"),
    ("model-x[1m]-latest", "model-x", "suffix"),
    # anything else is a guess
    ("model-x-mini", "model-x", "estimated"),
    ("model-x.7", "model-x", "estimated"),
    ("model-x-5", "model-x", "estimated"),
    ("model-x:free", "model-x", "estimated"),
    ("model-x-preview", "model-x", "estimated"),
    ("model-x-2026", "model-x", "estimated"),
    ("model-x-20260101-mini", "model-x", "estimated"),
    ("claude-opus-4-5-5", "claude-opus-4-5", "estimated"),
    # gateway prefixes, stacked and Bedrock-style
    ("openrouter/anthropic/claude-opus-4-5", "claude-opus-4-5", "exact"),
    ("us.anthropic.claude-opus-4-5-v1:0", "claude-opus-4-5", "suffix"),
    ("us.anthropic.claude-opus-4-5-20251101-v1:0", "claude-opus-4-5", "suffix"),
    ("global.anthropic.claude-opus-4-5", "claude-opus-4-5", "exact"),
    ("anthropic.claude-opus-4-5-v1:0", "claude-opus-4-5", "suffix"),
    # dotted Claude ids are the same model; other vendors keep their dots
    ("claude-sonnet-4.6", "claude-sonnet-4-6", "exact"),
    ("anthropic/claude-sonnet-4.5", "claude-sonnet-4-5", "exact"),
    ("openrouter/anthropic/claude-opus-5.5", "claude-opus-5-5", "exact"),
    ("claude-sonnet-4.6-20260101", "claude-sonnet-4-6", "suffix"),
    # newer vendors' prefixes
    ("qwen/qwen3.8-max", "qwen3.8-max", "exact"),
    ("z-ai/glm-5.3", "glm-5.3", "exact"),
    ("us.amazon.nova-pro-v1:0", "nova-pro", "suffix"),
    ("global.amazon.nova-pro-v1:0", "nova-pro", "suffix"),
    ("amazon.nova-pro-v1:0", "nova-pro", "suffix"),
    ("minimax/MiniMax-M3", "minimax-m3", "exact"),
]


@pytest.mark.parametrize("raw,match,kind", MATCH_CASES)
def test_match_kinds(raw: str, match: str, kind: str) -> None:
    found = MATCH_TABLE.lookup(raw)
    assert found is not None, raw
    assert (found.match, found.match_kind) == (match, kind)
    assert found.estimated is (kind == "estimated")
    assert MATCH_TABLE.match_of(raw).model_dump() == {"match": match, "kind": kind}


def test_an_unmatched_model_has_no_kind() -> None:
    assert MATCH_TABLE.lookup("something-else") is None
    assert MATCH_TABLE.match_of("something-else").model_dump() == {"match": None, "kind": "none"}
    assert MATCH_TABLE.match_of(None).kind == "none"


@pytest.mark.parametrize("entry", BUILTIN_PREFIXES, ids=lambda entry: entry.prefix)
def test_every_builtin_gateway_prefix_is_stripped(entry: Prefix) -> None:
    found = MATCH_TABLE.lookup(f"{entry.prefix}model-x")
    assert found is not None
    assert found.match_kind == "exact"


def test_the_dot_rewrite_is_claude_only() -> None:
    assert normalise_model("Claude-Sonnet-4.6", []) == "claude-sonnet-4-6"
    assert normalise_model("gpt-5.6-sol", []) == "gpt-5.6-sol"
    assert normalise_model("gemini-3.1-pro", []) == "gemini-3.1-pro"
    assert MATCH_TABLE.lookup("gpt-5-6-sol") is None  # dots are not rewritten for gpt


def test_prefix_stripping_repeats_and_prefers_the_longest_match() -> None:
    prefixes = effective_prefixes([])
    lengths = [len(entry.prefix) for entry in prefixes]
    assert lengths == sorted(lengths, reverse=True)
    names = [entry.prefix for entry in prefixes]
    assert names.index("us.anthropic.") < names.index("anthropic.")
    assert normalise_model("openrouter/openai/azure/gpt-x", prefixes) == "gpt-x"
    assert normalise_model("us.anthropic.claude-opus-4-5", prefixes) == "claude-opus-4-5"


def test_file_prefixes_win_over_builtin_ones_and_can_add_new_ones() -> None:
    rates = table(
        row("model-x"),
        prefixes=[
            {"prefix": "azure/", "provider": None},
            {"prefix": "mycorp/", "provider": "mycorp"},
        ],
    )
    assert rates.lookup("mycorp/model-x") is not None
    assert resolve_provider(None, "azure/model-x", rates) == "acme"  # file entry: no provider
    assert resolve_provider(None, "mycorp/model-x", rates) == "mycorp"


@pytest.mark.parametrize(
    "raw,provider",
    [
        ("us.anthropic.model-x", "bedrock"),
        ("eu.anthropic.model-x", "bedrock"),
        ("global.anthropic.model-x", "bedrock"),
        ("apac.anthropic.model-x", "bedrock"),
        ("au.anthropic.model-x", "bedrock"),
        ("jp.anthropic.model-x", "bedrock"),
        ("us.amazon.model-x", "bedrock"),
        ("amazon.model-x", "bedrock"),
        ("openrouter/model-x", "openrouter"),
        ("openrouter/anthropic/model-x", "openrouter"),
        ("azure/model-x", "azure"),
        ("anthropic/model-x", "acme"),  # null-provider prefix: the row decides
        ("xai/model-x", "acme"),
        ("model-x", "acme"),
        ("nothing-like-it", "unknown"),
    ],
)
def test_gateway_prefixes_map_to_providers(raw: str, provider: str) -> None:
    assert resolve_provider(None, raw, table(row("model-x"))) == provider


def test_a_declared_provider_always_wins() -> None:
    assert resolve_provider("mine", "us.anthropic.model-x", table(row("model-x"))) == "mine"


def test_an_unpriced_entry_beats_an_estimated_parent_match() -> None:
    rates = table(
        row("gpt-x"),
        unpriced_models=[
            {"match": "gpt-x-spark", "note": "no list price", "status": "no_list_price"},
            {"match": "gpt-y", "note": "watching", "status": "watchlist"},
        ],
    )
    assert rates.lookup("gpt-x-spark") is None
    assert rates.lookup("gpt-x-spark-preview") is None
    assert rates.unpriced_note("gpt-x-spark") == "no list price"
    assert rates.lookup("gpt-x-mini") is not None  # an unrelated guess is still estimated
    assert rates.unpriced_models[1].status == "watchlist"
    event = make_event("gpt-x-spark", uncached_input=10)
    assert price_event(event, rates) == (None, "unpriced")


def test_an_unpriced_entry_as_long_as_the_row_also_beats_an_estimated_match() -> None:
    rates = table(row("gpt-x"), unpriced_models=[{"match": "gpt-x", "note": "pulled"}])
    assert rates.lookup("gpt-x-mini") is None
    exact = rates.lookup("gpt-x")
    assert exact is not None and exact.match_kind == "exact"


def test_an_exact_or_suffix_match_on_a_real_row_always_beats_an_unpriced_entry() -> None:
    rates = table(
        row("gpt-x"),
        unpriced_models=[{"match": "gpt-x", "note": "n"}, {"match": "gpt-x-2026", "note": "n"}],
    )
    exact = rates.lookup("gpt-x")
    dated = rates.lookup("gpt-x-20260101")
    bracketed = rates.lookup("gpt-x[1m]")
    assert exact is not None and exact.match_kind == "exact"
    assert dated is not None and dated.match_kind == "suffix"
    assert bracketed is not None and bracketed.match_kind == "suffix"


def test_an_unpriced_entry_without_any_row_stays_unpriced() -> None:
    rates = table(row("other"), unpriced_models=[{"match": "gemini-4", "note": "no API id yet"}])
    assert rates.lookup("gemini-4-argon") is None
    assert rates.unpriced_note("gemini-4-argon") == "no API id yet"


def test_display_name_shows_the_row_for_exact_and_suffix_but_the_raw_id_for_estimated() -> None:
    rates = table(row("model-x", display="Model X"))
    assert rates.display_name("model-x") == "Model X"
    assert rates.display_name("model-x-20260101") == "Model X"
    assert rates.display_name("model-x[1m]") == "Model X"
    assert rates.display_name("model-x-mini") == "model-x-mini"
    assert rates.display_name("nothing") == "nothing"
    assert rates.display_name(None) == "unknown model"


def test_lookup_caches_per_raw_string() -> None:
    rates = table(row("model-x"))
    first = rates.lookup("openrouter/model-x")
    assert rates.lookup("openrouter/model-x") is first
    # pylint: disable=protected-access
    assert set(rates._lookup_cache) == {"openrouter/model-x"}


# --- estimated flag, warnings, report ---------------------------------------------------


def test_only_estimated_matches_set_the_flag() -> None:
    rates = table(row("model-x"))
    flags = {
        raw: cost(rates, raw, uncached_input=10).estimated
        for raw in ("model-x", "model-x-20260101", "model-x[1m]", "model-x-mini")
    }
    assert flags == {
        "model-x": False,
        "model-x-20260101": False,
        "model-x[1m]": False,
        "model-x-mini": True,
    }


def test_estimated_models_lists_only_estimated_ids_with_their_volume() -> None:
    rates = table(row("model-x"))
    events = []
    for model, n in [
        ("model-x-mini", 100),
        ("model-x-mini", 20),
        ("model-x-20260101", 5),
        ("model-x", 1),
    ]:
        event = make_event(model, uncached_input=n)
        result, state = price_event(event, rates)
        events.append(PricedEvent(event=event, cost=result, state=state))
    assert estimated_models(events) == {"model-x-mini": 120}


def _priced(rates: RateTable, model: str, session: str = "s1", **kwargs: object) -> PricedEvent:
    event = make_event(model, uncached_input=1000, output=500).model_copy(
        update={"session_id": session, **kwargs}
    )
    result, state = price_event(event, rates)
    return PricedEvent(event=event, cost=result, state=state)


def test_model_matches_covers_every_model_in_by_model() -> None:
    rates = table(row("model-x", display="Model X"))
    priced = [
        _priced(rates, "model-x"),
        _priced(rates, "model-x-20260101"),
        _priced(rates, "model-x-mini"),
        _priced(rates, "unheard-of"),
    ]
    report = build_report(
        priced,
        client_labels={},
        model_label=rates.display_name,
        model_match=rates.match_of,
        rates_age_days=12,
    )
    assert {bucket.key for bucket in report.by_model} == set(report.model_matches)
    assert {key: found.model_dump() for key, found in report.model_matches.items()} == {
        "model-x": {"match": "model-x", "kind": "exact"},
        "model-x-20260101": {"match": "model-x", "kind": "suffix"},
        "model-x-mini": {"match": "model-x", "kind": "estimated"},
        "unheard-of": {"match": None, "kind": "none"},
    }
    labels = {bucket.key: bucket.label for bucket in report.by_model}
    assert labels["model-x-20260101"] == "Model X"
    assert labels["model-x-mini"] == "model-x-mini"  # estimated: shown under its own id
    assert report.rates_age_days == 12


def test_build_report_without_a_match_callable_has_no_model_matches() -> None:
    rates = table(row("model-x"))
    report = build_report([_priced(rates, "model-x")], client_labels={}, model_label=str)
    assert report.model_matches == {}
    assert report.rates_age_days is None


# --- reported cost ----------------------------------------------------------------------


def _with_reported(
    rates: RateTable, model: str, session: str, reported: float | None
) -> PricedEvent:
    return _priced(rates, model, session, reported_cost=reported)


def test_reported_cost_is_summed_per_bucket_session_and_total() -> None:
    rates = table(row("a"), row("b"))
    priced = [
        _with_reported(rates, "a", "s1", 1.0),
        _with_reported(rates, "a", "s1", 2.0),
        _with_reported(rates, "b", "s1", None),
        _with_reported(rates, "b", "s2", None),
    ]
    report = build_report(priced, client_labels={}, model_label=str)
    assert report.totals.reported_cost == pytest.approx(3.0)
    by_model = {bucket.key: bucket.reported_cost for bucket in report.by_model}
    assert by_model == {"a": pytest.approx(3.0), "b": None}
    by_session = {row_.session_id: row_.reported_cost for row_ in report.sessions}
    assert by_session == {"s1": pytest.approx(3.0), "s2": None}
    assert report.by_provider[0].reported_cost == pytest.approx(3.0)
    assert report.by_day[0].reported_cost == pytest.approx(3.0)


def test_no_reported_cost_anywhere_stays_none() -> None:
    rates = table(row("a"))
    report = build_report(
        [_with_reported(rates, "a", "s1", None)], client_labels={}, model_label=str
    )
    assert report.totals.reported_cost is None
    assert report.sessions[0].reported_cost is None


@pytest.mark.parametrize(
    "reported,computed_tokens,diverges",
    [
        (1.0, 1.04, False),  # within 5%
        (1.0, 1.06, True),
        (1.0, 0.94, True),
        (0.001, 0.005, False),  # tiny: inside the $0.01 floor
        (0.0, 0.02, True),
        (100.0, 104.0, False),
        (100.0, 106.0, True),
    ],
)
def test_reported_cost_divergence_threshold(
    reported: float, computed_tokens: float, diverges: bool
) -> None:
    rates = table(row("a"))
    # 1M uncached tokens at $10/M compute to $10; scale tokens to hit the computed target
    tokens = int(computed_tokens / 10 * M)
    event = make_event("a", uncached_input=tokens).model_copy(update={"reported_cost": reported})
    result, state = price_event(event, rates)
    messages = reported_cost_divergences([PricedEvent(event=event, cost=result, state=state)])
    assert bool(messages) is diverges


def test_divergence_message_names_the_session_and_both_figures() -> None:
    rates = table(row("a"))
    event = make_event("a", uncached_input=M).model_copy(
        update={"reported_cost": 3.0, "session_id": "sess-9"}
    )
    result, state = price_event(event, rates)
    (message,) = reported_cost_divergences([PricedEvent(event=event, cost=result, state=state)])
    assert "sess-9" in message and "$3.0000" in message and "$10.0000" in message
    group = warning_groups_of([message])[0]
    assert group.kind == "reported_cost_divergence"
    assert group.instances[0].session_id == "sess-9"


def test_divergence_ignores_events_without_a_reported_figure() -> None:
    rates = table(row("a"))
    priced = [
        _with_reported(rates, "a", "s1", None),
        _with_reported(rates, "a", "s1", 0.0125),  # computed: 1000 in + 500 out = $0.03
    ]
    # only the event that carries both figures is compared: 0.0125 vs 0.03 -> diverges
    assert len(reported_cost_divergences(priced)) == 1


# --- staleness --------------------------------------------------------------------------


def _analyze(tmp_path: Path, as_of: str, today: date) -> Analysis:
    rates = tmp_path / "rates.json"
    rates.write_text(json.dumps({"as_of": as_of, "providers": {}, "models": []}), "utf-8")
    roots = {
        source_id: [NO_ROOT]
        for source_id in __import__("ai_usage_cost.sources", fromlist=["registry"]).registry()
    }
    return analyze(db_path=tmp_path / "usage.db", roots=roots, rates_path=rates, today=today)


def _stale(found: Analysis) -> list[str]:
    return [w for w in found.warnings if w.startswith("rates.json is ")]


@pytest.mark.parametrize(
    "today,age,severity",
    [
        (date(2026, 10, 1), 30, None),
        (date(2026, 10, 2), 31, "info"),
        (date(2026, 11, 30), 90, "info"),
        (date(2026, 12, 1), 91, "caution"),
    ],
)
def test_stale_rates_thresholds_with_an_injected_today(
    tmp_path: Path, today: date, age: int, severity: str | None
) -> None:
    found = _analyze(tmp_path, "2026-09-01", today)
    assert found.rates_age_days == age
    warnings = _stale(found)
    if severity is None:
        assert warnings == []
        return
    (message,) = warnings
    assert "2026-09-01" in message and f"{age} days" in message
    group = warning_groups_of([message])[0]
    assert group.kind == "stale_rates"
    assert group.severity.value == severity


@pytest.mark.parametrize("as_of", ["", "not a date", "2026-13-45"])
def test_no_stale_warning_without_a_usable_as_of(tmp_path: Path, as_of: str) -> None:
    found = _analyze(tmp_path, as_of, date(2030, 1, 1))
    assert found.rates_age_days is None
    assert _stale(found) == []


def test_report_carries_the_rates_age(tmp_path: Path) -> None:
    from ai_usage_cost.pipeline import report_of

    found = _analyze(tmp_path, "2026-09-01", date(2026, 10, 11))
    assert report_of(found).rates_age_days == 40


# --- sources ----------------------------------------------------------------------------


def test_source_experimental_defaults_to_false_and_reaches_source_info(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake(id_: str, experimental: bool | None) -> Source:
        kwargs = {} if experimental is None else {"experimental": experimental}
        return Source(
            id=id_,
            label=id_,
            clients={id_: id_},
            default_roots=lambda: [],
            files=lambda _root: [],
            parse=lambda _path, _warnings: iter(()),
            token_data="full",
            display_path="-",
            **kwargs,  # type: ignore[arg-type]
        )

    sources = {s.id: s for s in (fake("plain", None), fake("beta", True), fake("stable", False))}
    monkeypatch.setattr("ai_usage_cost.pipeline.registry", lambda: sources)
    infos = {info.id: info.experimental for info in _sources_of(None, {})}
    assert infos == {"plain": False, "beta": True, "stable": False}


# --- trace ------------------------------------------------------------------------------


def _span(started_at: datetime, **detail: str) -> Span:
    return Span(
        span_id="sp",
        source="claude-code",
        session_id="s1",
        seq=0,
        kind="model_call",
        model="m",
        started_at=started_at,
        source_file="",
        record_offset=0,
        record_length=1,
        detail=detail,
        tokens=TokenUsage(uncached_input=M),
        tokens_provenance="measured",
    )


def test_span_pricing_uses_the_span_start_time_and_tier() -> None:
    rates = table(
        row(
            context_window=123_000,
            periods=[{"until": "2026-07-01", "input": 20.0, "output": 80.0}],
            variants={"fast": {"input": 30.0, "output": 90.0}},
        )
    )
    old, _ = trace_module._price_span(_span(at(2026, 6, 1)), rates)  # pylint: disable=protected-access
    new, _ = trace_module._price_span(_span(at(2026, 8, 1)), rates)  # pylint: disable=protected-access
    fast, _ = trace_module._price_span(_span(at(2026, 8, 1), tier="fast"), rates)  # pylint: disable=protected-access
    assert (old.uncached_input, new.uncached_input, fast.uncached_input) == pytest.approx(
        (20.0, 10.0, 30.0)
    )
    # the copy `lookup` returns still carries the window `_capacity_of` reads
    capacity = trace_module._capacity_of(_span(at(2026, 8, 1)), rates)  # pylint: disable=protected-access
    assert capacity == (123_000, "estimated")


# --- file validation (rejected at load, never priced by accident) ------------------------


def test_a_wrap_around_peak_range_is_rejected() -> None:
    with pytest.raises(ValueError, match="utc_hours"):
        table(row(peak={"weekdays": [0], "utc_hours": [[22, 2]], "input": 2.0, "output": 4.0}))


def test_peak_weekdays_must_be_monday_to_sunday() -> None:
    with pytest.raises(ValueError, match="weekdays"):
        table(row(peak={"weekdays": [7], "utc_hours": [[1, 4]], "input": 2.0, "output": 4.0}))


def test_a_period_must_start_before_it_ends() -> None:
    with pytest.raises(ValueError, match="earlier"):
        table(row(periods=[{"from": "2026-08-01", "until": "2026-08-01", "input": 1.0}]))


def test_overlapping_periods_are_rejected() -> None:
    with pytest.raises(ValueError, match="overlapping"):
        table(
            row(
                periods=[
                    {"from": "2026-01-01", "until": "2026-06-01", "input": 1.0},
                    {"from": "2026-05-01", "until": "2026-09-01", "input": 2.0},
                ]
            )
        )


def test_adjacent_periods_are_accepted() -> None:
    table(
        row(
            periods=[
                {"from": "2026-01-01", "until": "2026-06-01", "input": 1.0},
                {"from": "2026-06-01", "until": "2026-09-01", "input": 2.0},
            ]
        )
    )


def test_duplicate_match_keys_are_rejected() -> None:
    with pytest.raises(ValueError, match="duplicate"):
        table(row("a"), row("a"))


def test_a_row_with_an_undefined_provider_is_rejected() -> None:
    with pytest.raises(ValueError, match="undefined providers"):
        table(row("a", provider="no-such-provider"))


def test_a_free_models_reported_cost_is_not_a_divergence() -> None:
    rates = RateTable.model_validate(
        {
            "providers": {"local": {"free": True}},
            "models": [
                {"match": "local-m", "provider": "local", "display": "L", "input": 0, "output": 0}
            ],
        }
    )
    event = make_event("local-m", uncached_input=1000, output=500).model_copy(
        update={"reported_cost": 2.5, "provider": "local"}
    )
    result, state = price_event(event, rates)
    assert state == "free"
    assert reported_cost_divergences([PricedEvent(event=event, cost=result, state=state)]) == []
