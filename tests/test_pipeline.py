"""Filtering and report aggregation."""

from __future__ import annotations

from datetime import UTC, date, datetime

import pytest

from ai_usage_cost.aggregate import Report, build_report
from ai_usage_cost.models import PricedEvent, TokenUsage, UsageEvent
from ai_usage_cost.pipeline import Analysis, filter_events, report_of
from ai_usage_cost.pricing import Pricer
from conftest import CLAUDE_BASIC, CODEX_BASIC, analyze_roots

PRICER = Pricer()


def priced(
    *,
    day: str,
    tool: str = "claude-code",
    model: str = "claude-opus-5",
    session_id: str = "s1",
    project: str | None = "alpha",
    is_sidechain: bool = False,
    output: int = 1_000,
) -> PricedEvent:
    event = UsageEvent(
        tool=tool,
        timestamp=datetime.fromisoformat(day).replace(tzinfo=UTC),
        model=model,
        session_id=session_id,
        project=project,
        tokens=TokenUsage(uncached_input=1_000, output=output),
        is_sidechain=is_sidechain,
    )
    cost = PRICER.price(event)
    assert cost is not None
    return PricedEvent(event=event, cost=cost)


# ------------------------------------------------------------------------ filtering


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


def test_tools_models_and_projects_narrow_the_list() -> None:
    events = [
        priced(day="2026-08-20T10:00:00", tool="claude-code", model="claude-opus-5"),
        priced(day="2026-08-20T10:00:00", tool="codex", model="gpt-5-codex", project="beta"),
        priced(day="2026-08-20T10:00:00", tool="codex", model="gpt-5.6-terra", project="beta"),
    ]
    assert len(filter_events(events, tools=["codex"])) == 2
    assert len(filter_events(events, models=["gpt-5-codex"])) == 1
    assert len(filter_events(events, projects=["alpha"])) == 1
    assert len(filter_events(events, tools=["codex"], models=["claude-opus-5"])) == 0


def test_empty_filter_sequences_are_treated_as_no_filter() -> None:
    events = [priced(day="2026-08-20T10:00:00")]
    assert len(filter_events(events, tools=[], models=[], projects=[])) == 1


def test_include_sidechains_false_drops_subagent_events() -> None:
    events = [
        priced(day="2026-08-20T10:00:00"),
        priced(day="2026-08-20T10:01:00", is_sidechain=True),
    ]
    assert len(filter_events(events, include_sidechains=True)) == 2
    kept = filter_events(events, include_sidechains=False)
    assert len(kept) == 1
    assert kept[0].event.is_sidechain is False


# ---------------------------------------------------------------------- build_report


@pytest.fixture
def report(analysis: Analysis) -> Report:
    return report_of(analysis)


def test_every_breakdown_sums_to_the_grand_total(report: Report) -> None:
    total = report.totals.cost.total
    assert total > 0
    for buckets in (report.by_model, report.by_tool, report.by_project, report.by_day):
        assert sum(bucket.cost.total for bucket in buckets) == pytest.approx(total)
        assert sum(bucket.events for bucket in buckets) == report.totals.events


def test_token_buckets_also_sum_to_the_grand_total(report: Report) -> None:
    for buckets in (report.by_model, report.by_tool, report.by_project):
        assert sum(bucket.tokens.total for bucket in buckets) == report.totals.tokens.total


def test_buckets_cover_the_fixture_keys(report: Report) -> None:
    assert {bucket.key for bucket in report.by_tool} == {"claude-code", "codex"}
    assert {bucket.label for bucket in report.by_tool} == {"Claude Code", "Codex CLI"}
    assert {bucket.key for bucket in report.by_project} == {"alpha", "beta"}
    assert {bucket.key for bucket in report.by_day} == {"2026-08-20", "2026-08-21"}
    assert {bucket.key for bucket in report.by_model} == {
        "claude-opus-5",
        "claude-sonnet-5",
        "claude-haiku-4-5",
        "gpt-5-codex",
        "gpt-5.6-terra",
    }
    assert "Claude Opus 5" in {bucket.label for bucket in report.by_model}


def test_buckets_are_sorted_by_cost_descending(report: Report) -> None:
    costs = [bucket.cost.total for bucket in report.by_model]
    assert costs == sorted(costs, reverse=True)


def test_sessions_are_counted_distinctly_per_tool_and_session_id(report: Report) -> None:
    assert report.totals.events == 8
    assert report.totals.sessions == 2
    assert {bucket.sessions for bucket in report.by_tool} == {1}


def test_the_same_session_id_under_two_tools_counts_twice() -> None:
    events = [
        priced(day="2026-08-20T10:00:00", tool="claude-code", session_id="shared"),
        priced(day="2026-08-20T10:00:00", tool="codex", model="gpt-5-codex",
               session_id="shared"),
    ]
    built = build_report(events, tool_labels={}, model_label=str)
    assert built.totals.sessions == 2


def test_series_has_one_point_per_day_tool_and_model(report: Report) -> None:
    keys = [(point.day.isoformat(), point.tool, point.model) for point in report.series]
    assert len(keys) == len(set(keys)) == 5
    assert keys == sorted(keys)
    assert sum(point.cost for point in report.series) == pytest.approx(report.totals.cost.total)
    assert sum(point.tokens for point in report.series) == report.totals.tokens.total


def test_sessions_rows_summarise_each_conversation(report: Report) -> None:
    assert len(report.sessions) == 2
    by_tool = {row.tool: row for row in report.sessions}
    claude = by_tool["claude-code"]
    assert claude.project == "alpha"
    assert claude.events == 4
    assert claude.models == ["claude-haiku-4-5", "claude-opus-5", "claude-sonnet-5"]
    assert claude.started.isoformat() == "2026-08-20T10:00:05+00:00"
    assert claude.ended.isoformat() == "2026-08-20T10:05:00+00:00"
    assert sum(row.cost for row in report.sessions) == pytest.approx(report.totals.cost.total)


def test_totals_span_the_first_and_last_event(report: Report) -> None:
    assert report.totals.first_event.isoformat() == "2026-08-20T10:00:05+00:00"
    assert report.totals.last_event.isoformat() == "2026-08-21T09:06:00+00:00"


def test_report_carries_scan_metadata(analysis: Analysis, report: Report) -> None:
    assert report.files_scanned == 2
    assert report.rates_as_of == analysis.pricer.table.as_of
    assert report.unknown_models == []
    assert report.warnings == []


def test_report_of_applies_filters(analysis: Analysis) -> None:
    narrowed = report_of(analysis, tools=["codex"])
    assert {bucket.key for bucket in narrowed.by_tool} == {"codex"}
    assert narrowed.totals.events == 4
    # The unfiltered scan metadata is preserved.
    assert narrowed.files_scanned == 2


def test_analyze_sorts_events_by_timestamp() -> None:
    found = analyze_roots(claude=CLAUDE_BASIC, codex=CODEX_BASIC)
    stamps = [item.event.timestamp for item in found.priced]
    assert stamps == sorted(stamps)


def test_analysis_tool_labels_cover_the_registry(analysis: Analysis) -> None:
    assert analysis.tool_labels["claude-code"] == "Claude Code"
    assert analysis.tool_labels["codex"] == "Codex CLI"
