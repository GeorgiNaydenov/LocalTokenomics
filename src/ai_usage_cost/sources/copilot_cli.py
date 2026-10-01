"""GitHub Copilot CLI sessions (``<COPILOT_HOME>/session-state/<id>/events.jsonl``).

EXPERIMENTAL: built from the SDK's generated event schema
(github/copilot-sdk ``nodejs/src/generated/session-events.ts``) and synthetic fixtures;
no real token-bearing session has been available to check it against.

Where tokens live. The per-request ``assistant.usage`` and ``session.usage_info`` events
are ephemeral and never reach ``events.jsonl``. The persisted carriers are:

* ``session.shutdown.data.modelMetrics.<model>.usage`` -- CUMULATIVE per session per model.
  A resumed session appends another shutdown holding the running total, so this parser
  emits the DELTA between consecutive shutdowns per model (the first is taken whole; a
  total smaller than the previous one is read as a counter reset and taken whole).
* ``session.compaction_complete.data.compactionTokensUsed`` -- one real LLM call each.
  NOT emitted by default (``_COUNT_COMPACTION``): the SDK schema never says whether the
  shutdown ``modelMetrics`` include that call, and counting it again would double count.
  Flip the constant once a real log proves the shutdown totals exclude it.

Only the top-level ``modelMetrics`` is read. ``agentMetrics.<agentId>.modelMetrics``
(per-agent breakdown, main conversation under ``main``) very likely re-slices the same
totals, and adding it would double count; subagent usage is therefore inside the
session's own numbers and no event is flagged ``is_sidechain``.

A session that crashed before writing a shutdown has no input/cache data (only
``assistant.message.outputTokens``); inventing output-only events would understate it, so
no event is emitted and a warning is raised instead.

Copilot logs credits (``totalNanoAiu``), not dollars: ``reported_cost`` stays ``None`` and
``raw["copilot_credits"]`` carries ``nanoAiu / 1e9`` (VS Code's unit).

Limitations: spans and per-model context windows are not provided (only
``compaction_complete.tokenLimit`` exists on disk). The store caches on ``events.jsonl``
only, so an edit to ``workspace.yaml`` alone (a rename) is not picked up until the log
next grows.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

from ..models import RawScalar, TokenUsage, UsageEvent
from ..trace import Capabilities
from .base import Source, as_int, parse_timestamp, project_of, read_json_lines, title_of

PROVIDER = "github-copilot"
_USAGE_KEYS = (
    "inputTokens",
    "outputTokens",
    "cacheReadTokens",
    "cacheWriteTokens",
    "reasoningTokens",
)
_NANO_PER_CREDIT = 1e9
# Unproven that shutdown modelMetrics exclude compaction calls (session-events.ts is silent),
# so by default they are not emitted separately; see the module docstring.
_COUNT_COMPACTION = False


def default_roots() -> list[Path]:
    home_env = os.environ.get("COPILOT_HOME", "").strip()
    root = Path(home_env) if home_env else Path.home() / ".copilot"
    return [root / "session-state"]


def session_files(root: Path) -> list[Path]:
    found = {p for p in root.glob("*/events.jsonl") if p.is_file()}
    direct = root / "events.jsonl"
    if direct.is_file():
        found.add(direct)
    return sorted(found)


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    workspace = _read_workspace(path.parent / "workspace.yaml")
    session_id = path.parent.name
    cwd: str | None = workspace.get("cwd")
    repository: str | None = workspace.get("repository")
    branch: str | None = workspace.get("branch")
    seen_start = False

    previous: dict[str, dict[str, int]] = {}
    pending_output = False  # assistant output logged since the last shutdown
    events: list[UsageEvent] = []

    def make(
        *,
        event_id: str,
        suffix: str,
        model: str | None,
        stamp: object,
        tokens: TokenUsage,
        nano: int,
        kind: str,
    ) -> UsageEvent:
        project = project_of(cwd)
        title, title_source = _title(workspace, project, session_id)
        raw: dict[str, RawScalar] = {"kind": kind}
        if nano:
            raw["copilot_credits"] = nano / _NANO_PER_CREDIT
        return UsageEvent(
            source="copilot-cli",
            client="copilot-cli",
            provider=PROVIDER,
            model=model,
            timestamp=parse_timestamp(stamp, path),
            session_id=session_id,
            request_id=f"copilot-cli:{session_id}:{event_id}:{suffix}",
            tokens=tokens,
            project=project,
            working_directory=cwd,
            repository=repository,
            branch=branch,
            title=title,
            title_source=title_source,
            source_file=str(path),
            raw=raw,
        )

    for record in read_json_lines(path, warnings):
        if record.get("ephemeral") is True:
            continue
        data = record.get("data")
        data = data if isinstance(data, dict) else {}
        kind = record.get("type")
        event_id = record.get("id")
        event_id = event_id if isinstance(event_id, str) and event_id else None

        if kind == "session.start" and not seen_start:
            seen_start = True
            sid = data.get("sessionId")
            if isinstance(sid, str) and sid:
                session_id = sid
            context = data.get("context")
            context = context if isinstance(context, dict) else {}
            cwd = _text(context.get("cwd")) or cwd
            repository = _text(context.get("repository")) or repository
            branch = _text(context.get("branch")) or branch
        elif kind == "assistant.message":
            if as_int(data.get("outputTokens")) > 0:
                pending_output = True
        elif kind == "session.shutdown":
            pending_output = False
            if event_id is None:
                continue
            metrics = data.get("modelMetrics")
            if not isinstance(metrics, dict):
                continue
            for model, metric in metrics.items():
                if not isinstance(metric, dict):
                    continue
                usage = metric.get("usage")
                if not isinstance(usage, dict):
                    continue
                total = {key: as_int(usage.get(key)) for key in _USAGE_KEYS}
                total["nano"] = as_int(metric.get("totalNanoAiu"))
                delta = _delta(previous.get(model), total)
                previous[model] = total
                tokens = _tokens(delta)
                if tokens.total == 0:
                    continue
                events.append(
                    make(
                        event_id=event_id,
                        suffix=model,
                        model=model,
                        stamp=record.get("timestamp"),
                        tokens=tokens,
                        nano=delta["nano"],
                        kind="shutdown",
                    )
                )
        elif _COUNT_COMPACTION and kind == "session.compaction_complete" and event_id is not None:
            used = data.get("compactionTokensUsed")
            if not isinstance(used, dict):
                continue
            tokens = _tokens({key: as_int(used.get(key)) for key in _USAGE_KEYS})
            if tokens.total == 0:
                continue
            model = _text(used.get("model"))
            usage = used.get("copilotUsage")
            nano = as_int(usage.get("totalNanoAiu")) if isinstance(usage, dict) else 0
            events.append(
                make(
                    event_id=event_id,
                    suffix="compaction",
                    model=model,
                    stamp=record.get("timestamp"),
                    tokens=tokens,
                    nano=nano,
                    kind="compaction",
                )
            )

    if pending_output:
        warnings.append(
            f"{path.parent.name}: session ended without a usage summary "
            "(no session.shutdown); its tokens are not counted"
        )
    yield from events


def _delta(previous: dict[str, int] | None, total: dict[str, int]) -> dict[str, int]:
    if previous is None or any(total[key] < previous[key] for key in total):
        return dict(total)
    return {key: total[key] - previous[key] for key in total}


def _tokens(values: dict[str, int]) -> TokenUsage:
    values = {key: max(0, value) for key, value in values.items()}
    input_total = values.get("inputTokens", 0)
    cache_read = values.get("cacheReadTokens", 0)
    cache_write = values.get("cacheWriteTokens", 0)
    # inputTokens already includes both cache buckets; clamp so odd data never goes negative.
    uncached = max(0, input_total - cache_read - cache_write)
    return TokenUsage(
        uncached_input=uncached,
        cache_read=cache_read,
        cache_write_5m=cache_write,
        output=values.get("outputTokens", 0),
        reasoning_output=values.get("reasoningTokens", 0),
    )


def _text(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _title(workspace: dict[str, str], project: str | None, session_id: str) -> tuple[str, str]:
    if workspace.get("name"):
        return workspace["name"], "tool"
    if workspace.get("summary"):
        return workspace["summary"], "summary"
    return title_of(project, session_id), "folder"


def _read_workspace(path: Path) -> dict[str, str]:
    """The few top-level scalar keys needed from ``workspace.yaml`` (no YAML dependency)."""
    wanted = {"cwd", "repository", "branch", "name", "summary"}
    found: dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return found
    for line in text.splitlines():
        if not line or line[0] in " \t#-":
            continue
        key, sep, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not sep or key not in wanted or not value or value[0] in "|>[{&*!":
            continue
        if value[0] in "\"'":
            closing = value.find(value[0], 1)
            value = value[1:closing] if closing > 0 else value[1:]
        elif " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        if value and value not in {"null", "~"}:
            found[key] = value
    return found


SOURCE = Source(
    id="copilot-cli",
    label="GitHub Copilot CLI",
    clients={"copilot-cli": "GitHub Copilot CLI"},
    default_roots=default_roots,
    files=session_files,
    parse=parse,
    token_data="session",
    display_path="$COPILOT_HOME/session-state/<session-id>/events.jsonl",
    capabilities=Capabilities(),
    experimental=True,
)
