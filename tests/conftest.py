from __future__ import annotations

from pathlib import Path

import pytest

from ai_usage_cost.pipeline import Analysis, analyze
from ai_usage_cost.sources import registry

FIXTURES = Path(__file__).parent / "fixtures"

CLAUDE_BASIC = FIXTURES / "claude_code" / "basic"
CLAUDE_DEDUP = FIXTURES / "claude_code" / "dedup"
CLAUDE_UNKNOWN = FIXTURES / "claude_code" / "unknown"
CODEX_BASIC = FIXTURES / "codex" / "basic"
CODEX_DRIFT = FIXTURES / "codex" / "drift"

CLAUDE_TRACE = FIXTURES / "claude_code" / "trace"
CODEX_TRACE = FIXTURES / "codex" / "trace"
CODEX_TRACE_LEGACY = FIXTURES / "codex" / "trace-legacy"
ANTIGRAVITY_TRACE = FIXTURES / "antigravity" / "trace"

NO_ROOT = FIXTURES / "does-not-exist"


def analyze_roots(tmp_path: Path | None = None, **roots: Path) -> Analysis:
    all_roots = {source_id: [roots.get(source_id, NO_ROOT)] for source_id in registry()}
    db_path = (tmp_path or FIXTURES / ".tmp") / "test.db"
    if db_path.exists():
        db_path.unlink()
    return analyze(db_path=db_path, roots=all_roots)


@pytest.fixture
def analysis(tmp_path: Path) -> Analysis:
    return analyze_roots(tmp_path, **{"claude-code": CLAUDE_BASIC, "codex": CODEX_BASIC})


@pytest.fixture
def trace_analysis(tmp_path: Path) -> Analysis:
    return analyze_roots(
        tmp_path,
        **{
            "claude-code": CLAUDE_TRACE,
            "codex": CODEX_TRACE,
            "antigravity": ANTIGRAVITY_TRACE,
        },
    )
