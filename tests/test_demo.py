from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Any

import pytest

from ai_usage_cost import cli
from ai_usage_cost.demo import (
    CLAUDE_MODELS,
    CODEX_MODELS,
    DEFAULT_CONTEXT_WINDOW,
    DEMO_DB_PATH,
    DEMO_DIR,
    DEMO_ESTIMATED_MODEL,
    DEMO_UNPRICED_MODEL,
    context_window,
    demo_roots,
    generate,
)
from ai_usage_cost.pipeline import DEFAULT_DB_PATH, analyze
from ai_usage_cost.sources import registry


def test_demo_store_is_separate_from_the_real_store() -> None:
    assert DEMO_DB_PATH != DEFAULT_DB_PATH
    assert DEMO_DB_PATH.is_relative_to(DEMO_DIR)
    assert not DEFAULT_DB_PATH.is_relative_to(DEMO_DIR)


def test_every_source_is_pointed_inside_the_demo_tree(tmp_path: Path) -> None:
    roots = demo_roots(tmp_path)
    assert set(roots) == set(registry())
    for path in roots.values():
        assert path.is_relative_to(tmp_path)


def test_generate_twice_converges(tmp_path: Path) -> None:
    generate(tmp_path, days=5)
    generate(tmp_path, days=5)
    with closing(sqlite3.connect(tmp_path / "dyad" / "sqlite.db")) as conn:
        assert conn.execute("SELECT COUNT(*) FROM apps").fetchone()[0] == 4


def test_demo_analysis_reads_only_generated_files(tmp_path: Path) -> None:
    generate(tmp_path, days=10)
    db_path = tmp_path / "usage.db"
    analysis = analyze(
        db_path=db_path, roots={source: [path] for source, path in demo_roots(tmp_path).items()}
    )
    assert analysis.events
    with closing(sqlite3.connect(db_path)) as conn:
        scanned = [Path(row[0]) for row in conn.execute("SELECT path FROM files")]
    assert scanned
    for path in scanned:
        assert path.is_relative_to(tmp_path)


def test_off_removes_the_demo_tree_then_serves_real_data(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    demo_dir = tmp_path / "demo"
    demo_dir.mkdir()
    (demo_dir / "usage.db").write_text("stale", encoding="utf-8")
    calls: list[dict[str, Any]] = []
    monkeypatch.setattr(cli, "DEMO_DIR", demo_dir)
    monkeypatch.setattr(cli, "serve", lambda **kwargs: calls.append(kwargs))

    cli.demo(off=True)
    cli.demo(off=True)

    assert not demo_dir.exists()
    assert len(calls) == 2
    for kwargs in calls:
        assert kwargs.get("root") is None
        assert kwargs.get("db") is None


def _demo_analysis(tmp_path: Path) -> Any:
    generate(tmp_path, days=45)
    return analyze(
        db_path=tmp_path / "usage.db",
        roots={source: [path] for source, path in demo_roots(tmp_path).items()},
    )


def test_demo_shows_priced_estimated_and_unpriced_states(tmp_path: Path) -> None:
    analysis = _demo_analysis(tmp_path)
    by_model: dict[str, set[str]] = {}
    for item in analysis.events:
        if item.event.model and item.event.tokens is not None:
            by_model.setdefault(item.event.model, set()).add(item.state)
    for model, _weight in CLAUDE_MODELS + CODEX_MODELS:
        assert model in by_model, f"{model} never appears in the demo"
    estimated = {item.event.model for item in analysis.events if item.cost and item.cost.estimated}
    assert estimated == {DEMO_ESTIMATED_MODEL}
    unpriced = {item.event.model for item in analysis.events if item.state == "unpriced"}
    assert unpriced == {DEMO_UNPRICED_MODEL}
    # Everything else the demo logs with tokens is priced from its own row (exact or suffix).
    for model, states in by_model.items():
        if model not in {DEMO_ESTIMATED_MODEL, DEMO_UNPRICED_MODEL}:
            assert states == {"priced"}, f"{model} is {states}"
    table = analysis.table
    assert table.match_of("claude-haiku-4-5-20251001").kind == "suffix"
    assert table.match_of(DEMO_ESTIMATED_MODEL).kind == "estimated"
    assert table.unpriced_note(DEMO_UNPRICED_MODEL)


def test_demo_context_windows_come_from_the_rate_table() -> None:
    assert context_window("claude-opus-5-5") == 1_000_000
    assert context_window("claude-haiku-4-5-20251001") == 200_000
    assert context_window(DEMO_UNPRICED_MODEL) == DEFAULT_CONTEXT_WINDOW


def test_demo_is_deterministic(tmp_path: Path) -> None:
    def fingerprint(root: Path) -> list[tuple[str, str]]:
        generate(root, days=10)
        names = sorted(path.parent.name for path in (root / "codex").rglob("rollout-*.jsonl"))
        models = sorted(
            line.split('"model"')[1][:40]
            for path in (root / "codex").rglob("rollout-*.jsonl")
            for line in path.read_text("utf-8").splitlines()[:1]
        )
        return list(zip(names, models, strict=True))

    assert fingerprint(tmp_path / "a") == fingerprint(tmp_path / "b")
