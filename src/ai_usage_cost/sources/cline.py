"""Cline family: Cline, Roo Code and Kilo Code (legacy v5), plus Cline's SDK session store.

Cline, Roo Code and Kilo v5 share one lineage: ``<globalStorage>/<ext-id>/tasks/<taskId>/``
with a ``ui_messages.json`` that is a JSON *array* rewritten whole (not JSONL). Usage lives in
the ``text`` field of ``say == "api_req_started"`` items, which is itself a JSON *string*
``{request, tokensIn, tokensOut, cacheWrites, cacheReads, cost, cancelReason}`` updated in
place. ``request`` is prompt text: it is dropped the moment the string is parsed and never
stored, logged or put in a warning.

This module holds the shared parser and the Cline ``SOURCE``; ``roo_code.py`` and
``kilo_legacy.py`` are thin siblings (the registry auto-discovers one ``SOURCE`` per module)
that call ``make_source`` with their own id, extension id and token policy. Kilo v7
(``kilo.db``) is an OpenCode fork handled by the OpenCode parser, not here.

Counted records (mirrors ``getApiMetrics.ts`` in cline/cline, confirmed on ``main``):
``api_req_started``, ``deleted_api_reqs`` and ``subagent_usage`` items, each carrying its
usage in the JSON string ``text``. Per the brief an ``api_req_started`` is only an event when
it has ``cost`` or ``cancelReason`` (the placeholder written before the response finishes has
neither) and is not ``partial``; the other two kinds are aggregated snapshots and count when
they carry any usage. ``subagent_usage`` is flagged ``is_sidechain``.

Token semantics (UNVERIFIED on a real log -- verify before trusting the totals)
-------------------------------------------------------------------------------
``tokensIn`` may or may not already include the cache buckets. ``_TOKENS_IN_INCLUSIVE``
records the policy per source:

* Roo Code: inclusive (``totalInputTokens`` = input + cacheWrites + cacheReads in Task.ts).
* Cline SDK ``metrics.inputTokens``: inclusive (usage.ts says so).
* Kilo v5: a Roo-derived fork, assumed inclusive. [unverified]
* Cline legacy: provider-dependent upstream; treated as EXCLUSIVE (Anthropic-style, where
  ``input_tokens`` excludes cache). [unverified] If a real log shows cacheReads > tokensIn
  routinely, flip the flag in ``cline.py``.

Inclusive: ``uncached = max(0, tokensIn - cacheReads - cacheWrites)``. Exclusive:
``uncached = tokensIn``. Either way ``cache_write_5m = cacheWrites``, ``cache_read =
cacheReads`` and ``output = tokensOut``. ``reported_cost`` is the tool's own USD ``cost``.

Model: Cline writes ``modelInfo.{modelId, providerId}`` on the api_req item, else the nearest
earlier (then first) ``task_metadata.json`` ``model_usage[]`` entry. Roo logs NO model id, so
``model=None`` (the event is unpriced, never guessed); its dollar figure is still reported.

SDK store (Cline >= 4.1 / Cline CLI): ``<sessions>/<id>/<id>.messages.json`` with assistant
messages carrying ``metrics`` and ``modelInfo``, plus a manifest ``<id>.json``. Dedup key is
session id + message index. Known limits, documented rather than solved:

* SDK versions before 0.0.74 re-counted the cached conversation on every request (about 5x
  inflated totals); no SDK version is recorded in the manifest, so such sessions cannot be
  told apart here.
* Legacy tasks migrated into SDK sessions can be double counted; only a manifest that says
  ``isLegacy`` (top level or in ``metadata``) is skipped.
* Directory names on this Windows machine are lowercased; extension ids are matched
  case-insensitively.
"""

from __future__ import annotations

import json
import os
import sys
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path

from ..models import TokenUsage, UsageEvent
from ..trace import Capabilities
from .base import Source, as_int, parse_timestamp, project_of, title_of

_VARIANTS = ["Code", "Code - Insiders", "Code - OSS", "VSCodium", "Cursor", "Windsurf"]
_USAGE_SAYS = ("api_req_started", "deleted_api_reqs", "subagent_usage")


# Whether `tokensIn` already includes cacheReads + cacheWrites, per source id. See the module
# docstring: every entry is unverified on a real log; edit here if one turns out wrong.
_TOKENS_IN_INCLUSIVE: dict[str, bool] = {
    "cline": False,
    "roo-code": True,
    "kilo-code-legacy": True,
}


@dataclass(frozen=True)
class Spec:
    source_id: str
    client: str
    ext_id: str
    tokens_in_inclusive: bool
    sdk: bool = False


CLINE_SPEC = Spec(
    "cline", "Cline", "saoudrizwan.claude-dev", _TOKENS_IN_INCLUSIVE["cline"], sdk=True
)


def vscode_bases() -> list[Path]:
    if sys.platform == "win32":
        app_data = os.environ.get("APPDATA")
        base = Path(app_data) if app_data else None
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path.home() / ".config"
    if base is None:
        return []
    return [base / variant / "User" / "globalStorage" for variant in _VARIANTS]


def task_roots(ext_id: str) -> list[Path]:
    """`tasks/` dirs for one extension id, matching the id case-insensitively."""
    found: list[Path] = []
    for storage in vscode_bases():
        try:
            children = list(storage.iterdir()) if storage.is_dir() else []
        except OSError:
            continue
        found.extend(c / "tasks" for c in children if c.name.lower() == ext_id.lower())
    if not found:
        bases = vscode_bases()
        return [bases[0] / ext_id / "tasks"] if bases else []
    return found


def sdk_sessions_root() -> Path:
    session_env = os.environ.get("CLINE_SESSION_DATA_DIR", "").strip()
    if session_env:
        return Path(session_env)
    data_env = os.environ.get("CLINE_DATA_DIR", "").strip()
    if data_env:
        return Path(data_env) / "sessions"
    dir_env = os.environ.get("CLINE_DIR", "").strip()
    base = Path(dir_env) if dir_env else Path.home() / ".cline"
    return base / "data" / "sessions"


def cline_roots() -> list[Path]:
    return [*task_roots(CLINE_SPEC.ext_id), sdk_sessions_root()]


def data_files(root: Path) -> list[Path]:
    """`ui_messages.json` task files and SDK `*.messages.json` session files under a root."""
    patterns = (
        "ui_messages.json",
        "*/ui_messages.json",
        "*/tasks/*/ui_messages.json",
        "*.messages.json",
        "*/*.messages.json",
    )
    found = {p for pattern in patterns for p in root.glob(pattern) if p.is_file()}
    return sorted(found)


def parse(path: Path, warnings: list[str], spec: Spec = CLINE_SPEC) -> Iterator[UsageEvent]:
    if path.name == "ui_messages.json":
        yield from _parse_task(path, warnings, spec)
    elif path.name.endswith(".messages.json") and spec.sdk:
        yield from _parse_sdk(path, warnings, spec)


# --- legacy task dirs -------------------------------------------------------------------


def _load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return None


def _salvage_array(text: str) -> list:
    """Complete leading elements of a JSON array cut off mid-write."""
    decoder = json.JSONDecoder()
    items: list = []
    idx = text.find("[") + 1
    while idx > 0:
        while idx < len(text) and text[idx] in " \t\r\n,":
            idx += 1
        if idx >= len(text) or text[idx] == "]":
            break
        try:
            item, idx = decoder.raw_decode(text, idx)
        except ValueError:
            break
        items.append(item)
    return items


def _read_array(path: Path, warnings: list[str]) -> list:
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        data = json.loads(text)
    except ValueError:
        data = _salvage_array(text)
        warnings.append(f"{path.parent.name}/{path.name}: truncated or invalid JSON, salvaged")
    if not isinstance(data, list):
        warnings.append(f"{path.parent.name}/{path.name}: expected a JSON array")
        return []
    return data


def _usage_dict(item: dict, counters: dict[str, int]) -> dict:
    """Parse `text` (a JSON string) and keep only numeric/enum usage keys: never `request`."""
    text = item.get("text")
    if not isinstance(text, str) or not text:
        return {}
    try:
        parsed = json.loads(text)
    except ValueError:
        counters["bad"] += 1
        return {}
    if not isinstance(parsed, dict):
        return {}
    keep = ("tokensIn", "tokensOut", "cacheWrites", "cacheReads", "cost", "cancelReason")
    return {key: parsed[key] for key in keep if key in parsed}


def _number(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return float(value)


def _tokens(
    tokens_in: int, tokens_out: int, writes: int, reads: int, *, inclusive: bool
) -> TokenUsage:
    # base.as_int passes negatives through; clamp every field so none can go below zero.
    tokens_in, tokens_out = max(0, tokens_in), max(0, tokens_out)
    writes, reads = max(0, writes), max(0, reads)
    uncached = max(0, tokens_in - reads - writes) if inclusive else tokens_in
    return TokenUsage(
        uncached_input=uncached,
        cache_read=reads,
        cache_write_5m=writes,
        output=tokens_out,
    )


def _history(task_dir: Path) -> dict:
    data = _load_json(task_dir / "history_item.json")
    return data if isinstance(data, dict) else {}


def _model_usage(task_dir: Path) -> list[tuple[float, str, str | None]]:
    data = _load_json(task_dir / "task_metadata.json")
    rows = data.get("model_usage") if isinstance(data, dict) else None
    out: list[tuple[float, str, str | None]] = []
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, dict):
            continue
        model = row.get("model_id")
        if not isinstance(model, str) or not model:
            continue
        provider = row.get("model_provider_id")
        ts = _number(row.get("ts")) or 0.0
        out.append((ts, model, provider if isinstance(provider, str) and provider else None))
    return sorted(out, key=lambda r: r[0])


def _nearest_model(
    usage: list[tuple[float, str, str | None]], ts: float
) -> tuple[str | None, str | None]:
    """Latest `model_usage` entry at or before `ts`, else the first one recorded."""
    if not usage:
        return None, None
    chosen = usage[0]
    for row in usage:
        if row[0] <= ts:
            chosen = row
    return chosen[1], chosen[2]


def _text(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _parse_task(path: Path, warnings: list[str], spec: Spec) -> Iterator[UsageEvent]:
    task_dir = path.parent
    task_id = task_dir.name
    history = _history(task_dir)
    cwd = _text(history.get("workspace")) or _text(history.get("cwdOnTaskInitialization"))
    project = project_of(cwd)
    parent = _text(history.get("parentTaskId"))
    root_task = _text(history.get("rootTaskId"))
    child = bool(parent) or (root_task is not None and root_task != task_id)
    metadata_models = _model_usage(task_dir)
    counters = {"bad": 0}
    seen: set[tuple[str, object]] = set()

    for item in _read_array(path, warnings):
        if not isinstance(item, dict) or item.get("type") != "say":
            continue
        say = item.get("say")
        if say not in _USAGE_SAYS or item.get("partial") is True:
            continue
        usage = _usage_dict(item, counters)
        if not usage:
            continue
        cost = _number(usage.get("cost"))
        if say == "api_req_started" and cost is None and "cancelReason" not in usage:
            continue
        tokens = _tokens(
            as_int(usage.get("tokensIn")),
            as_int(usage.get("tokensOut")),
            as_int(usage.get("cacheWrites")),
            as_int(usage.get("cacheReads")),
            inclusive=spec.tokens_in_inclusive,
        )
        if tokens.total == 0 and not cost:
            continue
        ts = item.get("ts")
        key = (str(say), ts)
        if key in seen:
            continue
        seen.add(key)

        info = item.get("modelInfo")
        info = info if isinstance(info, dict) else {}
        model = _text(info.get("modelId"))
        provider = _text(info.get("providerId")) or _text(history.get("apiProvider"))
        if model is None:
            model, meta_provider = _nearest_model(metadata_models, _number(ts) or 0.0)
            provider = provider or meta_provider
        suffix = "" if say == "api_req_started" else f":{say}"
        yield UsageEvent(
            source=spec.source_id,
            client=spec.source_id,
            provider=provider,
            model=model,
            timestamp=parse_timestamp(ts, path),
            session_id=task_id,
            request_id=f"{spec.source_id}:{task_id}:{ts}{suffix}",
            tokens=tokens,
            is_sidechain=child or say == "subagent_usage",
            project=project,
            working_directory=cwd,
            title=title_of(project, task_id),
            title_source="folder",
            source_file=str(path),
            reported_cost=cost,
        )
    if counters["bad"]:
        warnings.append(
            f"{task_id}/{path.name}: skipped {counters['bad']} unparsable usage entries"
        )


# --- Cline SDK store --------------------------------------------------------------------


def _parse_sdk(path: Path, warnings: list[str], spec: Spec) -> Iterator[UsageEvent]:
    data = _load_json(path)
    if not isinstance(data, dict):
        warnings.append(f"{path.name}: unreadable or truncated SDK messages file")
        return
    manifest = _load_json(path.with_name(path.name.removesuffix(".messages.json") + ".json"))
    manifest = manifest if isinstance(manifest, dict) else {}
    meta = manifest.get("metadata")
    meta = meta if isinstance(meta, dict) else {}
    if manifest.get("isLegacy") or meta.get("isLegacy"):
        return  # migrated legacy task: the task dir is the source of truth
    session_id = (
        _text(data.get("sessionId"))
        or _text(manifest.get("session_id"))
        or path.name.removesuffix(".messages.json")
    )
    cwd = _text(manifest.get("cwd")) or _text(manifest.get("workspace_root"))
    project = project_of(cwd)
    child = (data.get("agent") not in (None, "lead")) or bool(manifest.get("parent_session_id"))
    messages = data.get("messages")
    for index, message in enumerate(messages if isinstance(messages, list) else []):
        if not isinstance(message, dict) or message.get("role") != "assistant":
            continue
        metrics = message.get("metrics")
        if not isinstance(metrics, dict):
            continue
        tokens = _tokens(
            as_int(metrics.get("inputTokens")),
            as_int(metrics.get("outputTokens")),
            as_int(metrics.get("cacheWriteTokens")),
            as_int(metrics.get("cacheReadTokens")),
            inclusive=True,
        )
        cost = _number(metrics.get("cost"))
        if tokens.total == 0 and not cost:
            continue
        info = message.get("modelInfo")
        info = info if isinstance(info, dict) else {}
        yield UsageEvent(
            source=spec.source_id,
            client=spec.source_id,
            provider=_text(info.get("provider")) or _text(manifest.get("provider")),
            model=_text(info.get("id")) or _text(manifest.get("model")),
            timestamp=parse_timestamp(message.get("ts") or data.get("updated_at"), path),
            session_id=session_id,
            request_id=f"{spec.source_id}:sdk:{session_id}:{index}",
            tokens=tokens,
            is_sidechain=child,
            project=project,
            working_directory=cwd,
            title=title_of(project, session_id),
            title_source="folder",
            source_file=str(path),
            reported_cost=cost,
        )


# --- Source construction ----------------------------------------------------------------


def make_source(
    spec: Spec,
    *,
    label: str,
    default_roots: Callable[[], list[Path]],
    display_path: str,
) -> Source:
    def _parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
        return parse(path, warnings, spec)

    return Source(
        id=spec.source_id,
        label=label,
        clients={spec.source_id: spec.client},
        default_roots=default_roots,
        files=data_files,
        parse=_parse,
        token_data="full",
        display_path=display_path,
        capabilities=Capabilities(),
        experimental=True,
    )


SOURCE = make_source(
    CLINE_SPEC,
    label="Cline",
    default_roots=cline_roots,
    display_path=(
        "<VS Code user data>/User/globalStorage/saoudrizwan.claude-dev/tasks/<id>/"
        "ui_messages.json; "
        "$CLINE_DATA_DIR or ~/.cline/data/sessions/<id>/<id>.messages.json"
    ),
)
