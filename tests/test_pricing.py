"""Rate-table lookup and cost arithmetic.

Every dollar figure here is worked out by hand from ``rates.json`` and written as a
literal. Nothing in this module re-derives an expectation by calling the code it tests.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from ai_usage_cost.models import TokenUsage, UsageEvent
from ai_usage_cost.pricing import Pricer, RateTable, normalise_model
from conftest import CLAUDE_UNKNOWN, analyze_roots

M = 1_000_000


def event(model: str, tier: str = "standard", **tokens: int) -> UsageEvent:
    return UsageEvent(
        tool="claude-code",
        timestamp=datetime(2026, 8, 20, 10, 0, tzinfo=UTC),
        model=model,
        session_id="s1",
        tokens=TokenUsage(**tokens),
        tier=tier,
    )


# --------------------------------------------------------------------- multipliers


def test_anthropic_multipliers_price_each_bucket_separately() -> None:
    """Claude Opus 5 is $5 in / $25 out per 1M, 1M tokens in every bucket.

    uncached input  1M x $5                = $5.00
    cache read      1M x $5 x 0.1          = $0.50
    cache write 5m  1M x $5 x 1.25         = $6.25
    cache write 1h  1M x $5 x 2.0          = $10.00
    output          1M x $25               = $25.00
                                    total  = $46.75
    """
    cost = Pricer().price(
        event(
            "claude-opus-5",
            uncached_input=M,
            cache_read=M,
            cache_write_5m=M,
            cache_write_1h=M,
            output=M,
        )
    )
    assert cost is not None
    assert cost.uncached_input == pytest.approx(5.00)
    assert cost.cache_read == pytest.approx(0.50)
    assert cost.cache_write == pytest.approx(6.25 + 10.00)
    assert cost.output == pytest.approx(25.00)
    assert cost.total == pytest.approx(46.75)


def test_no_cache_equivalent_bills_every_input_token_at_the_full_input_rate() -> None:
    """4M input tokens x $5 + 1M output x $25 = $20.00 + $25.00 = $45.00.

    No cache-read discount and no cache-write premium appear in the baseline.
    """
    cost = Pricer().price(
        event(
            "claude-opus-5",
            uncached_input=M,
            cache_read=M,
            cache_write_5m=M,
            cache_write_1h=M,
            output=M,
        )
    )
    assert cost is not None
    assert cost.no_cache_equivalent == pytest.approx(45.00)
    # This mix pays more in write premium than it recovers in read discount.
    assert cost.cache_savings == pytest.approx(45.00 - 46.75)


def test_cache_savings_is_positive_when_reads_dominate() -> None:
    """200k uncached + 800k cache reads on Opus 5.

    billed   200k x $5 = $1.00  +  800k x $5 x 0.1 = $0.40   -> $1.40
    baseline 1M   x $5                                       -> $5.00
    savings                                                  -> $3.60
    """
    cost = Pricer().price(event("claude-opus-5", uncached_input=200_000, cache_read=800_000))
    assert cost is not None
    assert cost.total == pytest.approx(1.40)
    assert cost.no_cache_equivalent == pytest.approx(5.00)
    assert cost.cache_savings == pytest.approx(3.60)


def test_cache_write_premium_is_absent_from_the_no_cache_baseline() -> None:
    """Claude Sonnet 5 at $2 in: 100k uncached + 100k written to a 5m cache.

    billed   100k x $2 = $0.20  +  100k x $2 x 1.25 = $0.25  -> $0.45
    baseline 200k x $2                                       -> $0.40
    """
    cost = Pricer().price(
        event("claude-sonnet-5", uncached_input=100_000, cache_write_5m=100_000)
    )
    assert cost is not None
    assert cost.cache_write == pytest.approx(0.25)
    assert cost.total == pytest.approx(0.45)
    assert cost.no_cache_equivalent == pytest.approx(0.40)
    assert cost.cache_savings == pytest.approx(-0.05)


# --------------------------------------------------------------------------- tiers


def test_fast_tier_uses_the_opus_5_variant_rate() -> None:
    """The ``fast`` variant is $10 in / $50 out, multipliers unchanged.

    uncached 1M x $10        = $10.00
    read     1M x $10 x 0.1  =  $1.00
    write5m  1M x $10 x 1.25 = $12.50
    write1h  1M x $10 x 2.0  = $20.00
    output   1M x $50        = $50.00
                       total = $93.50
    """
    cost = Pricer().price(
        event(
            "claude-opus-5",
            tier="fast",
            uncached_input=M,
            cache_read=M,
            cache_write_5m=M,
            cache_write_1h=M,
            output=M,
        )
    )
    assert cost is not None
    assert cost.uncached_input == pytest.approx(10.00)
    assert cost.cache_read == pytest.approx(1.00)
    assert cost.cache_write == pytest.approx(12.50 + 20.00)
    assert cost.output == pytest.approx(50.00)
    assert cost.total == pytest.approx(93.50)
    assert cost.no_cache_equivalent == pytest.approx(40.00 + 50.00)


def test_batch_tier_halves_every_component() -> None:
    """Opus 5 has no batch variant, so the base $5/$25 is halved to $2.50/$12.50."""
    cost = Pricer().price(
        event(
            "claude-opus-5",
            tier="batch",
            uncached_input=M,
            cache_read=M,
            cache_write_5m=M,
            cache_write_1h=M,
            output=M,
        )
    )
    assert cost is not None
    assert cost.uncached_input == pytest.approx(2.50)
    assert cost.cache_read == pytest.approx(0.25)
    assert cost.cache_write == pytest.approx(3.125 + 5.00)
    assert cost.output == pytest.approx(12.50)
    assert cost.total == pytest.approx(23.375)
    assert cost.no_cache_equivalent == pytest.approx(10.00 + 12.50)


# ------------------------------------------------------------------ model matching


def test_dated_snapshot_resolves_to_the_longest_matching_family() -> None:
    table = RateTable.load()
    rate = table.lookup("claude-opus-4-5-20251101")
    assert rate is not None
    assert rate.match == "claude-opus-4-5"
    assert rate.display == "Claude Opus 4.5"
    # $5/$25, not the $15/$75 of the shorter "claude-opus-4" entry it also prefixes.
    assert (rate.input, rate.output) == (5.0, 25.0)


def test_plain_opus_4_still_resolves_to_the_opus_4_entry() -> None:
    rate = RateTable.load().lookup("claude-opus-4-20250514")
    assert rate is not None
    assert rate.match == "claude-opus-4"
    assert (rate.input, rate.output) == (15.0, 75.0)


def test_sonnet_5_does_not_fall_into_sonnet_4_6() -> None:
    rate = RateTable.load().lookup("claude-sonnet-5")
    assert rate is not None
    assert rate.match == "claude-sonnet-5"
    assert rate.display == "Claude Sonnet 5"
    assert (rate.input, rate.output) == (2.0, 10.0)


@pytest.mark.parametrize(
    "raw",
    [
        "claude-opus-5",
        "anthropic/claude-opus-5",
        "us.anthropic.claude-opus-5",
        "eu.anthropic.claude-opus-5-20260101",
        "  Claude-Opus-5  ",
    ],
)
def test_provider_prefixes_and_case_normalise_to_the_same_rate(raw: str) -> None:
    assert normalise_model(raw).startswith("claude-opus-5")
    rate = RateTable.load().lookup(raw)
    assert rate is not None
    assert rate.match == "claude-opus-5"


def test_openai_prefix_is_stripped() -> None:
    rate = RateTable.load().lookup("openai/gpt-5-codex")
    assert rate is not None
    assert rate.match == "gpt-5-codex"
    assert rate.provider == "openai"


# ------------------------------------------------------------------ unknown models


def test_unknown_model_is_not_priced_and_is_recorded_with_its_tokens() -> None:
    pricer = Pricer()
    unpriceable = event(
        "moonshot-v9-turbo", uncached_input=1000, cache_read=2000, output=500
    )

    assert pricer.price(unpriceable) is None
    assert pricer.unknown_models["moonshot-v9-turbo"].total == 3500

    pricer.price(unpriceable)
    assert pricer.unknown_models["moonshot-v9-turbo"].total == 7000
    assert pricer.unknown_events["moonshot-v9-turbo"] == 2


def test_unknown_model_is_excluded_from_totals_but_reported() -> None:
    """The fixture has one Opus 5 record (100 in / 100 out) and one unknown model."""
    found = analyze_roots(claude=CLAUDE_UNKNOWN)

    assert [item.event.model for item in found.priced] == ["claude-opus-5"]
    assert found.priced[0].event.tokens.total == 200

    unknown = found.unknown_models()
    assert len(unknown) == 1
    assert unknown[0].model == "moonshot-v9-turbo"
    assert unknown[0].tokens == 3500
    assert unknown[0].events == 1
    assert any("moonshot-v9-turbo" in warning for warning in found.warnings)


def test_display_name_and_provider_fall_back_for_unknown_models() -> None:
    pricer = Pricer()
    assert pricer.display_name("claude-opus-5") == "Claude Opus 5"
    assert pricer.provider_of("claude-opus-5") == "anthropic"
    assert pricer.display_name("moonshot-v9-turbo") == "moonshot-v9-turbo"
    assert pricer.provider_of("moonshot-v9-turbo") == "unknown"
