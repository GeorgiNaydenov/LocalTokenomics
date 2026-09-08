from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_usage_cost import privacy
from ai_usage_cost.api import create_app
from ai_usage_cost.pipeline import Analysis

CLAUDE_SESSION = ("claude-code", "sess-trace")
CODEX_SESSION = ("codex", "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")


@pytest.fixture
def client(analysis: Analysis) -> Iterator[TestClient]:
    with TestClient(create_app(analysis)) as test_client:
        yield test_client


@pytest.fixture
def traced(trace_analysis: Analysis) -> Iterator[TestClient]:
    with TestClient(create_app(trace_analysis)) as test_client:
        yield test_client


def readable_content(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"metadata_only": False}), "utf-8")
    monkeypatch.setattr(privacy, "DEFAULT_CONFIG_PATH", config)


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

    assert len(meta["sources"]) == 9
    for source in meta["sources"]:
        assert {"id", "token_data", "detected", "files", "root_hint", "capabilities"} <= set(source)
    detected = {source["id"]: source for source in meta["sources"] if source["detected"]}
    assert set(detected) == {"claude-code", "codex"}
    assert all(source["files"] > 0 for source in detected.values())
    undetected = [source for source in meta["sources"] if not source["detected"]]
    assert all(source["files"] == 0 for source in undetected)


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
        "request_count", "tokens", "cost", "cost_state", "cost_states", "is_sidechain",
        "currency", "project", "working_directory", "repository",
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


def test_states_filter_narrows_the_report(client: TestClient) -> None:
    everything = client.get("/api/report").json()
    priced_only = client.get("/api/report", params={"states": "priced"}).json()

    assert priced_only["totals"]["events"] <= everything["totals"]["events"]
    assert priced_only["totals"]["events"] > 0
    assert priced_only["facets"]["clients"] == everything["facets"]["clients"]


def test_search_filter_narrows_the_report(client: TestClient) -> None:
    everything = client.get("/api/report").json()
    narrowed = client.get("/api/report", params={"search": "codex-cli"}).json()

    assert narrowed["totals"]["events"] < everything["totals"]["events"]
    assert {bucket["key"] for bucket in narrowed["by_client"]} == {"codex-cli"}


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


def test_cursor_is_registered_with_nothing_available(client: TestClient) -> None:
    meta = client.get("/api/meta").json()
    cursor = next(source for source in meta["sources"] if source["id"] == "cursor")
    assert cursor["detected"] is False
    assert cursor["files"] == 0
    assert set(cursor["capabilities"].values()) == {"unavailable"}
    codex = next(source for source in meta["sources"] if source["id"] == "codex")
    assert codex["capabilities"] == {
        "trace": "measured", "tokens": "measured", "cost": "derived",
        "context": "measured", "latency": "measured",
    }


def test_every_parent_id_resolves_inside_the_trace(traced: TestClient) -> None:
    source, session_id = CLAUDE_SESSION
    response = traced.get(f"/api/sessions/{source}/{session_id}/trace")
    assert response.status_code == 200
    trace = response.json()

    assert trace["capabilities"]["trace"] == "measured"
    assert trace["spans"]
    known = {span["span_id"] for span in trace["spans"]}
    parents = {span["parent_id"] for span in trace["spans"] if span["parent_id"]}
    assert parents <= known
    assert any(span["kind"] == "subagent" for span in trace["spans"])
    assert all(insight["span_id"] in known for insight in trace["insights"])


def test_an_unknown_session_has_no_trace(traced: TestClient) -> None:
    assert traced.get("/api/sessions/codex/nope/trace").status_code == 404


def test_economics_totals_equal_the_sum_over_model_calls(traced: TestClient) -> None:
    source, session_id = CLAUDE_SESSION
    spans = traced.get(f"/api/sessions/{source}/{session_id}/trace").json()["spans"]
    economics = traced.get(f"/api/sessions/{source}/{session_id}/economics").json()

    calls = [span for span in spans if span["kind"] == "model_call" and span["tokens"]]
    assert economics["totals"]["model_calls"] == len(calls)
    assert economics["totals"]["tokens"]["total"] == sum(
        span["tokens"]["total"] for span in calls
    )
    assert sum(row["tokens"]["total"] for row in economics["by_model"]) == (
        economics["totals"]["tokens"]["total"]
    )
    assert economics["totals"]["cost_state"] == "priced"
    assert economics["totals"]["cost"]["total"] > 0
    assert economics["totals"]["retries"] == 2


def test_claude_code_context_capacity_is_estimated_from_the_rate_table(
    traced: TestClient,
) -> None:
    source, session_id = CLAUDE_SESSION
    snapshots = traced.get(f"/api/sessions/{source}/{session_id}/context").json()
    assert snapshots

    opus = next(item for item in snapshots if item["model"] == "claude-opus-5")
    assert (opus["capacity"], opus["capacity_provenance"]) == (1_000_000, "estimated")
    assert opus["occupancy_provenance"] == "estimated"

    long_context = next(item for item in snapshots if item["model"] == "claude-sonnet-5[1m]")
    assert long_context["capacity_provenance"] == "inferred"


def test_codex_context_occupancy_is_derived_from_the_logged_window(traced: TestClient) -> None:
    source, session_id = CODEX_SESSION
    snapshots = traced.get(f"/api/sessions/{source}/{session_id}/context").json()
    assert snapshots
    for item in snapshots:
        assert item["capacity_provenance"] == "measured"
        assert item["occupancy_provenance"] == "derived"
    assert snapshots[1]["delta_input"] == (
        snapshots[1]["input_total"] - snapshots[0]["input_total"]
    )
    assert snapshots[0]["delta_input"] is None


def test_an_outcome_round_trips_and_carries_computed_signals(traced: TestClient) -> None:
    source, session_id = CLAUDE_SESSION
    path = f"/api/sessions/{source}/{session_id}/outcome"

    before = traced.get(path).json()
    assert before["outcome"] == "unrated"
    assert before["signals"]["aborted_turns"] == 1

    saved = traced.put(
        path, json={"outcome": "partial", "notes": "stopped early", "tags": ["review"]}
    )
    assert saved.status_code == 200
    assert saved.json()["signals"]["aborted_turns"] == 1

    after = traced.get(path).json()
    assert (after["outcome"], after["notes"], after["tags"]) == (
        "partial", "stopped early", ["review"]
    )
    assert after["signals"]["interrupted_tools"] == 1
    assert after["signals"]["errors"] == 1
    assert traced.get(f"/api/sessions/{source}/{session_id}/trace").json()["outcome"][
        "outcome"
    ] == "partial"


def test_deleting_a_session_removes_its_trace_but_not_its_requests(traced: TestClient) -> None:
    source, session_id = CODEX_SESSION
    before = traced.get("/api/report").json()

    deleted = traced.delete(f"/api/sessions/{source}/{session_id}")
    assert deleted.status_code == 200
    assert deleted.json()["deleted_spans"] > 0

    assert traced.get(f"/api/sessions/{source}/{session_id}/trace").status_code == 404
    after = traced.get("/api/report").json()
    assert [row["session_id"] for row in after["sessions"]] == [
        row["session_id"] for row in before["sessions"]
    ]


def test_span_content_is_unavailable_while_metadata_only_is_on(traced: TestClient) -> None:
    source, session_id = CLAUDE_SESSION
    response = traced.get(f"/api/sessions/{source}/{session_id}/spans/u4/content")
    assert response.status_code == 404


def test_span_content_is_redacted_when_content_capture_is_allowed(
    traced: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    readable_content(monkeypatch, tmp_path)
    source, session_id = CLAUDE_SESSION
    response = traced.get(f"/api/sessions/{source}/{session_id}/spans/u4/content")
    assert response.status_code == 200
    content = response.json()

    assert content["span_id"] == "u4"
    assert "[REDACTED:anthropic_key]" in content["content"]
    assert "sk-ant-api03-FAKE" not in content["content"]
    assert content["redactions"] >= 1

    assert traced.get(
        f"/api/sessions/{source}/{session_id}/spans/nope/content"
    ).status_code == 404


def test_the_report_can_be_filtered_by_trace_data_and_errors(traced: TestClient) -> None:
    everything = traced.get("/api/report").json()
    assert len(everything["sessions"]) == 3
    assert all(row["traced"] for row in everything["sessions"])
    assert everything["facets"]["outcomes"] == {"unrated": 3}

    assert traced.get("/api/report", params={"traced": "false"}).json()["sessions"] == []
    assert len(traced.get("/api/report", params={"traced": "true"}).json()["sessions"]) == 3

    with_errors = traced.get("/api/report", params={"has_errors": "true"}).json()
    assert {row["source"] for row in with_errors["sessions"]} == {"claude-code", "antigravity"}
    without = traced.get("/api/report", params={"has_errors": "false"}).json()
    assert {row["source"] for row in without["sessions"]} == {"codex"}

    unrated = traced.get("/api/report", params={"outcomes": "unrated"}).json()
    assert len(unrated["sessions"]) == 3
    assert traced.get("/api/report", params={"outcomes": "successful"}).json()["sessions"] == []
