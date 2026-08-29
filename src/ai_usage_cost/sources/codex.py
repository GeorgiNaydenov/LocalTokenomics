"""Codex CLI rollouts: ``~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl``.

Field names follow ``TokenUsage`` / ``TokenUsageInfo`` / ``TokenCountEvent`` in
``codex-rs/protocol/src/protocol.rs``; ``EventMsg`` is tagged
``#[serde(tag = "type", rename_all = "snake_case")]``, hence ``"type": "token_count"``.

Two normalisations matter:

* ``cached_input_tokens`` is a **subset** of ``input_tokens``, so the uncached input we
  bill is ``input_tokens - cached_input_tokens``. Anthropic reports these disjointly,
  OpenAI does not.
* ``reasoning_output_tokens`` is a subset of ``output_tokens`` -- display only.

The envelope has changed across Codex versions, so every lookup here is defensive: a
record is inspected both at the top level and inside ``payload``.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from ..models import TokenUsage, UsageEvent
from .base import JsonlSource, parse_timestamp, read_json_lines, register

RECONCILE_TOLERANCE = 0.01
RECONCILE_MIN_TOKENS = 1000


class CodexSource(JsonlSource):
    id = "codex"
    label = "Codex CLI"

    def default_roots(self) -> list[Path]:
        return [Path.home() / ".codex" / "sessions"]

    def iter_file(self, path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
        model = "unknown"
        session_id = _session_id_from_name(path)
        project: str | None = None
        summed = TokenUsage()
        final_total: dict | None = None

        for record in read_json_lines(path, warnings):
            payload = record.get("payload")
            payload = payload if isinstance(payload, dict) else record
            kind = payload.get("type") or record.get("type")

            found_model = _find_model(payload)
            if found_model:
                model = found_model
            found_session = _find_session_id(payload)
            if found_session:
                session_id = found_session
            found_cwd = _find_cwd_name(payload)
            if found_cwd:
                project = found_cwd

            if kind != "token_count":
                continue

            info = payload.get("info")
            info = info if isinstance(info, dict) else payload
            last = info.get("last_token_usage")
            total = info.get("total_token_usage")

            if isinstance(total, dict):
                final_total = total
            if not isinstance(last, dict):
                continue

            tokens = _tokens_from_usage(last)
            if tokens.total == 0:
                continue
            summed = summed + tokens

            yield UsageEvent(
                tool=self.id,
                timestamp=parse_timestamp(
                    record.get("timestamp") or payload.get("timestamp"), path
                ),
                model=model,
                session_id=session_id,
                project=project,
                tokens=tokens,
                source_file=str(path),
            )

        _reconcile(path, summed, final_total, warnings)


def _reconcile(
    path: Path, summed: TokenUsage, final_total: dict | None, warnings: list[str]
) -> None:
    """The per-turn deltas should add up to the session's own running total."""
    if final_total is None:
        return
    reported = _int(final_total.get("total_tokens"))
    if reported <= 0:
        return
    drift = abs(summed.total - reported)
    if drift > RECONCILE_MIN_TOKENS and drift / reported > RECONCILE_TOLERANCE:
        warnings.append(
            f"codex: {path.name}: summed turns {summed.total:,} vs session total "
            f"{reported:,} ({drift / reported:.1%} drift)"
        )


def _tokens_from_usage(usage: dict) -> TokenUsage:
    total_input = _int(usage.get("input_tokens"))
    cached = _int(usage.get("cached_input_tokens"))
    if total_input:
        cached = min(cached, total_input)
    return TokenUsage(
        uncached_input=max(0, total_input - cached),
        cache_read=cached,
        cache_write_5m=_int(usage.get("cache_write_input_tokens")),
        output=_int(usage.get("output_tokens")),
        reasoning_output=_int(usage.get("reasoning_output_tokens")),
    )


def _find_model(payload: dict) -> str:
    for candidate in (
        payload.get("model"),
        _nested(payload, "turn_context", "model"),
        _nested(payload, "info", "model"),
        _nested(payload, "model", "slug"),
    ):
        if isinstance(candidate, str) and candidate:
            return candidate
    return ""


def _find_session_id(payload: dict) -> str:
    for candidate in (payload.get("id"), payload.get("session_id"), payload.get("conversation_id")):
        if isinstance(candidate, str) and len(candidate) >= 8:
            return candidate
    return ""


def _find_cwd_name(payload: dict) -> str | None:
    for candidate in (payload.get("cwd"), _nested(payload, "turn_context", "cwd")):
        if isinstance(candidate, str) and candidate:
            return Path(candidate.replace("\\", "/")).name or candidate
    return None


def _nested(payload: dict, *keys: str) -> object:
    current: object = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _session_id_from_name(path: Path) -> str:
    # rollout-2026-08-29T10-11-12-<uuid>.jsonl
    stem = path.stem
    parts = stem.split("-")
    return "-".join(parts[-5:]) if len(parts) >= 5 else stem


def _int(value: object) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


register(CodexSource())
