from __future__ import annotations

from datetime import UTC, datetime

import pytest

from ai_usage_cost.models import CostBreakdown, TokenUsage, UsageEvent
from ai_usage_cost.pricing import RateTable, price_event, resolve_provider
from conftest import CLAUDE_UNKNOWN, analyze_roots

M = 1_000_000


def event(
    model: str | None, tier: str = "standard", provider: str | None = None, **tokens: int
) -> UsageEvent:
    return UsageEvent(
        source="claude-code",
        client="claude-code",
        provider=provider,
        timestamp=datetime(2026, 8, 20, 10, 0, tzinfo=UTC),
        model=model,
        session_id="s1",
        tokens=TokenUsage(**tokens),
        tier=tier,
    )


TABLE = RateTable.load()


def price(**kwargs: object) -> CostBreakdown:
    cost, state = price_event(event(**kwargs), TABLE)  # type: ignore[arg-type]
    assert state == "priced"
    assert cost is not None
    return cost


def test_anthropic_multipliers_price_each_bucket_separately() -> None:
    cost = price(
        model="claude-opus-5",
        uncached_input=M, cache_read=M, cache_write_5m=M, cache_write_1h=M, output=M,
    )
    assert cost.uncached_input == pytest.approx(5.00)
    assert cost.cache_read == pytest.approx(0.50)
    assert cost.cache_write == pytest.approx(6.25 + 10.00)
    assert cost.output == pytest.approx(25.00)
    assert cost.total == pytest.approx(46.75)


def test_no_cache_equivalent_bills_every_input_token_at_the_full_input_rate() -> None:
    cost = price(
        model="claude-opus-5",
        uncached_input=M, cache_read=M, cache_write_5m=M, cache_write_1h=M, output=M,
    )
    assert cost.no_cache_equivalent == pytest.approx(45.00)
    assert cost.cache_savings == pytest.approx(45.00 - 46.75)


def test_cache_savings_is_positive_when_reads_dominate() -> None:
    cost = price(model="claude-opus-5", uncached_input=200_000, cache_read=800_000)
    assert cost.total == pytest.approx(1.40)
    assert cost.no_cache_equivalent == pytest.approx(5.00)
    assert cost.cache_savings == pytest.approx(3.60)


def test_cache_write_premium_is_absent_from_the_no_cache_baseline() -> None:
    cost = price(model="claude-sonnet-5", uncached_input=100_000, cache_write_5m=100_000)
    assert cost.cache_write == pytest.approx(0.25)
    assert cost.total == pytest.approx(0.45)
    assert cost.no_cache_equivalent == pytest.approx(0.40)
    assert cost.cache_savings == pytest.approx(-0.05)


def test_fast_tier_uses_the_opus_5_variant_rate() -> None:
    cost = price(
        model="claude-opus-5", tier="fast",
        uncached_input=M, cache_read=M, cache_write_5m=M, cache_write_1h=M, output=M,
    )
    assert cost.uncached_input == pytest.approx(10.00)
    assert cost.total == pytest.approx(93.50)


def test_batch_tier_halves_every_component() -> None:
    cost = price(
        model="claude-opus-5", tier="batch",
        uncached_input=M, cache_read=M, cache_write_5m=M, cache_write_1h=M, output=M,
    )
    assert cost.uncached_input == pytest.approx(2.50)
    assert cost.total == pytest.approx(23.375)


def test_dated_snapshot_resolves_to_the_longest_matching_family() -> None:
    rate = TABLE.lookup("claude-opus-4-5-20251101")
    assert rate is not None
    assert rate.match == "claude-opus-4-5"
    assert (rate.input, rate.output) == (5.0, 25.0)


def test_plain_opus_4_still_resolves_to_the_opus_4_entry() -> None:
    rate = TABLE.lookup("claude-opus-4-20250514")
    assert rate is not None
    assert rate.match == "claude-opus-4"
    assert (rate.input, rate.output) == (15.0, 75.0)


def test_sonnet_5_does_not_fall_into_sonnet_4_6() -> None:
    rate = TABLE.lookup("claude-sonnet-5")
    assert rate is not None
    assert rate.match == "claude-sonnet-5"
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
    rate = TABLE.lookup(raw)
    assert rate is not None
    assert rate.match == "claude-opus-5"


def test_openai_prefix_is_stripped() -> None:
    rate = TABLE.lookup("openai/gpt-5-codex")
    assert rate is not None
    assert rate.match == "gpt-5-codex"
    assert rate.provider == "openai"


def test_bedrock_prefix_resolves_the_gateway_provider() -> None:
    assert resolve_provider(None, "us.anthropic.claude-opus-5", TABLE) == "bedrock"


def test_declared_provider_wins_over_prefix() -> None:
    assert resolve_provider("anthropic", "us.anthropic.claude-opus-5", TABLE) == "anthropic"


def test_provider_falls_back_to_the_matched_rate_when_no_prefix() -> None:
    assert resolve_provider(None, "claude-opus-5", TABLE) == "anthropic"


def test_provider_is_unknown_when_nothing_resolves_it() -> None:
    assert resolve_provider(None, "moonshot-v9-turbo-not-a-real-model", TABLE) == "unknown"


def test_unknown_model_is_not_priced() -> None:
    unpriceable = event(model="moonshot-v9-turbo", uncached_input=1000, cache_read=2000, output=500)
    cost, state = price_event(unpriceable, TABLE)
    assert cost is None
    assert state == "unpriced"


def test_unknown_model_is_excluded_from_totals_but_reported() -> None:
    found = analyze_roots(**{"claude-code": CLAUDE_UNKNOWN})
    priced = [item for item in found.events if item.state == "priced"]

    assert [item.event.model for item in priced] == ["claude-opus-5"]
    assert priced[0].event.tokens.total == 200

    unknown = found.unknown_models()
    assert len(unknown) == 1
    assert unknown[0].model == "moonshot-v9-turbo"
    assert unknown[0].tokens == 3500
    assert unknown[0].events == 1
    assert any("moonshot-v9-turbo" in warning for warning in found.warnings)


def test_display_name_falls_back_for_unknown_models() -> None:
    assert TABLE.display_name("claude-opus-5") == "Claude Opus 5"
    assert TABLE.display_name("moonshot-v9-turbo") == "moonshot-v9-turbo"
    assert TABLE.display_name(None) == "unknown model"


def test_tokens_none_is_the_unavailable_state() -> None:
    unavailable = UsageEvent(
        source="dyad", client="dyad", model=None,
        timestamp=datetime(2026, 8, 20, 10, 0, tzinfo=UTC), session_id="s1", tokens=None,
    )
    cost, state = price_event(unavailable, TABLE)
    assert cost is None
    assert state == "unavailable"


def test_free_provider_prices_at_zero() -> None:
    local = UsageEvent(
        source="ollama-app", client="ollama-app", provider="local", model="llama3",
        timestamp=datetime(2026, 8, 20, 10, 0, tzinfo=UTC), session_id="s1",
        tokens=TokenUsage(uncached_input=1000, output=500),
    )
    cost, state = price_event(local, TABLE)
    assert state == "free"
    assert cost is not None
    assert cost.total == 0.0
