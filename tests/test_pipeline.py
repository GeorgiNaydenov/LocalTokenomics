from __future__ import annotations

import json
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from ai_usage_cost import privacy
from ai_usage_cost.aggregate import Report, build_report
from ai_usage_cost.models import PricedEvent, TokenUsage, UsageEvent
from ai_usage_cost.pipeline import Analysis, filter_events, report_of
from ai_usage_cost.pricing import RateTable, price_event
from conftest import CLAUDE_BASIC, CLAUDE_TRACE, CODEX_BASIC, CODEX_TRACE, analyze_roots

TABLE = RateTable.load()
_DEFAULT_TOKENS = object()

FLAGS = {
    ("claude-code", "good"): (True, 0, "successful"),
    ("claude-code", "bad"): (True, 4, "failed"),
}


def priced(
    *,
    day: str,
    client: str = "claude-code",
    source: str = "claude-code",
    provider: str | None = None,
    model: str = "claude-opus-5",
    session_id: str = "s1",
    project: str | None = "alpha",
    is_sidechain: bool = False,
    output: int = 1_000,
    tokens: TokenUsage | None | object = _DEFAULT_TOKENS,
) -> PricedEvent:
    resolved_tokens = (
        TokenUsage(uncached_input=1_000, output=output) if tokens is _DEFAULT_TOKENS else tokens
    )
    event = UsageEvent(
        source=source,
        client=client,
        provider=provider,
        timestamp=datetime.fromisoformat(day).replace(tzinfo=UTC),
        model=model,
        session_id=session_id,
        project=project,
        tokens=resolved_tokens,  # type: ignore[arg-type]
        is_sidechain=is_sidechain,
    )
    cost, state = price_event(event, TABLE)
    return PricedEvent(event=event, cost=cost, state=state)


def test_since_and_until_include_the_boundary_days() -> None:
    events = [
        priced(day="2026-08-19T23:59:59"),
        priced(day="2026-08-20T00:00:00"),
        priced(day="2026-08-20T23:59:59"),
        priced(day="2026-08-21T00:00:00"),
    ]
    kept = filter_events(events, since=date(2026, 8, 20), until=date(2026, 8, 20))
    assert [item.event.timestamp.isoformat() for item in kept] == [
        "2026-08-20T00:00:00+00:00",
        "2026-08-20T23:59:59+00:00",
    ]


def test_since_alone_keeps_everything_from_that_day_on() -> None:
    events = [priced(day="2026-08-19T12:00:00"), priced(day="2026-08-20T00:00:00")]
    assert len(filter_events(events, since=date(2026, 8, 20))) == 1


def test_until_alone_keeps_everything_up_to_the_end_of_that_day() -> None:
    events = [priced(day="2026-08-20T23:59:59"), priced(day="2026-08-21T00:00:00")]
    assert len(filter_events(events, until=date(2026, 8, 20))) == 1


def test_no_filters_keeps_everything() -> None:
    events = [priced(day="2026-08-19T12:00:00"), priced(day="2026-08-25T12:00:00")]
    assert filter_events(events) == events


def test_clients_models_and_projects_narrow_the_list() -> None:
    events = [
        priced(day="2026-08-20T10:00:00", client="claude-code", model="claude-opus-5"),
        priced(
            day="2026-08-20T10:00:00", client="codex-cli", model="gpt-5-codex", project="beta"
        ),
        priced(
            day="2026-08-20T10:00:00", client="codex-cli", model="gpt-5.6-terra", project="beta"
        ),
    ]
    assert len(filter_events(events, clients=["codex-cli"])) == 2
    assert len(filter_events(events, models=["gpt-5-codex"])) == 1
    assert len(filter_events(events, projects=["alpha"])) == 1
    assert len(filter_events(events, clients=["codex-cli"], models=["claude-opus-5"])) == 0


def test_providers_narrow_the_list() -> None:
    events = [
        priced(day="2026-08-20T10:00:00", provider="anthropic"),
        priced(day="2026-08-20T10:00:00", provider="bedrock"),
    ]
    assert len(filter_events(events, providers=["bedrock"])) == 1


def test_empty_filter_sequences_are_treated_as_no_filter() -> None:
    events = [priced(day="2026-08-20T10:00:00")]
    assert len(filter_events(events, clients=[], models=[], projects=[])) == 1


def test_include_sidechains_false_drops_subagent_events() -> None:
    events = [
        priced(day="2026-08-20T10:00:00"),
        priced(day="2026-08-20T10:01:00", is_sidechain=True),
    ]
    assert len(filter_events(events, include_sidechains=True)) == 2
    kept = filter_events(events, include_sidechains=False)
    assert len(kept) == 1
    assert kept[0].event.is_sidechain is False


def test_states_narrow_the_list() -> None:
    events = [
        priced(day="2026-08-20T10:00:00", model="claude-opus-5"),
        priced(day="2026-08-20T10:01:00", model="totally-unknown-model"),
    ]
    assert [item.state for item in events] == ["priced", "unpriced"]
    assert len(filter_events(events, states=["priced"])) == 1
    assert len(filter_events(events, states=["unpriced"])) == 1
    assert len(filter_events(events, states=["priced", "unpriced"])) == 2


def test_search_matches_case_insensitively_across_several_fields() -> None:
    events = [
        priced(
            day="2026-08-20T10:00:00", client="claude-code", model="claude-opus-5",
            project="Alpha", session_id="abc-123",
        ),
        priced(
            day="2026-08-20T10:01:00", client="codex-cli", model="gpt-5-codex",
            project="beta", session_id="xyz-789",
        ),
    ]
    assert len(filter_events(events, search="ALPHA")) == 1
    assert len(filter_events(events, search="gpt-5-codex")) == 1
    assert len(filter_events(events, search="xyz-789")) == 1
    assert filter_events(events, search="no-such-term") == []


@pytest.fixture
def report(analysis: Analysis) -> Report:
    return report_of(analysis)


def test_every_breakdown_sums_to_the_grand_total(report: Report) -> None:
    total = report.totals.cost.total
    assert total > 0
    for buckets in (report.by_model, report.by_client, report.by_project, report.by_day):
        assert sum(bucket.cost.total for bucket in buckets) == pytest.approx(total)
        assert sum(bucket.events for bucket in buckets) == report.totals.events


def test_token_buckets_also_sum_to_the_grand_total(report: Report) -> None:
    for buckets in (report.by_model, report.by_client, report.by_project):
        assert sum(bucket.tokens.total for bucket in buckets) == report.totals.tokens.total


def test_buckets_cover_the_fixture_keys(report: Report) -> None:
    assert {bucket.key for bucket in report.by_client} == {"claude-code", "codex-cli"}
    assert {bucket.label for bucket in report.by_client} == {"Claude Code", "Codex CLI"}
    assert {bucket.key for bucket in report.by_project} == {"alpha", "beta"}
    assert {bucket.key for bucket in report.by_day} == {"2026-08-20", "2026-08-21"}
    assert {bucket.key for bucket in report.by_model} == {
        "claude-opus-5", "claude-sonnet-5", "claude-haiku-4-5", "gpt-5-codex", "gpt-5.6-terra",
    }
    assert "Claude Opus 5" in {bucket.label for bucket in report.by_model}


def test_buckets_are_sorted_by_cost_descending(report: Report) -> None:
    costs = [bucket.cost.total for bucket in report.by_model]
    assert costs == sorted(costs, reverse=True)


def test_sessions_are_counted_distinctly_per_source_and_session_id(report: Report) -> None:
    assert report.totals.events == 8
    assert report.totals.sessions == 2
    assert {bucket.sessions for bucket in report.by_client} == {1}


def test_the_same_session_id_under_two_sources_counts_twice() -> None:
    events = [
        priced(
            day="2026-08-20T10:00:00", source="claude-code", client="claude-code",
            session_id="shared",
        ),
        priced(
            day="2026-08-20T10:00:00", source="codex", client="codex-cli",
            model="gpt-5-codex", session_id="shared",
        ),
    ]
    built = build_report(events, client_labels={}, model_label=lambda m: m or "unknown")
    assert built.totals.sessions == 2


def test_series_has_one_point_per_day_client_provider_and_model(report: Report) -> None:
    keys = [
        (point.day.isoformat(), point.client, point.provider, point.model)
        for point in report.series
    ]
    assert len(keys) == len(set(keys)) == 5
    assert keys == sorted(keys)
    assert sum(point.cost for point in report.series) == pytest.approx(report.totals.cost.total)
    assert sum(point.tokens for point in report.series) == report.totals.tokens.total


def test_sessions_rows_summarise_each_conversation(report: Report) -> None:
    assert len(report.sessions) == 2
    by_client = {row.client: row for row in report.sessions}
    claude = by_client["claude-code"]
    assert claude.project == "alpha"
    assert claude.request_count == 4
    assert claude.models == ["claude-haiku-4-5", "claude-opus-5", "claude-sonnet-5"]
    assert claude.start_time.isoformat() == "2026-08-20T10:00:05+00:00"
    assert claude.end_time.isoformat() == "2026-08-20T10:05:00+00:00"
    assert claude.cost_state == "priced"
    assert sum(row.cost.total if row.cost else 0.0 for row in report.sessions) == pytest.approx(
        report.totals.cost.total
    )


def test_totals_span_the_first_and_last_event(report: Report) -> None:
    assert report.totals.first_event.isoformat() == "2026-08-20T10:00:05+00:00"
    assert report.totals.last_event.isoformat() == "2026-08-21T09:06:00+00:00"


def test_report_carries_scan_metadata(analysis: Analysis, report: Report) -> None:
    assert report.files_scanned == 2
    assert report.rates_as_of == analysis.table.as_of
    assert report.unknown_models == []
    assert report.warnings == []


def test_report_of_applies_filters(analysis: Analysis) -> None:
    narrowed = report_of(analysis, clients=["codex-cli"])
    assert {bucket.key for bucket in narrowed.by_client} == {"codex-cli"}
    assert narrowed.totals.events == 4
    assert narrowed.files_scanned == 2


def test_analyze_sorts_events_by_timestamp() -> None:
    found = analyze_roots(**{"claude-code": CLAUDE_BASIC, "codex": CODEX_BASIC})
    stamps = [item.event.timestamp for item in found.events]
    assert stamps == sorted(stamps)


def test_analysis_client_labels_cover_the_registry(analysis: Analysis) -> None:
    assert analysis.client_labels["claude-code"] == "Claude Code"
    assert analysis.client_labels["codex-cli"] == "Codex CLI"


def test_facets_are_computed_from_the_base_slice_not_the_filtered_one() -> None:
    events = [
        priced(day="2026-08-20T10:00:00", client="claude-code", model="claude-opus-5",
               session_id="s1"),
        priced(day="2026-08-20T10:00:00", client="claude-code", model="claude-sonnet-5",
               session_id="s2"),
        priced(day="2026-08-20T10:00:00", client="codex-cli", model="gpt-5-codex",
               session_id="s3"),
    ]
    analysis = Analysis(events=events, table=TABLE)
    full = report_of(analysis)
    narrowed = report_of(analysis, models=["claude-opus-5"])

    assert full.facets.clients["claude-code"] == 2
    assert narrowed.totals.sessions == 1
    assert narrowed.facets.clients["claude-code"] == 2


def test_report_counts_only_the_unpriced_models_inside_the_window() -> None:
    events = [
        priced(day="2026-07-01T10:00:00", model="totally-unknown-model", session_id="s1"),
        priced(day="2026-08-20T10:00:00", model="another-unknown-model", session_id="s2"),
    ]
    analysis = Analysis(events=events, table=TABLE)

    everything = report_of(analysis)
    just_august = report_of(analysis, since=date(2026, 8, 1))

    assert {u.model for u in everything.unknown_models} == {
        "totally-unknown-model",
        "another-unknown-model",
    }
    assert {u.model for u in just_august.unknown_models} == {"another-unknown-model"}


def test_token_usage_total_excludes_reasoning_output() -> None:
    tokens = TokenUsage(uncached_input=100, cache_read=10, output=50, reasoning_output=30)
    assert tokens.total == 160
    assert tokens.output == 50


def session_events() -> list[PricedEvent]:
    return [
        priced(day="2026-08-20T10:00:00", session_id="good"),
        priced(day="2026-08-20T10:01:00", session_id="good", model="claude-sonnet-5"),
        priced(day="2026-08-20T10:02:00", session_id="bad"),
        priced(day="2026-08-20T10:03:00", session_id="quiet"),
    ]


def test_outcome_traced_and_error_filters_keep_or_drop_a_whole_session() -> None:
    events = session_events()

    def kept(**filters: object) -> set[str]:
        return {
            item.event.session_id
            for item in filter_events(events, session_flags=FLAGS, **filters)  # type: ignore[arg-type]
        }

    assert kept(outcomes=["successful"]) == {"good"}
    assert kept(outcomes=["successful", "failed"]) == {"good", "bad"}
    assert kept(outcomes=["unrated"]) == {"quiet"}
    assert kept(traced=True) == {"good", "bad"}
    assert kept(traced=False) == {"quiet"}
    assert kept(has_errors=True) == {"bad"}
    assert kept(has_errors=False) == {"good", "quiet"}
    assert kept(outcomes=["failed"], has_errors=False) == set()
    assert len(filter_events(events, session_flags=FLAGS)) == len(events)


def test_session_rows_and_facets_carry_the_stored_outcome() -> None:
    analysis = Analysis(events=session_events(), table=TABLE, session_flags=dict(FLAGS))
    report = report_of(analysis)
    rows = {row.session_id: row for row in report.sessions}

    assert (rows["good"].outcome, rows["good"].traced, rows["good"].error_count) == (
        "successful", True, 0
    )
    assert (rows["bad"].outcome, rows["bad"].traced, rows["bad"].error_count) == ("failed", True, 4)
    assert (rows["quiet"].outcome, rows["quiet"].traced, rows["quiet"].error_count) == (
        "unrated", False, 0
    )
    assert report.facets.outcomes == {"successful": 1, "failed": 1, "unrated": 1}


def test_analyze_records_its_store_and_the_session_flags_it_read(tmp_path: Path) -> None:
    found = analyze_roots(tmp_path, **{"claude-code": CLAUDE_TRACE, "codex": CODEX_TRACE})

    assert found.db_path == tmp_path / "test.db"
    traced, errors, outcome = found.session_flags[("claude-code", "sess-trace")]
    assert (traced, errors, outcome) == (True, 1, "unrated")
    assert found.session_flags[("codex", "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")][1] == 0


def test_analyze_forwards_the_privacy_config_to_ingest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = tmp_path / "config.json"
    config.write_text(
        json.dumps({"exclude_projects": ["gamma"], "content_retention_days": 7}), "utf-8"
    )
    monkeypatch.setattr(privacy, "DEFAULT_CONFIG_PATH", config)

    found = analyze_roots(tmp_path, **{"claude-code": CLAUDE_TRACE})

    assert found.session_flags == {}
    assert [item.event.session_id for item in found.events] == ["sess-trace"] * len(found.events)
    assert found.events
    assert any("content_retention_days" in warning for warning in found.warnings)


def test_unavailable_and_unpriced_events_count_but_dont_cost() -> None:
    events = [
        priced(day="2026-08-20T10:00:00", tokens=None),
        priced(day="2026-08-20T10:01:00", model="totally-unknown-model"),
        priced(day="2026-08-20T10:02:00"),
    ]
    built = build_report(events, client_labels={}, model_label=lambda m: m or "unknown")
    assert built.totals.events == 3
    assert built.totals.sessions == 1
    assert built.totals.cost.total == pytest.approx(events[2].cost.total)
