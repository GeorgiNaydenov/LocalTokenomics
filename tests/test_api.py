from __future__ import annotations

import json
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_usage_cost import privacy
from ai_usage_cost.aggregate import build_report, sessions_of
from ai_usage_cost.api import create_app
from ai_usage_cost.models import CostBreakdown, PricedEvent, TokenUsage, UsageEvent
from ai_usage_cost.pipeline import Analysis
from ai_usage_cost.sources import registry
from conftest import CLAUDE_TRACE, NO_ROOT

CLAUDE_SESSION = ("claude-code", "sess-trace")
CODEX_SESSION = ("codex", "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
ANTIGRAVITY_SESSION = ("antigravity", "test-uuid-trace")
JAN_SESSION = ("jan", "thread-1")


@pytest.fixture
def client(analysis: Analysis) -> Iterator[TestClient]:
    with TestClient(create_app(analysis)) as test_client:
        yield test_client


@pytest.fixture
def traced(trace_analysis: Analysis) -> Iterator[TestClient]:
    with TestClient(create_app(trace_analysis)) as test_client:
        yield test_client


@pytest.fixture
def free(free_analysis: Analysis) -> Iterator[TestClient]:
    with TestClient(create_app(free_analysis)) as test_client:
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

    assert len(meta["sources"]) == 11
    for source in meta["sources"]:
        assert {"id", "token_data", "detected", "files", "root_hint", "capabilities"} <= set(source)
    detected = {source["id"]: source for source in meta["sources"] if source["detected"]}
    assert set(detected) == {"claude-code", "codex"}

    assert set(meta["client_last_seen"]) == {"claude-code", "codex-cli"}
    assert set(meta["model_last_seen"]) == set(meta["models"])
    assert set(meta["project_last_seen"]) == {"alpha", "beta"}
    for value in meta["client_last_seen"].values():
        assert meta["first_day"] <= value[:10] <= meta["last_day"]

    assert all(source["files"] > 0 for source in detected.values())
    undetected = [source for source in meta["sources"] if not source["detected"]]
    assert all(source["files"] == 0 for source in undetected)


def test_meta_last_seen_reflects_the_full_scan_not_a_report_filter(client: TestClient) -> None:
    meta = client.get("/api/meta").json()
    window = {"since": meta["last_day"], "until": meta["last_day"]}
    narrow = client.get("/api/report", params=window)
    assert narrow.status_code == 200
    unfiltered_last_seen = meta["client_last_seen"]

    still = client.get("/api/meta").json()

    assert still["client_last_seen"] == unfiltered_last_seen


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
        "session_id",
        "source",
        "client",
        "provider",
        "models",
        "start_time",
        "end_time",
        "request_count",
        "tokens",
        "cost",
        "cost_state",
        "cost_states",
        "is_sidechain",
        "currency",
        "project",
        "working_directory",
        "repository",
        "branch",
        "machine",
        "raw_source",
    }


def test_session_title_serializes_with_the_folder_fallback(client: TestClient) -> None:
    # No route change was needed for this -- SessionRow.title rides along automatically
    # since /api/report already returns full Report/SessionRow objects. The claude-code
    # basic fixture has no custom-title record, so the session falls through to the
    # folder-fallback title built from project + session_id.
    report = client.get("/api/report").json()
    session = next(s for s in report["sessions"] if s["session_id"] == "sess-alpha")
    assert session["title"] == "alpha_sess-alpha"


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
        "inherited",
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
    no_sidechains = client.get("/api/report", params={"include_sidechains": "false"}).json()
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
        "trace": "measured",
        "tokens": "measured",
        "cost": "derived",
        "context": "measured",
        "latency": "measured",
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


def test_spans_are_loaded_once_and_shared_across_endpoints(
    traced: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Opening a session's trace, economics and context tabs must not each pay the full
    # SQL-fetch-plus-Pydantic-validation cost of reconstructing every span from scratch.
    import ai_usage_cost.api as api_module

    source, session_id = CLAUDE_SESSION
    calls = 0
    real_load_spans = api_module.store.load_spans

    def counting_load_spans(*args: object, **kwargs: object) -> list:
        nonlocal calls
        calls += 1
        return real_load_spans(*args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(api_module.store, "load_spans", counting_load_spans)

    assert traced.get(f"/api/sessions/{source}/{session_id}/trace").status_code == 200
    assert traced.get(f"/api/sessions/{source}/{session_id}/economics").status_code == 200
    assert traced.get(f"/api/sessions/{source}/{session_id}/context").status_code == 200
    assert calls == 1, "trace, economics and context must share one cached span load"


def test_refresh_invalidates_the_span_cache(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # `traced`/`create_app(trace_analysis)` doesn't pass db_path/roots to create_app (only
    # the pre-built Analysis), so /api/refresh has nothing to re-scan there -- this test
    # builds its own app the way `serve()` really does, with matching db_path and roots.
    import ai_usage_cost.api as api_module

    db_path = tmp_path / "test.db"
    roots = {
        source_id: [CLAUDE_TRACE if source_id == "claude-code" else NO_ROOT]
        for source_id in registry()
    }
    app = create_app(db_path=db_path, roots=roots)
    source, session_id = CLAUDE_SESSION
    calls = 0
    real_load_spans = api_module.store.load_spans

    def counting_load_spans(*args: object, **kwargs: object) -> list:
        nonlocal calls
        calls += 1
        return real_load_spans(*args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(api_module.store, "load_spans", counting_load_spans)

    with TestClient(app) as client:
        assert client.get(f"/api/sessions/{source}/{session_id}/trace").status_code == 200
        assert client.get(f"/api/sessions/{source}/{session_id}/trace").status_code == 200
        assert calls == 1, "a second request for the same session must hit the cache"

        assert client.post("/api/refresh").status_code == 200
        assert client.get(f"/api/sessions/{source}/{session_id}/trace").status_code == 200
        assert calls == 2, "a refresh must invalidate the cache, not keep serving stale spans"


def test_deleting_a_session_invalidates_only_its_own_cache_entry(
    traced: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    import ai_usage_cost.api as api_module

    source, session_id = CLAUDE_SESSION
    other_source, other_session_id = "codex", "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    calls = 0
    real_load_spans = api_module.store.load_spans

    def counting_load_spans(*args: object, **kwargs: object) -> list:
        nonlocal calls
        calls += 1
        return real_load_spans(*args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(api_module.store, "load_spans", counting_load_spans)

    assert traced.get(f"/api/sessions/{source}/{session_id}/trace").status_code == 200
    assert traced.get(f"/api/sessions/{other_source}/{other_session_id}/trace").status_code == 200
    assert calls == 2

    assert traced.delete(f"/api/sessions/{source}/{session_id}").status_code == 200
    assert traced.get(f"/api/sessions/{other_source}/{other_session_id}/trace").status_code == 200
    assert calls == 2, "deleting one session must not evict a different session's cache entry"
    assert traced.get(f"/api/sessions/{source}/{session_id}/trace").status_code == 404


def test_economics_totals_equal_the_sum_over_model_calls(traced: TestClient) -> None:
    source, session_id = CLAUDE_SESSION
    spans = traced.get(f"/api/sessions/{source}/{session_id}/trace").json()["spans"]
    economics = traced.get(f"/api/sessions/{source}/{session_id}/economics").json()

    calls = [span for span in spans if span["kind"] == "model_call" and span["tokens"]]
    assert economics["totals"]["model_calls"] == len(calls)
    assert economics["totals"]["tokens"]["total"] == sum(span["tokens"]["total"] for span in calls)
    assert (
        sum(row["tokens"]["total"] for row in economics["by_model"])
        == (economics["totals"]["tokens"]["total"])
    )
    assert economics["totals"]["cost_state"] == "priced"
    assert economics["totals"]["cost"]["total"] > 0
    assert economics["totals"]["retries"] == 2
    assert economics["totals"]["tokens_provenance"] == "measured"


def test_economics_reports_absent_tokens_rather_than_zero(traced: TestClient) -> None:
    source, session_id = ANTIGRAVITY_SESSION
    economics = traced.get(f"/api/sessions/{source}/{session_id}/economics").json()

    assert economics["totals"]["model_calls"] > 0
    assert economics["totals"]["tokens"] is None
    assert economics["totals"]["tokens_provenance"] == "unavailable"
    assert economics["by_model"]
    assert all(row["tokens"] is None for row in economics["by_model"])


def test_report_and_economics_agree_without_token_counts(free: TestClient) -> None:
    source, session_id = JAN_SESSION
    row = next(
        item
        for item in free.get("/api/report").json()["sessions"]
        if (item["source"], item["session_id"]) == (source, session_id)
    )
    totals = free.get(f"/api/sessions/{source}/{session_id}/economics").json()["totals"]

    assert row["tokens"] is None
    assert row["cost_state"] == "unavailable"
    assert (row["cost"], row["cost_state"]) == (totals["cost"], totals["cost_state"])


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
        "partial",
        "stopped early",
        ["review"],
    )
    assert after["signals"]["interrupted_tools"] == 1
    assert after["signals"]["errors"] == 1
    assert (
        traced.get(f"/api/sessions/{source}/{session_id}/trace").json()["outcome"]["outcome"]
        == "partial"
    )


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

    assert traced.get(f"/api/sessions/{source}/{session_id}/spans/nope/content").status_code == 404


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


def test_by_turn_rows_carry_ordinal_started_at_and_a_privacy_gated_label(
    traced: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    source, session_id = CLAUDE_SESSION
    path = f"/api/sessions/{source}/{session_id}/economics"

    hidden = traced.get(path).json()
    first_turn = hidden["by_turn"][0]
    assert first_turn["ordinal"] == 1
    assert first_turn["started_at"]
    assert first_turn["is_sidechain"] is False
    # metadata_only defaults to True: no prompt text is ever read into a label.
    assert first_turn["label"] is None
    assert any(row["is_sidechain"] for row in hidden["by_turn"])

    readable_content(monkeypatch, tmp_path)
    revealed = traced.get(path).json()
    assert revealed["by_turn"][0]["label"] == "Add a health check endpoint"


def test_totals_report_how_many_events_actually_priced_the_dollar_figure(
    client: TestClient,
) -> None:
    report = client.get("/api/report").json()
    assert report["totals"]["priced_events"] <= report["totals"]["events"]
    assert report["totals"]["priced_events"] > 0


def test_files_in_slice_narrows_with_the_report_but_files_scanned_does_not(
    client: TestClient,
) -> None:
    everything = client.get("/api/report").json()
    assert everything["files_in_slice"] <= everything["files_scanned"]

    narrowed = client.get("/api/report", params={"clients": "codex-cli"}).json()
    assert narrowed["files_in_slice"] <= everything["files_in_slice"]
    assert narrowed["files_scanned"] == everything["files_scanned"]


def _event(*, is_sidechain: bool) -> UsageEvent:
    return UsageEvent(
        source="claude-code",
        client="claude-code",
        model="claude-opus-5",
        timestamp=datetime(2026, 9, 5, 10, 0, tzinfo=UTC),
        session_id="mixed",
        tokens=TokenUsage(uncached_input=10, output=10),
        is_sidechain=is_sidechain,
    )


def test_session_is_sidechain_only_when_every_event_is_but_has_sidechain_on_any() -> None:
    mostly_main = sessions_of(
        [
            PricedEvent(event=_event(is_sidechain=False), cost=CostBreakdown(), state="priced"),
            PricedEvent(event=_event(is_sidechain=True), cost=CostBreakdown(), state="priced"),
        ],
        currency="USD",
    )[0]
    assert mostly_main.has_sidechain is True
    assert mostly_main.is_sidechain is False

    all_sidechain = sessions_of(
        [PricedEvent(event=_event(is_sidechain=True), cost=CostBreakdown(), state="priced")],
        currency="USD",
    )[0]
    assert all_sidechain.has_sidechain is True
    assert all_sidechain.is_sidechain is True


def test_session_cost_state_is_the_worst_of_its_requests_with_mixed_states_kept() -> None:
    row = sessions_of(
        [
            PricedEvent(event=_event(is_sidechain=False), cost=CostBreakdown(), state="priced"),
            PricedEvent(event=_event(is_sidechain=False), cost=None, state="unpriced"),
        ],
        currency="USD",
    )[0]
    assert row.cost_state == "unpriced"
    assert set(row.cost_states) == {"priced", "unpriced"}


def test_build_report_files_in_slice_counts_distinct_source_files_in_the_filtered_set() -> None:
    def event(source_file: str) -> UsageEvent:
        return UsageEvent(
            source="claude-code",
            client="claude-code",
            model="claude-opus-5",
            timestamp=datetime(2026, 9, 5, 10, 0, tzinfo=UTC),
            session_id="s1",
            tokens=TokenUsage(uncached_input=1, output=1),
            source_file=source_file,
        )

    priced = [
        PricedEvent(event=event("a.jsonl"), cost=CostBreakdown(), state="priced"),
        PricedEvent(event=event("a.jsonl"), cost=CostBreakdown(), state="priced"),
        PricedEvent(event=event("b.jsonl"), cost=CostBreakdown(), state="priced"),
    ]
    report = build_report(
        priced,
        client_labels={},
        model_label=lambda m: m or "unknown",
        files_scanned=9,
    )
    assert report.files_in_slice == 2
    assert report.files_scanned == 9


# --- Phase 4: Meta.warning_summary and Meta.session_warnings --------------------------
#
# Both are computed in api.py from `aggregate.warning_groups_of()`, not from a field on
# SessionRow -- see the module docstring near `_session_lookup` in api.py for the exact
# shape (`dict[session_id, list[warning kind]]`) and why it lives on Meta instead.


def _codex_priced_event(
    *, source_file: str, session_id: str, tokens: int, cost: float
) -> PricedEvent:
    return PricedEvent(
        event=UsageEvent(
            source="codex",
            client="codex-cli",
            model="gpt-5-codex",
            timestamp=datetime(2026, 9, 5, 10, 0, tzinfo=UTC),
            session_id=session_id,
            tokens=TokenUsage(uncached_input=tokens, output=0),
            source_file=source_file,
        ),
        cost=CostBreakdown(uncached_input=cost),
        state="priced",
    )


def _warnings_analysis() -> Analysis:
    warnings = [
        # caution, resolves to sess-1 via sample.jsonl, delta_tokens = 5 - 100 = -95
        "codex: sample.jsonl: summed turns 5 vs session total 100 (7.6% drift)",
        # critical, no magnitude
        "codex: reset.jsonl: counter reset -- this session's cumulative token count "
        "decreased partway through the file, so its final total cannot be used as a "
        "reconciliation baseline",
        # info, pipeline-level -- previously never reached warning_groups_of() at all
        "content_retention_days is set but inert: no content is persisted in this version, "
        "so there is nothing for it to expire",
    ]
    events = [
        _codex_priced_event(
            source_file="sample.jsonl", session_id="sess-1", tokens=1000, cost=50.0
        ),
        _codex_priced_event(source_file="reset.jsonl", session_id="sess-2", tokens=500, cost=10.0),
    ]
    return Analysis(events=events, warnings=warnings, scan_warnings=warnings)


def test_meta_warning_summary_counts_instances_by_severity() -> None:
    with TestClient(create_app(_warnings_analysis())) as test_client:
        meta = test_client.get("/api/meta").json()

    summary = meta["warning_summary"]
    assert summary["caution"] == 1
    assert summary["critical"] == 1
    assert summary["info"] == 1
    # The only instance with a known delta_tokens (-95) resolves to sess-1, whose total
    # tokens/cost (1000, $50.00) give a proportional delta_cost of 95/1000 * 50 = $4.75.
    assert summary["total_delta_cost"] == pytest.approx(4.75)


def test_meta_session_warnings_keys_by_session_id_with_sorted_kinds() -> None:
    with TestClient(create_app(_warnings_analysis())) as test_client:
        meta = test_client.get("/api/meta").json()

    assert meta["session_warnings"] == {
        "sess-1": ["codex_drift"],
        "sess-2": ["codex_counter_reset"],
    }


def test_meta_warning_summary_is_all_zero_when_nothing_is_flagged(client: TestClient) -> None:
    meta = client.get("/api/meta").json()
    assert meta["warning_summary"] == {
        "critical": 0,
        "caution": 0,
        "info": 0,
        "total_delta_cost": 0.0,
    }
    assert meta["session_warnings"] == {}
