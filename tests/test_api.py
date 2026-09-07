from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from ai_usage_cost.api import create_app
from ai_usage_cost.pipeline import Analysis


@pytest.fixture
def client(analysis: Analysis) -> Iterator[TestClient]:
    with TestClient(create_app(analysis)) as test_client:
        yield test_client


def test_meta_describes_the_scan(client: TestClient) -> None:
    response = client.get("/api/meta")
    assert response.status_code == 200
    meta = response.json()

    assert meta["clients"] == [
        {"id": "claude-code", "label": "Claude Code"},
        {"id": "codex-cli", "label": "Codex CLI"},
    ]
    assert meta["models"] == [
        "claude-haiku-4-5",
        "claude-opus-5",
        "claude-sonnet-5",
        "gpt-5-codex",
        "gpt-5.6-terra",
    ]
    assert meta["projects"] == ["alpha", "beta"]
    assert meta["first_day"] == "2026-08-20"
    assert meta["last_day"] == "2026-08-21"
    assert meta["events"] == 8
    assert meta["files_scanned"] == 2
    assert meta["rates_as_of"]
    assert meta["currency"] == "USD"
    assert meta["warnings"] == []
    assert "anthropic" in meta["providers"]
    assert "openai" in meta["providers"]


def test_report_returns_the_expected_shape(client: TestClient) -> None:
    response = client.get("/api/report")
    assert response.status_code == 200
    report = response.json()

    for key in (
        "generated_at",
        "rates_as_of",
        "currency",
        "files_scanned",
        "totals",
        "by_client",
        "by_provider",
        "by_model",
        "by_project",
        "by_day",
        "series",
        "sessions",
        "unknown_models",
        "warnings",
    ):
        assert key in report

    assert report["totals"]["events"] == 8
    assert report["totals"]["sessions"] == 2
    assert len(report["series"]) == 5
    assert {bucket["key"] for bucket in report["by_client"]} == {"claude-code", "codex-cli"}

    bucket = report["by_model"][0]
    assert set(bucket) >= {"key", "label", "tokens", "cost", "events", "sessions"}

    session = report["sessions"][0]
    assert set(session) >= {
        "session_id", "source", "client", "provider", "models", "start_time", "end_time",
        "request_count", "input_tokens", "output_tokens", "cached_tokens", "reasoning_tokens",
        "cost", "cost_state", "currency", "project", "working_directory", "repository",
        "branch", "machine", "raw_source",
    }


def test_computed_fields_are_serialized(client: TestClient) -> None:
    report = client.get("/api/report").json()

    cost = report["totals"]["cost"]
    assert set(cost) == {
        "uncached_input",
        "cache_read",
        "cache_write",
        "output",
        "no_cache_equivalent",
        "total",
        "cache_savings",
    }
    assert cost["total"] == pytest.approx(
        cost["uncached_input"] + cost["cache_read"] + cost["cache_write"] + cost["output"]
    )
    assert cost["cache_savings"] == pytest.approx(cost["no_cache_equivalent"] - cost["total"])

    tokens = report["totals"]["tokens"]
    assert {"total", "input_total", "cache_write"} <= set(tokens)
    assert tokens["input_total"] == (
        tokens["uncached_input"] + tokens["cache_read"] + tokens["cache_write"]
    )
    assert tokens["total"] == tokens["input_total"] + tokens["output"]

    for bucket in report["by_model"] + report["by_client"] + report["by_project"]:
        assert "total" in bucket["cost"]
        assert "cache_savings" in bucket["cost"]
        assert "total" in bucket["tokens"]


def test_client_filter_narrows_the_report(client: TestClient) -> None:
    everything = client.get("/api/report").json()
    codex_only = client.get("/api/report", params={"clients": "codex-cli"}).json()

    assert codex_only["totals"]["events"] == 4
    assert {bucket["key"] for bucket in codex_only["by_client"]} == {"codex-cli"}
    assert codex_only["totals"]["cost"]["total"] < everything["totals"]["cost"]["total"]


def test_provider_filter_narrows_the_report(client: TestClient) -> None:
    report = client.get("/api/report", params={"providers": "openai"}).json()
    assert {bucket["key"] for bucket in report["by_provider"]} == {"openai"}


def test_date_filter_narrows_the_report(client: TestClient) -> None:
    report = client.get("/api/report", params={"since": "2026-08-21"}).json()
    assert {bucket["key"] for bucket in report["by_day"]} == {"2026-08-21"}
    assert report["totals"]["events"] == 4


def test_include_sidechains_false_drops_the_subagent_event(client: TestClient) -> None:
    everything = client.get("/api/report").json()
    no_sidechains = client.get(
        "/api/report", params={"include_sidechains": "false"}
    ).json()
    assert no_sidechains["totals"]["events"] == everything["totals"]["events"] - 1


def test_model_and_project_filters_compose(client: TestClient) -> None:
    report = client.get(
        "/api/report", params={"models": "claude-opus-5", "projects": "alpha"}
    ).json()
    assert report["totals"]["events"] == 2
    assert {bucket["key"] for bucket in report["by_model"]} == {"claude-opus-5"}


def test_a_filter_that_matches_nothing_returns_an_empty_report(client: TestClient) -> None:
    report = client.get("/api/report", params={"projects": "nope"}).json()
    assert report["totals"]["events"] == 0
    assert report["totals"]["cost"]["total"] == 0
    assert report["by_model"] == []


def test_rates_returns_the_loaded_table(client: TestClient) -> None:
    response = client.get("/api/rates")
    assert response.status_code == 200
    rates = response.json()

    assert rates["currency"] == "USD"
    assert rates["as_of"]
    assert rates["providers"]["anthropic"]["cache_read"] == 0.1
    assert rates["providers"]["anthropic"]["cache_write_5m"] == 1.25
    assert rates["providers"]["anthropic"]["cache_write_1h"] == 2.0
    assert rates["providers"]["anthropic"]["batch"] == 0.5
    assert rates["providers"]["local"]["free"] is True
    opus = next(model for model in rates["models"] if model["match"] == "claude-opus-5")
    assert opus["provider"] == "anthropic"
    assert opus["display"] == "Claude Opus 5"
    assert (opus["input"], opus["output"]) == (5.0, 25.0)
    assert opus["variants"]["fast"] == {"input": 10.0, "output": 50.0}
