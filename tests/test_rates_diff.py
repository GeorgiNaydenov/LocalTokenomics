"""Tests for scripts/rates_diff.py (maintainer price-table diff). No network."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = Path(__file__).parent / "fixtures" / "rates_diff" / "litellm_sample.json"
TODAY = date(2026, 10, 1)


def _load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("rates_diff", ROOT / "scripts" / "rates_diff.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["rates_diff"] = module
    spec.loader.exec_module(module)
    return module


rd = _load_script()

RATES: dict[str, Any] = {
    "as_of": "2026-09-20",
    "models": [
        {
            "match": "claude-opus-5-5",
            "provider": "anthropic",
            "input": 5.0,
            "output": 25.0,
            "cache_read": 0.5,
            "verified": "2026-09-20",
        },
        {
            "match": "claude-sonnet-5",
            "provider": "anthropic",
            "input": 3.0,
            "output": 15.0,
            "verified": "2026-09-25",
        },
        {
            "match": "gpt-6-sol",
            "provider": "openai",
            "input": 2.0,
            "output": 10.0,
            "status": "preview",
            "verified": "2026-09-25",
        },
        {
            "match": "gpt-6-luna",
            "provider": "openai",
            "input": 0.5,
            "output": 2.5,
            "periods": [{"from": "2026-09-01", "until": "2026-10-31", "input": 0.5, "output": 2.5}],
        },
        {
            "match": "gemini-3-flash",
            "provider": "google",
            "input": 0.3,
            "output": 2.5,
            "status": "retired",
            "verified": "2026-01-01",
        },
    ],
    "unpriced_models": [
        {"match": "gemini-4", "note": "not out yet", "status": "watchlist"},
        {"match": "codex-auto-review", "note": "no list price"},
    ],
}
BASE_ARGS = ["--catalog", str(FIXTURE), "--today", "2026-10-01"]


def _write_rates(tmp_path: Path, data: dict[str, Any] | None = None) -> Path:
    path = tmp_path / "rates.json"
    path.write_text(json.dumps(RATES if data is None else data), encoding="utf-8")
    return path


@pytest.fixture(name="report")
def report_fixture() -> dict[str, Any]:
    catalog = rd.load_catalog(str(FIXTURE))
    return rd.analyse(copy.deepcopy(RATES), catalog, today=TODAY)


def test_normalise_key_strips_prefixes_and_skips_noise() -> None:
    assert rd.normalise_key("anthropic/Claude-Opus-5-5") == "claude-opus-5-5"
    assert rd.normalise_key("us.anthropic.claude-x-v1:0") == "claude-x-v1:0"
    assert rd.normalise_key("vertex_ai/claude-x@20260101") == "claude-x@20260101"
    assert rd.normalise_key("eu.anthropic.claude-x") == "claude-x"
    assert rd.normalise_key("openrouter/anthropic/claude-x") is None  # third-party host
    assert rd.normalise_key("bedrock/us-east-1/claude-x") is None
    assert rd.normalise_key("ft:gpt-6-sol:org") is None


@pytest.mark.parametrize(
    ("model_id", "kind"),
    [
        ("gpt-6-sol", "exact"),
        ("gpt-6-sol-20260101", "suffix"),
        ("gpt-6-sol-2026-01-01", "suffix"),
        ("gpt-6-sol@20260101", "suffix"),
        ("gpt-6-sol[1m]", "suffix"),
        ("gpt-6-sol-v2", "suffix"),
        ("gpt-6-sol-v1:0", "suffix"),
        ("gpt-6-sol-latest", "suffix"),
        ("gpt-6-sol-20260101-v1:0", "suffix"),
        ("gpt-6-sol-mini", "estimated"),
        ("gpt-6-sol-20260101-mini", "estimated"),
        ("gpt-6-sol.1", "estimated"),
        ("gpt-7", "none"),
    ],
)
def test_classify_benign_suffix_grammar(model_id: str, kind: str) -> None:
    assert rd.classify(model_id, ["gpt-6", "gpt-6-sol"])[0] == kind


def test_classify_longest_match_wins() -> None:
    assert rd.classify("gpt-6-sol-latest", ["gpt-6", "gpt-6-sol"]) == ("suffix", "gpt-6-sol")


def test_per_million_rounds_and_ignores_junk() -> None:
    assert rd.per_million(2.5e-06) == 2.5
    assert rd.per_million(1.4e-08) == 0.014
    assert rd.per_million(3.125e-06) == 3.125
    assert rd.per_million(None) is None
    assert rd.per_million("x") is None


def test_regional_keys_are_not_price_sources() -> None:
    entry = {"mode": "chat", "input_cost_per_token": 1e-06}
    keys = [(i, k) for i, k, _ in rd.candidates({"eu.anthropic.claude-x": entry})]
    assert keys == []


def test_missing_section(report: dict[str, Any]) -> None:
    flat = {s["match"]: s for rows in report["missing"].values() for s in rows}
    # prefix collision with a non-benign remainder is missing, grouped by provider
    assert "claude-sonnet-5-5" in {s["match"] for s in report["missing"]["anthropic"]}
    assert {"gpt-6.1-sol", "gemini-4-pro-preview", "deepseek-flash", "grok-4.7"} <= set(flat)
    # matched, benign-suffixed, regional, third-party, fine-tune and non-chat entries are not
    for absent in (
        "claude-opus-5-5",
        "gpt-6-sol",
        "text-embedding-3-small",
        "gpt-image-1",
        "rerank-v4",
        "sample_spec",
    ):
        assert absent not in flat
    assert not any(m.startswith("ft:") for m in flat)
    assert set(report["missing"]) == {"anthropic", "openai", "google", "deepseek", "xai"}


def test_skeleton_math_bands_and_variants(report: dict[str, Any]) -> None:
    skeleton = next(s for s in report["missing"]["openai"] if s["match"] == "gpt-6.1-sol")
    assert skeleton["provider"] == "openai"
    assert skeleton["display"] == "GPT 6.1 Sol"
    assert (skeleton["input"], skeleton["output"]) == (2.5, 15.0)
    assert skeleton["cache_read"] == 0.25
    assert skeleton["cache_write_5m"] == 3.125
    assert skeleton["cache_write_1h"] == 5.0
    assert skeleton["context_window"] == 922000
    assert skeleton["bands"] == [
        {
            "min_input_tokens": 272001,
            "input": 5.0,
            "output": 22.5,
            "cache_read": 0.5,
            "variants": {"priority": {"input": 10.0, "output": 45.0}},
        }
    ]
    assert skeleton["variants"] == {
        "priority": {"input": 5.0, "output": 30.0},
        "flex": {"input": 1.25, "output": 7.5},
        "batch": {"input": 1.25, "output": 7.5},
    }
    assert skeleton["source"] == rd.CATALOG_URL
    assert skeleton["verified"] is None
    assert "vendor-page check" in skeleton["note"]


def test_skeleton_200k_band_threshold(report: dict[str, Any]) -> None:
    gemini = report["missing"]["google"][0]
    assert gemini["match"] == "gemini-4-pro-preview"
    assert gemini["bands"][0]["min_input_tokens"] == 200001
    assert gemini["bands"][0]["input"] == 4.0


def test_drift_section(report: dict[str, Any]) -> None:
    drift = {d["match"]: d for d in report["drift"]}
    assert set(drift) == {"gpt-6-sol"}  # luna skipped (period), opus equal, flash retired
    assert drift["gpt-6-sol"]["diffs"] == [
        {"field": "input", "ours": 2.0, "theirs": 4.0},
        {"field": "output", "ours": 10.0, "theirs": 20.0},
    ]
    assert report["drift_skipped"] == 2  # gpt-6-luna (period) + gemini-3-flash (retired)


def test_drift_tolerance_and_cache() -> None:
    entry = {
        "input_cost_per_token": 5.01e-06,
        "output_cost_per_token": 2.5e-05,
        "cache_read_input_token_cost": 6e-07,
    }
    row = {"input": 5.0, "output": 25.0, "cache_read": 0.5}
    diffs = rd.compare_prices(row, entry)
    assert [d["field"] for d in diffs] == ["cache_read"]  # 0.2% input drift is within tolerance
    assert rd.compare_prices({"input": 5.0}, {"output_cost_per_token": 1.0}) == []


def test_preview_retired_and_stale(report: dict[str, Any]) -> None:
    assert report["preview"] == ["gpt-6-sol"]
    assert report["retired_in_catalog"] == ["gemini-3-flash"]
    stale = report["stale"]
    assert stale["count"] == 1  # luna has no `verified`; retired rows are excluded
    assert stale["oldest"] == [{"match": "gpt-6-luna", "verified": None}]
    tight = rd.analyse(
        copy.deepcopy(RATES), rd.load_catalog(str(FIXTURE)), today=TODAY, stale_days=10
    )
    assert tight["stale"]["count"] == 2  # opus (verified 11 days ago) joins luna
    assert tight["stale"]["oldest"][0]["verified"] is None


def test_watchlist(report: dict[str, Any]) -> None:
    watch = {w["match"]: w for w in report["watchlist"]}
    assert watch["gemini-4"]["hit"] is True
    entry = watch["gemini-4"]["entries"][0]
    assert entry["catalog_key"] == "gemini/gemini-4-pro-preview"
    assert (entry["input"], entry["output"]) == (2.0, 12.0)
    assert watch["codex-auto-review"]["hit"] is False


def test_watchlist_literals_added_when_file_has_none() -> None:
    names = {w["match"] for w in rd.watchlist({"models": []}, {})}
    assert names == {"gemini-4", "codex-auto-review"}


def test_v1_rows_without_new_fields() -> None:
    rates = {"models": [{"match": "gpt-6-sol", "provider": "openai", "input": 4, "output": 20}]}
    result = rd.analyse(rates, rd.load_catalog(str(FIXTURE)), today=TODAY)
    assert result["drift"] == []
    assert result["stale"]["count"] == 1
    assert result["counts"]["rows"] == 1


def test_text_output(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    code = rd.main(["--rates", str(_write_rates(tmp_path)), *BASE_ARGS])
    out = capsys.readouterr().out
    assert code == 0
    for heading in ("1. Missing", "2. Price drift", "3. Preview", "4. Retired", "5. Watchlist"):
        assert heading in out
    assert "needs a vendor-page check" in out
    assert "WATCHLIST HIT gemini-4" in out
    assert "ours 2.0  theirs 4.0" in out
    assert "SUMMARY missing=" in out


def test_json_output_and_exit_codes(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    args = ["--rates", str(_write_rates(tmp_path)), *BASE_ARGS]
    assert rd.main([*args, "--format", "json", "--fail-on-findings"]) == 1
    data = json.loads(capsys.readouterr().out)
    assert data["findings"] > 0
    assert data["summary"].startswith("SUMMARY")
    assert data["watchlist"][0]["match"] == "codex-auto-review"
    # No findings: exit 0 even with the flag
    empty = tmp_path / "empty_catalog.json"
    empty.write_text("{}", encoding="utf-8")
    clean = _write_rates(tmp_path, {"models": []})
    assert rd.main(["--rates", str(clean), "--catalog", str(empty), "--fail-on-findings"]) == 0
    capsys.readouterr()


def test_bad_inputs_exit_2(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    code = rd.main(["--rates", str(tmp_path / "nope.json"), "--catalog", str(FIXTURE)])
    assert code == 2
    assert "error:" in capsys.readouterr().err
    with pytest.raises(rd.CatalogError):
        rd.load_catalog(str(tmp_path / "missing.json"))


def test_never_writes_rates(tmp_path: Path) -> None:
    rates = _write_rates(tmp_path)
    before = (rates.read_bytes(), rates.stat().st_mtime_ns)
    real = ROOT / "src" / "ai_usage_cost" / "rates.json"
    real_before = real.read_bytes()
    rd.main(["--rates", str(rates), *BASE_ARGS])
    rd.main(["--rates", str(real), *BASE_ARGS])
    assert (rates.read_bytes(), rates.stat().st_mtime_ns) == before
    assert real.read_bytes() == real_before
