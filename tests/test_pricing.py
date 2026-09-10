from __future__ import annotations

from datetime import UTC, datetime

import pytest

from ai_usage_cost.models import CostBreakdown, TokenUsage, UsageEvent
from ai_usage_cost.pipeline import unknown_models
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
        uncached_input=M,
        cache_read=M,
        cache_write_5m=M,
        cache_write_1h=M,
        output=M,
    )
    assert cost.uncached_input == pytest.approx(5.00)
    assert cost.cache_read == pytest.approx(0.50)
    assert cost.cache_write == pytest.approx(6.25 + 10.00)
    assert cost.output == pytest.approx(25.00)
    assert cost.total == pytest.approx(46.75)


def test_no_cache_equivalent_bills_every_input_token_at_the_full_input_rate() -> None:
    cost = price(
        model="claude-opus-5",
        uncached_input=M,
        cache_read=M,
        cache_write_5m=M,
        cache_write_1h=M,
        output=M,
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
        model="claude-opus-5",
        tier="fast",
        uncached_input=M,
        cache_read=M,
        cache_write_5m=M,
        cache_write_1h=M,
        output=M,
    )
    assert cost.uncached_input == pytest.approx(10.00)
    assert cost.total == pytest.approx(93.50)


def test_batch_tier_halves_every_component() -> None:
    cost = price(
        model="claude-opus-5",
        tier="batch",
        uncached_input=M,
        cache_read=M,
        cache_write_5m=M,
        cache_write_1h=M,
        output=M,
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

    unknown = unknown_models(found.events)
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
        source="dyad",
        client="dyad",
        model=None,
        timestamp=datetime(2026, 8, 20, 10, 0, tzinfo=UTC),
        session_id="s1",
        tokens=None,
    )
    cost, state = price_event(unavailable, TABLE)
    assert cost is None
    assert state == "unavailable"


def test_google_cache_read_is_ten_percent_not_the_old_25_percent() -> None:
    cost = price(model="gemini-2.5-pro", uncached_input=M, cache_read=M, output=M)
    assert cost.uncached_input == pytest.approx(1.25)
    assert cost.cache_read == pytest.approx(0.125)
    assert cost.output == pytest.approx(10.00)


def test_google_cache_write_is_billed_like_ordinary_input() -> None:
    cost = price(model="gemini-2.5-flash", uncached_input=M, cache_write_5m=M, cache_write_1h=M)
    assert cost.cache_write == pytest.approx(2 * 0.30)


def test_deepseek_cache_read_reflects_the_real_cache_hit_discount() -> None:
    cost = price(model="deepseek-v4-pro", uncached_input=M, cache_read=M)
    assert cost.uncached_input == pytest.approx(0.66)
    assert cost.cache_read == pytest.approx(0.66 * 0.033)


def test_deepseek_has_no_batch_discount() -> None:
    cost = price(model="deepseek-v4-pro", tier="batch", uncached_input=M)
    assert cost.uncached_input == pytest.approx(0.66)


def test_moonshot_batch_and_cache_read_multipliers() -> None:
    cost = price(model="kimi-k2.7-code", uncached_input=M, cache_read=M)
    assert cost.cache_read == pytest.approx(0.95 * 0.2)
    batch_cost = price(model="kimi-k2.7-code", tier="batch", uncached_input=M)
    assert batch_cost.uncached_input == pytest.approx(0.95 * 0.6)


def test_xai_has_no_batch_discount_by_default() -> None:
    cost = price(model="grok-4.6", tier="batch", uncached_input=M, cache_read=M)
    assert cost.uncached_input == pytest.approx(2.00)
    assert cost.cache_read == pytest.approx(2.00 * 0.25)


def test_alibaba_implicit_cache_read_discount() -> None:
    cost = price(model="qwen-max", uncached_input=M, cache_read=M)
    assert cost.cache_read == pytest.approx(2.00 * 0.2)


def test_zhipu_has_no_batch_discount() -> None:
    cost = price(model="glm-4.5", tier="batch", uncached_input=M, cache_read=M)
    assert cost.uncached_input == pytest.approx(0.60)
    assert cost.cache_read == pytest.approx(0.60 * 0.2)


def test_mistral_has_a_real_cache_discount_and_batch_halves_the_price() -> None:
    cost = price(model="mistral-large-3", uncached_input=M, cache_read=M)
    assert cost.cache_read == pytest.approx(0.50 * 0.1)
    batch_cost = price(model="mistral-large-3", tier="batch", uncached_input=M, output=M)
    assert batch_cost.uncached_input == pytest.approx(0.25)
    assert batch_cost.output == pytest.approx(0.75)


def test_minimax_cache_write_premium() -> None:
    cost = price(model="minimax-m3", uncached_input=M, cache_write_5m=M)
    assert cost.cache_write == pytest.approx(0.30 * 1.25)


def test_amazon_nova_cache_read_and_batch() -> None:
    cost = price(model="amazon-nova-pro", uncached_input=M, cache_read=M)
    assert cost.cache_read == pytest.approx(0.80 * 0.25)
    batch_cost = price(model="amazon-nova-pro", tier="batch", uncached_input=M, output=M)
    assert batch_cost.uncached_input == pytest.approx(0.40)
    assert batch_cost.output == pytest.approx(1.60)


def test_no_provider_silently_falls_back_to_anthropic_shaped_cache_defaults() -> None:
    for name in ["deepseek", "moonshot", "xai", "alibaba", "zhipu", "mistral", "minimax", "amazon"]:
        rules = TABLE.rules_for(name)
        assert (rules.cache_read, rules.cache_write_5m, rules.cache_write_1h, rules.batch) != (
            0.1,
            1.25,
            2.0,
            0.5,
        )


def test_gpt_5_2_codex_does_not_collide_with_plain_gpt_5() -> None:
    rate = TABLE.lookup("gpt-5.2-codex")
    assert rate is not None
    assert rate.match == "gpt-5.2-codex"
    assert (rate.input, rate.output) == (1.75, 14.0)


def test_claude_fable_5_1_does_not_collide_with_claude_fable_5() -> None:
    rate = TABLE.lookup("claude-fable-5-1")
    assert rate is not None
    assert rate.match == "claude-fable-5-1"
    assert (rate.input, rate.output) == (10.0, 50.0)


def test_claude_fable_5_1_cache_read_uses_its_own_discount_not_the_provider_default() -> None:
    cost = price(model="claude-fable-5-1", cache_read=M)
    assert cost.cache_read == pytest.approx(0.25)


def test_claude_mythos_5_1_cache_read_uses_its_own_discount_not_the_provider_default() -> None:
    cost = price(model="claude-mythos-5-1", cache_read=M)
    assert cost.cache_read == pytest.approx(0.25)


def test_claude_fable_5_cache_read_still_uses_the_provider_default() -> None:
    cost = price(model="claude-fable-5", cache_read=M)
    assert cost.cache_read == pytest.approx(1.0)


def test_claude_fable_5_1_cache_write_and_batch_still_use_the_provider_default() -> None:
    cost = price(model="claude-fable-5-1", cache_write_5m=M, cache_write_1h=M)
    assert cost.cache_write == pytest.approx(12.5 + 20.0)
    batch_cost = price(model="claude-fable-5-1", tier="batch", uncached_input=M)
    assert batch_cost.uncached_input == pytest.approx(5.0)


def test_gpt_6_astra_is_priced() -> None:
    rate = TABLE.lookup("gpt-6-astra")
    assert rate is not None
    assert (rate.input, rate.output) == (10.0, 50.0)


def test_lookup_flags_a_versioned_snapshot_as_inherited() -> None:
    rate = TABLE.lookup("claude-opus-4-5-20251101")
    assert rate is not None
    assert rate.inherited is True


def test_lookup_does_not_flag_an_exact_match_as_inherited() -> None:
    rate = TABLE.lookup("claude-fable-5-1")
    assert rate is not None
    assert rate.inherited is False


def test_lookup_inherited_flag_does_not_mutate_the_shared_rate() -> None:
    TABLE.lookup("claude-opus-4-5-20251101")
    stored = next(m for m in TABLE.models if m.match == "claude-opus-4-5")
    assert stored.inherited is False


def test_free_provider_prices_at_zero() -> None:
    local = UsageEvent(
        source="ollama-app",
        client="ollama-app",
        provider="local",
        model="llama3",
        timestamp=datetime(2026, 8, 20, 10, 0, tzinfo=UTC),
        session_id="s1",
        tokens=TokenUsage(uncached_input=1000, output=500),
    )
    cost, state = price_event(local, TABLE)
    assert state == "free"
    assert cost is not None
    assert cost.total == 0.0


def test_free_provider_without_token_counts_is_unavailable() -> None:
    local = UsageEvent(
        source="ollama-app",
        client="ollama-app",
        provider="local",
        model="llama3",
        timestamp=datetime(2026, 8, 20, 10, 0, tzinfo=UTC),
        session_id="s1",
        tokens=None,
    )
    cost, state = price_event(local, TABLE)
    assert state == "unavailable"
    assert cost is None


def test_every_declared_context_window_is_a_positive_int() -> None:
    declared = [rate for rate in TABLE.models if rate.context_window is not None]
    assert declared
    for rate in declared:
        assert isinstance(rate.context_window, int)
        assert not isinstance(rate.context_window, bool)
        assert rate.context_window > 0


def test_every_priced_model_states_a_context_window() -> None:
    missing = [rate.match for rate in TABLE.models if rate.context_window is None]
    assert missing == []


def test_context_windows_match_the_vendors_stated_limits() -> None:
    assert TABLE.lookup("claude-opus-5").context_window == 1_000_000
    assert TABLE.lookup("claude-haiku-4-5").context_window == 200_000
    assert TABLE.lookup("gpt-6-astra").context_window == 922_000
    assert TABLE.lookup("gpt-5-codex").context_window == 272_000
    assert TABLE.lookup("gemini-3.1-pro").context_window == 1_048_576
    assert TABLE.lookup("grok-4.3").context_window == 1_000_000
    assert TABLE.lookup("minimax-m2").context_window == 204_800
    assert TABLE.lookup("totally-unknown-model") is None


def test_a_long_context_model_id_inherits_its_row_and_window() -> None:
    rate = TABLE.lookup("claude-sonnet-5[1m]")
    assert rate is not None
    assert rate.inherited is True
    assert rate.context_window == 1_000_000


def test_gpt_5_6_sol_matches_the_published_rate() -> None:
    rate = TABLE.lookup("gpt-5.6-sol")
    assert rate is not None
    assert (rate.input, rate.output) == (4.00, 20.00)


def test_gpt_5_3_codex_has_its_own_row_not_the_gpt_5_price() -> None:
    rate = TABLE.lookup("gpt-5.3-codex")
    assert rate is not None
    assert rate.match == "gpt-5.3-codex" and not rate.inherited
    assert (rate.input, rate.output) == (1.75, 14.0)


@pytest.mark.parametrize(
    "model,expected",
    [
        ("gpt-5.5", (5.0, 30.0)),
        ("gpt-5.5-pro", (30.0, 180.0)),
        ("gpt-5.4", (2.5, 15.0)),
        ("gpt-5.4-mini", (0.75, 4.5)),
        ("gpt-5.4-nano", (0.2, 1.25)),
        ("gpt-5.4-pro", (30.0, 180.0)),
        ("gpt-5.2", (1.75, 14.0)),
        ("gpt-5.1", (1.25, 10.0)),
        ("gpt-5-pro", (15.0, 120.0)),
        ("o3-mini", (1.1, 4.4)),
        ("o3-pro", (20.0, 80.0)),
        ("gpt-4.1-mini", (0.4, 1.6)),
        ("gpt-4.1-nano", (0.1, 0.4)),
        ("gpt-4o-mini", (0.15, 0.6)),
    ],
)
def test_sibling_openai_families_do_not_inherit_a_shorter_prefix(
    model: str, expected: tuple[float, float]
) -> None:
    rate = TABLE.lookup(model)
    assert rate is not None and not rate.inherited
    assert (rate.input, rate.output) == expected


@pytest.mark.parametrize(
    "model,ratio",
    [
        ("gpt-4o", 0.5),
        ("gpt-4o-mini", 0.5),
        ("o3", 0.25),
        ("o3-mini", 0.5),
        ("gpt-4.1", 0.25),
        ("gpt-4.1-mini", 0.25),
        ("gpt-4.1-nano", 0.25),
        ("o4-mini", 0.25),
    ],
)
def test_legacy_openai_cache_read_overrides_are_not_the_provider_default(
    model: str, ratio: float
) -> None:
    rate = TABLE.lookup(model)
    assert rate is not None
    rules = rate.cache_rules or TABLE.rules_for(rate.provider)
    assert rules.cache_read == pytest.approx(ratio)
    cost = price(model=model, cache_read=M)
    assert cost.cache_read == pytest.approx(rate.input * ratio)


def test_legacy_openai_cache_rules_keep_the_providers_own_write_and_batch_multipliers() -> None:
    # A model's cache_rules fully replaces the provider block rather than merging with it --
    # each override must repeat the openai provider's own write/batch values, not the
    # ProviderRules class defaults (cache_write_1h defaults to 2.0, openai's is 1.25).
    provider_rules = TABLE.rules_for("openai")
    for model in ("gpt-4o", "o3", "gpt-4.1", "o4-mini"):
        rate = TABLE.lookup(model)
        assert rate is not None and rate.cache_rules is not None
        assert rate.cache_rules.cache_write_5m == provider_rules.cache_write_5m
        assert rate.cache_rules.cache_write_1h == provider_rules.cache_write_1h
        assert rate.cache_rules.batch == provider_rules.batch


def test_codex_auto_review_is_explicitly_known_unpriced_with_a_note() -> None:
    assert TABLE.lookup("codex-auto-review") is None
    note = TABLE.unpriced_note("codex-auto-review")
    assert note is not None
    assert "no published" in note


def test_unpriced_note_is_none_for_a_model_nobody_ever_flagged() -> None:
    assert TABLE.unpriced_note("totally-unknown-model") is None
    assert TABLE.unpriced_note(None) is None


def test_inherited_pricing_is_surfaced_on_the_cost_breakdown() -> None:
    cost, state = price_event(event(model="claude-opus-4-5-20251101", uncached_input=M), TABLE)
    assert state == "priced"
    assert cost is not None
    assert cost.inherited is True


def test_exact_match_pricing_is_not_flagged_inherited() -> None:
    cost, state = price_event(event(model="claude-opus-5", uncached_input=M), TABLE)
    assert state == "priced"
    assert cost is not None
    assert cost.inherited is False


def test_summed_cost_breakdowns_carry_inherited_forward() -> None:
    plain = CostBreakdown(uncached_input=1.0)
    flagged = CostBreakdown(uncached_input=1.0, inherited=True)
    assert (plain + flagged).inherited is True
    assert (plain + plain).inherited is False
