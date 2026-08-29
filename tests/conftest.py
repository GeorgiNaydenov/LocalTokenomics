"""Shared fixture paths and helpers.

Every test drives the real code over real JSONL: either one of the small committed
files under ``tests/fixtures/`` or a file written into ``tmp_path``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_usage_cost.pipeline import Analysis, analyze

FIXTURES = Path(__file__).parent / "fixtures"

CLAUDE_BASIC = FIXTURES / "claude_code" / "basic"
CLAUDE_DEDUP = FIXTURES / "claude_code" / "dedup"
CLAUDE_UNKNOWN = FIXTURES / "claude_code" / "unknown"
CODEX_BASIC = FIXTURES / "codex" / "basic"
CODEX_DRIFT = FIXTURES / "codex" / "drift"

# A path that does not exist: scan() skips missing roots, which is how a test asks for
# one source only without ever falling back to the developer's real ~/.claude logs.
NO_ROOT = FIXTURES / "does-not-exist"


def analyze_roots(claude: Path = NO_ROOT, codex: Path = NO_ROOT) -> Analysis:
    """Analyse the given roots and nothing else.

    Both source ids are always supplied so no source can silently fall back to its
    default root in the developer's home directory.
    """
    return analyze(
        tools=["claude-code", "codex"],
        roots={"claude-code": [claude], "codex": [codex]},
    )


@pytest.fixture
def analysis() -> Analysis:
    """One Claude Code session plus one Codex rollout, parsed and priced."""
    return analyze_roots(claude=CLAUDE_BASIC, codex=CODEX_BASIC)
