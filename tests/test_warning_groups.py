from __future__ import annotations

import pytest

from ai_usage_cost.aggregate import WarningSeverity, warning_groups_of


def test_repeated_drift_warnings_collapse_into_one_group() -> None:
    warnings = [
        "codex: a.jsonl: summed turns 0 vs session total 10,419 (100.0% drift)",
        "codex: b.jsonl: summed turns 610,633 vs session total 282,295 (116.3% drift)",
    ]
    groups = warning_groups_of(warnings)
    assert len(groups) == 1
    assert groups[0].kind == "codex_drift"
    assert groups[0].count == 2
    assert groups[0].warnings == warnings


def test_different_kinds_stay_in_separate_groups_sorted_by_count() -> None:
    warnings = [
        "a.jsonl: skipped 3 unparsable lines",
        "codex: a.jsonl: summed turns 0 vs session total 10 (100.0% drift)",
        "codex: b.jsonl: summed turns 0 vs session total 10 (100.0% drift)",
    ]
    groups = warning_groups_of(warnings)
    assert [g.kind for g in groups] == ["codex_drift", "unparsable_lines"]
    assert [g.count for g in groups] == [2, 1]


def test_an_unrecognized_warning_lands_in_other_rather_than_disappearing() -> None:
    groups = warning_groups_of(["something entirely unexpected happened"])
    assert len(groups) == 1
    assert groups[0].kind == "other"
    assert groups[0].count == 1


def test_no_warnings_produces_no_groups() -> None:
    assert warning_groups_of([]) == []


def test_codex_drift_summary_names_the_worst_percentage() -> None:
    warnings = [
        "codex: a.jsonl: summed turns 0 vs session total 10 (100.0% drift)",
        "codex: b.jsonl: summed turns 5 vs session total 100 (7.6% drift)",
    ]
    summary = warning_groups_of(warnings)[0].summary
    assert "2 Codex files" in summary
    assert "100.0%" in summary


# --- Phase 4: severity, magnitude parsing, and the pipeline-level warnings -------------
#
# The message strings below are copied verbatim from the templates in the *current*
# (post phase-2) `codex.py._reconcile()` and `pipeline.py.analyze()` -- not from the
# warnings.md audit report's Part A examples, whose exact numbers predate phase 2's
# dedupe/forked-thread/counter-reset fixes.


def test_plain_codex_drift_message_parses_delta_tokens_and_is_caution_severity() -> None:
    # codex.py._reconcile(), non-forked branch: f"codex: {name}: summed turns {n:,} vs
    # session total {n:,} ({pct:.1%} drift)".
    warning = "codex: b.jsonl: summed turns 5 vs session total 100 (7.6% drift)"
    group = warning_groups_of([warning])[0]
    instance = group.instances[0]
    assert instance.kind == "codex_drift"
    assert instance.delta_tokens == 5 - 100
    assert instance.severity == WarningSeverity.caution
    assert group.total_delta_tokens == 95


def test_large_codex_drift_percentage_is_classified_critical() -> None:
    # Synthetic magnitude (not a real post-phase-2 example -- the worst real case in the
    # audit report is now a counter-reset warning, see below) purely to exercise the
    # severity threshold on a still-valid "summed turns ... drift)" message shape.
    warning = (
        "codex: worst.jsonl: summed turns 37,829,135 vs session total 353,400 (10604.3% drift)"
    )
    instance = warning_groups_of([warning])[0].instances[0]
    assert instance.delta_tokens == 37_829_135 - 353_400
    assert instance.severity == WarningSeverity.critical


def test_forked_thread_message_parses_into_its_own_kind_with_a_caution_default() -> None:
    # codex.py._reconcile(), forked branch: f"codex: {name}: forked thread -- summed turns
    # {n:,} vs {n:,} after excluding {n:,} tokens inherited from the parent thread
    # ({pct:.1%} still unexplained)".
    warning = (
        "codex: fork.jsonl: forked thread -- summed turns 10,500 vs 1,010,000 after "
        "excluding 999,500 tokens inherited from the parent thread (99.0% still unexplained)"
    )
    group = warning_groups_of([warning])[0]
    instance = group.instances[0]
    assert group.kind == "codex_forked_thread"
    assert instance.kind == "codex_forked_thread"
    assert instance.delta_tokens == 10_500 - 1_010_000
    assert instance.severity == WarningSeverity.caution
    assert instance.auto_corrected is True
    assert instance.likely_cause is not None and "forked" in instance.likely_cause


def test_counter_reset_message_parses_into_its_own_kind_with_no_magnitude() -> None:
    # codex.py._reconcile(), reset_detected branch -- carries no numbers at all, since the
    # file's own cumulative counter is unusable as a baseline.
    warning = (
        "codex: reset.jsonl: counter reset -- this session's cumulative token count "
        "decreased partway through the file, so its final total cannot be used as a "
        "reconciliation baseline"
    )
    group = warning_groups_of([warning])[0]
    instance = group.instances[0]
    assert group.kind == "codex_counter_reset"
    assert instance.delta_tokens is None
    assert instance.severity == WarningSeverity.critical


def test_session_lookup_resolves_session_id_and_affected_sessions() -> None:
    warning = "codex: sample.jsonl: summed turns 5 vs session total 100 (7.6% drift)"
    groups = warning_groups_of([warning], session_lookup={"sample.jsonl": "sess-42"})
    instance = groups[0].instances[0]
    assert instance.session_id == "sess-42"
    assert groups[0].affected_sessions == 1


def test_session_totals_price_the_known_delta_proportionally() -> None:
    warning = "codex: sample.jsonl: summed turns 5 vs session total 100 (7.6% drift)"
    groups = warning_groups_of(
        [warning],
        session_lookup={"sample.jsonl": "sess-42"},
        session_totals={"sess-42": (1000, 50.0)},
    )
    instance = groups[0].instances[0]
    # delta_tokens is -95; proportional cost = 95/1000 * $50.00 = $4.75.
    assert instance.delta_cost == pytest.approx(4.75)
    assert groups[0].total_delta_cost == pytest.approx(4.75)


def test_without_session_data_delta_cost_stays_unknown() -> None:
    warning = "codex: sample.jsonl: summed turns 5 vs session total 100 (7.6% drift)"
    instance = warning_groups_of([warning])[0].instances[0]
    assert instance.session_id is None
    assert instance.delta_cost is None


def test_unknown_model_rate_pipeline_warning_is_now_grouped() -> None:
    # pipeline.py analyze(): f"no rate for model {model!r} ({tokens:,} tokens) -- add it to
    # rates.json; it is excluded from the cost total, but its tokens are still counted".
    warning = (
        "no rate for model 'gpt-9' (1,234 tokens) -- add it to rates.json; it is excluded "
        "from the cost total, but its tokens are still counted"
    )
    groups = warning_groups_of([warning])
    assert len(groups) == 1
    assert groups[0].kind == "unknown_model_rate"
    assert groups[0].instances[0].severity == WarningSeverity.caution


def test_inert_retention_config_pipeline_warning_is_now_grouped() -> None:
    warning = (
        "content_retention_days is set but inert: no content is persisted in this version, "
        "so there is nothing for it to expire"
    )
    groups = warning_groups_of([warning])
    assert len(groups) == 1
    assert groups[0].kind == "inert_retention_config"
    assert groups[0].instances[0].severity == WarningSeverity.info


def test_inherited_pricing_pipeline_warning_is_now_grouped() -> None:
    warning = (
        "model 'gpt-9' has no exact rates.json row of its own -- priced from the GPT-9 rate "
        "because no exact row exists; check whether 'gpt-9' needs its own"
    )
    groups = warning_groups_of([warning])
    assert len(groups) == 1
    assert groups[0].kind == "inherited_pricing"


def test_warnings_alias_still_lists_raw_messages_for_back_compat() -> None:
    warnings = [
        "codex: a.jsonl: summed turns 0 vs session total 10 (100.0% drift)",
        "codex: b.jsonl: summed turns 5 vs session total 100 (7.6% drift)",
    ]
    group = warning_groups_of(warnings)[0]
    assert group.warnings == warnings
    assert [instance.message for instance in group.instances] == warnings


def test_groups_with_unknown_magnitude_sort_by_count_when_deltas_are_all_unknown() -> None:
    warnings = [
        "a.jsonl: skipped 3 unparsable lines",
        "b.jsonl: skipped 3 unparsable lines",
        "c.jsonl: cannot parse chat blob",
    ]
    groups = warning_groups_of(warnings)
    assert [g.kind for g in groups] == ["unparsable_lines", "chat_data_parse_error"]
    assert [g.count for g in groups] == [2, 1]


def test_worst_example_is_the_most_impactful_member() -> None:
    warnings = [
        "codex: a.jsonl: summed turns 0 vs session total 10 (100.0% drift)",
        "codex: b.jsonl: summed turns 37,829,135 vs session total 353,400 (10604.3% drift)",
    ]
    group = warning_groups_of(warnings)[0]
    assert group.worst_example is not None
    assert group.worst_example.message == warnings[1]
