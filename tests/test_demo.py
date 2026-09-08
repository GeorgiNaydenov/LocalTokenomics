from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Any

import pytest

from ai_usage_cost import cli
from ai_usage_cost.demo import DEMO_DB_PATH, DEMO_DIR, demo_roots, generate
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
