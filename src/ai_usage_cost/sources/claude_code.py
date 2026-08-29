"""Claude Code transcripts: ``~/.claude/projects/<encoded-cwd>/<session>.jsonl``.

Usage lives on ``type == "assistant"`` records under ``message.usage``. Anthropic reports
the four billable buckets separately -- ``input_tokens`` already excludes cache reads and
cache writes -- so they map onto :class:`TokenUsage` directly.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from ..models import TokenUsage, UsageEvent
from .base import JsonlSource, parse_timestamp, read_json_lines, register

SYNTHETIC_MODELS = {"<synthetic>", "synthetic"}


class ClaudeCodeSource(JsonlSource):
    id = "claude-code"
    label = "Claude Code"

    def default_roots(self) -> list[Path]:
        home = Path.home()
        return [home / ".claude" / "projects", home / ".config" / "claude" / "projects"]

    def __init__(self) -> None:
        # Resumed sessions and sidechain copies repeat the same assistant record across
        # files, so the dedup key has to be held for the whole scan, not per file.
        self._seen: set[tuple[str, str]] = set()

    def scan(self, roots=None):  # type: ignore[override]
        self._seen = set()
        return super().scan(roots)

    def iter_file(self, path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
        session_id = path.stem
        for record in read_json_lines(path, warnings):
            if record.get("type") != "assistant":
                continue
            message = record.get("message")
            if not isinstance(message, dict):
                continue
            usage = message.get("usage")
            if not isinstance(usage, dict):
                continue

            model = str(message.get("model") or "")
            if not model or model in SYNTHETIC_MODELS:
                continue

            key = (str(message.get("id") or ""), str(record.get("requestId") or ""))
            if key != ("", "") and key in self._seen:
                continue
            self._seen.add(key)

            tokens = _tokens_from_usage(usage)
            if tokens.total == 0:
                continue

            yield UsageEvent(
                tool=self.id,
                timestamp=parse_timestamp(record.get("timestamp"), path),
                model=model,
                session_id=str(record.get("sessionId") or session_id),
                project=_project_name(record, path),
                tokens=tokens,
                is_sidechain=bool(record.get("isSidechain")),
                tier=_tier(usage),
                source_file=str(path),
            )


def _tokens_from_usage(usage: dict) -> TokenUsage:
    # Never sum usage["iterations"] -- the top-level block is already their total.
    creation = usage.get("cache_creation")
    write_5m = write_1h = 0
    if isinstance(creation, dict):
        write_5m = _int(creation.get("ephemeral_5m_input_tokens"))
        write_1h = _int(creation.get("ephemeral_1h_input_tokens"))
    if write_5m == 0 and write_1h == 0:
        # Older transcripts report only the total; assume the 5m TTL.
        write_5m = _int(usage.get("cache_creation_input_tokens"))

    details = usage.get("output_tokens_details")
    thinking = _int(details.get("thinking_tokens")) if isinstance(details, dict) else 0

    return TokenUsage(
        uncached_input=_int(usage.get("input_tokens")),
        cache_read=_int(usage.get("cache_read_input_tokens")),
        cache_write_5m=write_5m,
        cache_write_1h=write_1h,
        output=_int(usage.get("output_tokens")),
        # thinking_tokens are part of output_tokens; kept for display only.
        thinking_output=thinking,
    )


def _tier(usage: dict) -> str:
    if usage.get("speed") == "fast":
        return "fast"
    if usage.get("service_tier") == "batch":
        return "batch"
    return "standard"


def _project_name(record: dict, path: Path) -> str:
    cwd = record.get("cwd")
    if isinstance(cwd, str) and cwd:
        return Path(cwd.replace("\\", "/")).name or cwd
    # Directory names encode the cwd with separators replaced by '-'.
    return path.parent.name.strip("-").split("-")[-1] or path.parent.name


def _int(value: object) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


register(ClaudeCodeSource())
