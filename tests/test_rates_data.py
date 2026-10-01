"""Invariants and headline prices of the real `src/ai_usage_cost/rates.json`.

Structural checks run over the raw JSON and through `RateTable.load`; the cost tests price real
`TokenUsage` through `price_event` with explicit token counts and the arithmetic in comments.
"""

from __future__ import annotations

import json
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import pytest

from ai_usage_cost.models import CostBreakdown, TokenUsage, UsageEvent
from ai_usage_cost.pricing import BUILTIN_PREFIXES, DEFAULT_RATES_PATH, RateTable, price_event

M = 1_000_000
RAW: dict[str, Any] = json.loads(DEFAULT_RATES_PATH.read_text("utf-8"))
ROWS: list[dict[str, Any]] = RAW["models"]
TABLE = RateTable.load()
FIXTURES = Path(__file__).parent / "fixtures"

# Rows whose vendor page states no context window (the page lists price only). Left unset
# rather than guessed; the dashboard then shows context occupancy as unavailable.
CONTEXT_WINDOW_UNSTATED = frozenset({"glm-5.1", "glm-5", "glm-4.6"})

# Rows with `verified: null`: the vendor no longer lists them on its pricing page, so the
# historical price kept from the previous table could not be re-read. Retired by Anthropic.
UNVERIFIED_ROWS = frozenset(
    {"claude-3-7-sonnet", "claude-3-5-sonnet", "claude-3-opus", "claude-3-haiku"}
)

# v1 `match` keys that were re-keyed to the vendor's real id: key -> successor row.
REKEYED = {
    "grok-build": "grok-build-0.1",
    "mistral-medium-3.5": "mistral-medium-3-5",
    "mistral-large-3": "mistral-large-2512",
    "mistral-small-4": "mistral-small-2603",
    "codestral": "codestral-2508",
    "ministral-14b": "ministral-14b-2512",
    "ministral-8b": "ministral-8b-2512",
    "ministral-3b": "ministral-3b-2512",
    "amazon-nova-2-lite": "nova-2-lite",
    "amazon-nova-premier": "nova-premier",
    "amazon-nova-pro": "nova-pro",
    "amazon-nova-lite": "nova-lite",
    "amazon-nova-micro": "nova-micro",
}

CACHE_FIELDS = ("cache_read", "cache_write_5m", "cache_write_1h")
PRICE_FIELDS = ("input", "output", *CACHE_FIELDS)


def _price_sets(row: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """Every PriceSet-shaped dict in a row (top level, variants, bands, peak, periods)."""
    found: list[tuple[str, dict[str, Any]]] = []

    def collect(path: str, block: dict[str, Any]) -> None:
        found.append((path, block))
        for tier, variant in (block.get("variants") or {}).items():
            found.append((f"{path}.variants.{tier}", variant))
        for band in block.get("bands") or []:
            collect(f"{path}.bands[{band['min_input_tokens']}]", band)
        if block.get("peak"):
            found.append((f"{path}.peak", block["peak"]))

    top = {k: v for k, v in row.items() if k != "periods"}
    collect(row["match"], top)
    for period in row.get("periods") or []:
        collect(f"{row['match']}.period[{period.get('from')}]", period)
    return found


def _when(text: str) -> datetime:
    return datetime.fromisoformat(text).replace(tzinfo=UTC)


def cost(
    model: str,
    when: str = "2026-10-01T12:00:00",
    tier: str = "standard",
    **tokens: int,
) -> CostBreakdown:
    event = UsageEvent(
        source="claude-code",
        client="claude-code",
        timestamp=_when(when),
        model=model,
        session_id="s1",
        tokens=TokenUsage(**tokens),
        tier=tier,
    )
    breakdown, state = price_event(event, TABLE)
    assert state == "priced"
    assert breakdown is not None
    return breakdown


# ---------------------------------------------------------------- structure


def test_the_shipped_table_loads_and_has_rows() -> None:
    table = RateTable.load()
    assert len(table.models) == len(ROWS) > 100


def test_every_row_provider_is_declared() -> None:
    declared = set(RAW["providers"])
    assert {row["provider"] for row in ROWS} <= declared
    assert RAW["providers"]["local"] == {"free": True}


def test_every_row_cites_a_vendor_url() -> None:
    for row in ROWS:
        assert str(row.get("source", "")).startswith("https://"), row["match"]


def test_every_row_has_a_valid_status() -> None:
    for row in ROWS:
        assert row.get("status") in {"ga", "preview", "retired"}, row["match"]


def test_verified_is_a_date_or_an_allow_listed_null() -> None:
    nulls = set()
    for row in ROWS:
        assert "verified" in row, row["match"]
        if row["verified"] is None:
            nulls.add(row["match"])
        else:
            date.fromisoformat(row["verified"])
    assert nulls == UNVERIFIED_ROWS
    for match in UNVERIFIED_ROWS:
        assert next(r for r in ROWS if r["match"] == match)["status"] == "retired"


def test_context_window_is_present_except_the_allow_list() -> None:
    missing = {row["match"] for row in ROWS if row.get("context_window") is None}
    assert missing == CONTEXT_WINDOW_UNSTATED


def test_as_of_is_the_oldest_verified_date() -> None:
    assert RAW["as_of"] == min(row["verified"] for row in ROWS if row["verified"])


def test_no_duplicate_match_keys_and_keys_are_lowercase() -> None:
    keys = [row["match"] for row in ROWS]
    assert len(keys) == len(set(keys))
    assert all(key == key.lower() for key in keys)


def test_unpriced_entries_do_not_duplicate_a_row() -> None:
    keys = {row["match"] for row in ROWS}
    unpriced = [entry["match"] for entry in RAW["unpriced_models"]]
    assert len(unpriced) == len(set(unpriced))
    assert not keys & set(unpriced)
    for entry in RAW["unpriced_models"]:
        assert entry["note"]
        assert entry.get("status") in {None, "watchlist", "no_list_price"}


def test_file_prefixes_do_not_repeat_the_builtins() -> None:
    builtin = {entry.prefix for entry in BUILTIN_PREFIXES}
    assert not {entry["prefix"] for entry in RAW["prefixes"]} & builtin


def test_every_v1_key_is_kept_or_explicitly_rekeyed() -> None:
    v1 = json.loads((FIXTURES / "rates_v1.json").read_text("utf-8"))
    keys = {row["match"] for row in ROWS}
    for row in v1["models"]:
        key = row["match"]
        if key in REKEYED:
            assert key not in keys
            assert REKEYED[key] in keys
        else:
            assert key in keys, f"v1 row {key} vanished"


def test_periods_are_ascending_and_do_not_overlap() -> None:
    for row in ROWS:
        previous_end: date | None = None
        for index, period in enumerate(row.get("periods") or []):
            start = date.fromisoformat(period["from"]) if period.get("from") else date.min
            end = date.fromisoformat(period["until"]) if period.get("until") else date.max
            assert start < end, row["match"]
            if index:
                assert previous_end is not None
                assert start >= previous_end, f"{row['match']} periods overlap or are unordered"
            previous_end = end


def test_periods_restate_every_field_the_row_has_for_that_window() -> None:
    # A period that omits cache prices, variants, bands or peak KEEPS the row's value, so a
    # stale current-day figure would leak into the old window. Each period must write the
    # field (an empty list/dict or null meaning "none/derived in this window").
    checked = 0
    for row in ROWS:
        for period in row.get("periods") or []:
            checked += 1
            for name in CACHE_FIELDS:
                if row.get(name) is not None:
                    assert name in period, f"{row['match']} period omits {name}"
            for name in ("variants", "bands"):
                if row.get(name):
                    assert name in period, f"{row['match']} period omits {name}"
            if row.get("peak"):
                assert "peak" in period, f"{row['match']} period omits peak"
    assert checked >= 7


def test_bands_are_strictly_ascending() -> None:
    for row in ROWS:
        blocks = [row, *(row.get("periods") or [])]
        for block in blocks:
            thresholds = [band["min_input_tokens"] for band in block.get("bands") or []]
            assert thresholds == sorted(set(thresholds)), row["match"]
            assert all(isinstance(t, int) and t > 0 for t in thresholds)


def test_peak_windows_are_valid() -> None:
    peaks = [
        (row["match"], peak) for row in ROWS for _, peak in _price_sets(row) if "weekdays" in peak
    ]
    assert peaks
    for match, peak in peaks:
        assert peak["weekdays"], match
        assert all(isinstance(day, int) and 0 <= day <= 6 for day in peak["weekdays"]), match
        assert peak["utc_hours"], match
        for start, end in peak["utc_hours"]:
            assert 0 <= start < end <= 24, match


def test_all_prices_are_non_negative_numbers() -> None:
    for row in ROWS:
        for path, block in _price_sets(row):
            for name in PRICE_FIELDS:
                value = block.get(name)
                if value is None:
                    continue
                assert isinstance(value, int | float), f"{path}.{name}"
                assert not isinstance(value, bool), f"{path}.{name}"
                assert value >= 0, f"{path}.{name}"


def test_cache_figures_are_numbers_or_null_never_strings() -> None:
    for row in ROWS:
        for path, block in _price_sets(row):
            for name in CACHE_FIELDS:
                if name in block:
                    value = block[name]
                    assert value is None or (
                        isinstance(value, int | float) and not isinstance(value, bool)
                    ), f"{path}.{name}={value!r}"


def test_variant_tiers_are_known() -> None:
    allowed = {"fast", "priority", "flex", "batch", "ultrafast"}
    for row in ROWS:
        for path, block in _price_sets(row):
            assert set(block.get("variants") or {}) <= allowed, path


# ---------------------------------------------------------------- resolve cases

CASES = json.loads((FIXTURES / "rates_resolve_cases.json").read_text("utf-8"))


def test_resolve_cases_cover_every_expected_kind() -> None:
    assert {case["expect_kind"] for case in CASES} == {"exact", "suffix", "estimated", "none"}
    ids = [case["id"] for case in CASES]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_model_ids_resolve_to_the_expected_row_and_kind(case: dict[str, Any]) -> None:
    found = TABLE.match_of(case["id"])
    assert found.kind == case["expect_kind"]
    assert found.match == case["expect_match"]


# ---------------------------------------------------------------- hand-computed costs


def test_claude_opus_5_5_standard_and_fast() -> None:
    usage = {
        "uncached_input": M,
        "cache_read": M,
        "cache_write_5m": M,
        "cache_write_1h": M,
        "output": M,
    }
    # standard 4 + read 0.20 + 5m write 5.00 + 1h write 8.00 + output 20 = 37.20
    assert cost("claude-opus-5-5", **usage).total == pytest.approx(37.20)
    # fast 8/40, read 0.40, writes 10.00 and 16.00: 8 + 0.40 + 10 + 16 + 40 = 74.40
    assert cost("claude-opus-5-5", tier="fast", **usage).total == pytest.approx(74.40)


def test_claude_sonnet_5_5() -> None:
    # 2 + read 0.20 + 5m write 2.50 + 1h write 4.00 + output 10 = 18.70
    total = cost(
        "claude-sonnet-5-5",
        uncached_input=M,
        cache_read=M,
        cache_write_5m=M,
        cache_write_1h=M,
        output=M,
    ).total
    assert total == pytest.approx(18.70)


def test_gpt_6_sol_short_context_versus_the_long_context_band() -> None:
    # short (input_total 200,000 <= 272,000): 0.1M x 2 + 0.1M x 0.20 + 0.01M x 10
    #   = 0.20 + 0.02 + 0.10 = 0.32
    short = cost("gpt-6-sol", uncached_input=100_000, cache_read=100_000, output=10_000)
    assert short.total == pytest.approx(0.32)
    # 300,000 input > 272,000: the WHOLE request bills the band, 4 in / 15 out:
    #   0.3M x 4 + 0.01M x 15 = 1.20 + 0.15 = 1.35 (marginal billing would give 0.6 + ... )
    long = cost("gpt-6-sol", uncached_input=300_000, output=10_000)
    assert long.total == pytest.approx(1.35)
    # the threshold itself: 272,000 is short (2 x 0.272 = 0.544), 272,001 is long
    # (4 x 0.272001 = 1.088004)
    assert cost("gpt-6-sol", uncached_input=272_000).total == pytest.approx(0.544)
    assert cost("gpt-6-sol", uncached_input=272_001).total == pytest.approx(1.088004)


def test_gpt_5_6_sol_before_and_after_the_2026_08_21_cut() -> None:
    # 50K + 50K + 50K = 150,000 input (short context), 100K output.
    usage = {
        "uncached_input": 50_000,
        "cache_read": 50_000,
        "cache_write_5m": 50_000,
        "output": 100_000,
    }
    # before the cut (period 5/30, read 0.50, 5m write derived 1.25 x 5 = 6.25):
    #   0.05 x 5 + 0.05 x 0.50 + 0.05 x 6.25 + 0.1 x 30 = 0.25 + 0.025 + 0.3125 + 3.0 = 3.5875
    before = cost("gpt-5.6-sol", when="2026-08-20T23:59:59", **usage)
    assert before.total == pytest.approx(3.5875)
    # from 2026-08-21 (4/20, read 0.40, write 5.00):
    #   0.05 x 4 + 0.05 x 0.40 + 0.05 x 5 + 0.1 x 20 = 0.2 + 0.02 + 0.25 + 2.0 = 2.47
    after = cost("gpt-5.6-sol", when="2026-08-21T00:00:00", **usage)
    assert after.total == pytest.approx(2.47)
    # pre-cut tier and long-context tables were never published: no >272K band in the window
    # (300,000 x 5 = 1.50, not the current 8/M long rate) and a flex event falls back to standard
    long = cost("gpt-5.6-sol", when="2026-08-20T12:00:00", uncached_input=300_000)
    assert long.total == pytest.approx(1.5)
    flex = cost("gpt-5.6-sol", when="2026-08-20T12:00:00", tier="flex", uncached_input=100_000)
    assert flex.total == pytest.approx(0.5)
    assert flex.tier_unpriced is True
    # the `gpt-5.6` alias follows Sol
    assert cost("gpt-5.6", when="2026-08-20T12:00:00", **usage).total == pytest.approx(3.5875)


def test_gpt_6_astra_ultrafast() -> None:
    usage = {
        "uncached_input": 50_000,
        "cache_read": 50_000,
        "cache_write_5m": 50_000,
        "output": 10_000,
    }
    # input_total 150,000 (short context). Standard 10/1.00/12.50/50:
    #   0.05 x 10 + 0.05 x 1 + 0.05 x 12.5 + 0.01 x 50 = 0.5 + 0.05 + 0.625 + 0.5 = 1.675
    assert cost("gpt-6-astra", **usage).total == pytest.approx(1.675)
    # ultrafast 60/6/75/300: 0.05 x 60 + 0.05 x 6 + 0.05 x 75 + 0.01 x 300
    #   = 3 + 0.3 + 3.75 + 3 = 10.05
    assert cost("gpt-6-astra", tier="ultrafast", **usage).total == pytest.approx(10.05)


def test_gemini_3_8_flash_introductory_price_ends_after_2026_12_31() -> None:
    usage = {"uncached_input": M, "cache_read": M, "output": M}
    # intro 0.75 + read 0.075 + out 3.75 = 4.575
    intro = cost("gemini-3.8-flash", when="2026-12-31T23:59:59", **usage)
    assert intro.total == pytest.approx(4.575)
    # from 2027-01-01: 1.50 + 0.15 + 7.50 = 9.15
    later = cost("gemini-3.8-flash", when="2027-01-01T00:00:00", **usage)
    assert later.total == pytest.approx(9.15)


@pytest.mark.parametrize(
    ("when", "expected"),
    [
        # 1M uncached + 1M cache read + 1M output.
        # 2026-09-22 is a Tuesday. Peak (01-04, 06-10 UTC Mon-Fri): 1.32 + 0.044 + 3.96 = 5.324
        ("2026-09-22T02:00:00", 5.324),
        ("2026-09-22T06:00:00", 5.324),
        # off-peak: 0.66 + 0.022 + 1.98 = 2.662 (12:00; 04:00 and 10:00 are exclusive ends)
        ("2026-09-22T12:00:00", 2.662),
        ("2026-09-22T04:00:00", 2.662),
        ("2026-09-22T10:00:00", 2.662),
        # Saturday 02:00 UTC is off-peak
        ("2026-09-26T02:00:00", 2.662),
    ],
)
def test_deepseek_v4_pro_peak_and_off_peak(when: str, expected: float) -> None:
    total = cost("deepseek-v4-pro", when=when, uncached_input=M, cache_read=M, output=M).total
    assert total == pytest.approx(expected)


def test_grok_4_7_whole_request_band_at_200k() -> None:
    # 199,999 input + 100,000 output at 2/6: 0.199999 x 2 + 0.1 x 6 = 0.399998 + 0.6 = 0.999998
    below = cost("grok-4.7", uncached_input=199_999, output=100_000)
    assert below.total == pytest.approx(0.999998)
    # 200,000 input bills everything at 4/12: 0.2 x 4 + 0.1 x 12 = 0.8 + 1.2 = 2.0
    at = cost("grok-4.7", uncached_input=200_000, output=100_000)
    assert at.total == pytest.approx(2.0)


def test_kimi_k3_bills_one_hour_cache_writes() -> None:
    # 1M uncached x 3 + 1M 1h write x 6.00 = 9.00 (the 5m write is 3.00, read 0.30)
    assert cost("kimi-k3", uncached_input=M, cache_write_1h=M).total == pytest.approx(9.0)
    assert cost("kimi-k3", cache_write_5m=M).total == pytest.approx(3.0)
    assert cost("kimi-k3", cache_read=M).total == pytest.approx(0.3)


def test_muse_spark_standard_versus_contributor() -> None:
    usage = {"uncached_input": M, "cache_read": M, "output": M}
    # standard: 1.25 + 0.15 + 4.25 = 5.65; contributor: 0.10 + 0.002 + 0.20 = 0.302
    assert cost("muse-spark-1.3", **usage).total == pytest.approx(5.65)
    assert cost("muse-spark-1.3-contributor", **usage).total == pytest.approx(0.302)
    assert TABLE.match_of("muse-spark-1.3-contributor").match == "muse-spark-1.3-contributor"
    assert TABLE.match_of("muse-spark-1.3").match == "muse-spark-1.3"


def test_jev_output_is_free() -> None:
    # 1M input x 0.042 + 1M output x 0 = 0.042
    breakdown = cost("jev-1.13.0", uncached_input=M, output=M)
    assert breakdown.output == 0.0
    assert breakdown.total == pytest.approx(0.042)
