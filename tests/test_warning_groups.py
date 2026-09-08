from __future__ import annotations

from ai_usage_cost.aggregate import warning_groups_of


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
