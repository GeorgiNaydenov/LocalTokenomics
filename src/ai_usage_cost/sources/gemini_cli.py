"""Gemini CLI (google-gemini/gemini-cli) session logs.

Layout: ``<home>/.gemini/tmp/<slug>/chats/session-*.jsonl`` (subagents:
``chats/<parentSessionId>/<sub>.jsonl``), ``<home>`` = ``GEMINI_CLI_HOME`` else the user home.
Since 2026-04-09 a session file is an append-only op log: a metadata line, message lines (a
``gemini`` message is appended again in full when tokens attach), ``{"$set": ...}`` partial
updates and ``{"$rewindTo": id}``. Older versions wrote one whole-file ``session-*.json``
(a ``ConversationRecord`` with a ``messages`` array and the same field names); those are read
too.

Policy: messages are deduped by ``id`` (last wins). A ``$rewindTo`` drops messages from the
conversation but their API calls were still billed, so every distinct billed message id ever
seen is counted, rewound or not. Limitation: ``projects.json`` / ``.project_root`` are read
at parse time only, so a project-name change alone does not invalidate the store cache.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from pathlib import Path

from ..models import TokenUsage, UsageEvent
from ..trace import Capabilities
from .base import Source, as_int, parse_timestamp, project_of, read_json_records, title_of

SOURCE_ID = "gemini-cli"


def default_roots() -> list[Path]:
    home_env = os.environ.get("GEMINI_CLI_HOME", "").strip()
    home = Path(home_env) if home_env else Path.home()
    # The second root is where Gemini CLI relocates its home under the macOS sandbox.
    return [home / ".gemini" / "tmp", home / ".cache" / ".gemini" / "tmp"]


def session_files(root: Path) -> list[Path]:
    """Only ``chats/session-*.json[l]`` and subagent ``chats/<parent>/**.jsonl`` under
    ``<tmp>/<slug>/``: ~/.gemini also holds unrelated (Antigravity) data that must yield
    nothing."""
    found: set[Path] = set()
    for base in (root, root / "tmp", root / ".gemini" / "tmp"):
        if not base.is_dir():
            continue
        for chats in base.glob("*/chats"):
            if not chats.is_dir():
                continue
            for pattern in ("session-*.jsonl", "session-*.json"):
                found.update(p for p in chats.glob(pattern) if p.is_file())
            for sub in chats.iterdir():
                if sub.is_dir():
                    found.update(p for p in sub.rglob("*.jsonl") if p.is_file())
    return sorted(found)


def _slug_dir(path: Path) -> Path | None:
    for parent in path.parents:
        if parent.name == "chats":
            return parent.parent
    return None


def _is_nested(path: Path) -> bool:
    """True for ``chats/<parentSessionId>/<sub>.jsonl`` (a subagent file)."""
    return path.parent.name != "chats"


def _project_root(path: Path, directories: object) -> str | None:
    slug_dir = _slug_dir(path)
    if slug_dir is not None:
        slug = slug_dir.name
        registry = slug_dir.parent.parent / "projects.json"
        try:
            projects = json.loads(registry.read_text(encoding="utf-8")).get("projects")
        except (OSError, ValueError, AttributeError):
            projects = None
        if isinstance(projects, dict):
            for root, name in projects.items():
                if name == slug and isinstance(root, str) and root:
                    return root
        try:
            marker = (slug_dir / ".project_root").read_text(encoding="utf-8").strip()
        except OSError:
            marker = ""
        if marker:
            return marker
    if isinstance(directories, list) and directories and isinstance(directories[0], str):
        return directories[0] or None
    return None


def _count(value: object) -> int:
    return max(0, as_int(value))


def _tokens_of(tokens: dict) -> TokenUsage | None:
    input_total = _count(tokens.get("input"))
    cached = min(_count(tokens.get("cached")), input_total)
    thoughts = _count(tokens.get("thoughts"))
    output = _count(tokens.get("output"))
    tool = _count(tokens.get("tool"))
    total = _count(tokens.get("total"))
    uncached = input_total - cached
    # `tool` (tool-use prompt tokens) is input-billed but not part of `input`; add it only
    # when the record's own total reconciles that way, otherwise it is ignored.
    if tool > 0 and total == input_total + output + thoughts + tool:
        uncached += tool
    usage = TokenUsage(
        uncached_input=uncached,
        cache_read=cached,
        output=output + thoughts,
        reasoning_output=thoughts,
    )
    return usage if usage.total > 0 else None


def _read_ops(path: Path, warnings: list[str]) -> Iterator[tuple[int, dict]]:
    if path.suffix == ".json":
        try:
            doc = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        except ValueError:
            warnings.append(f"{path.name}: skipped unparsable file")
            return
        if isinstance(doc, dict):
            yield 0, {"$set": {k: v for k, v in doc.items() if k != "messages"}}
            yield 0, {"$set": {"messages": doc.get("messages")}}
        return
    for offset, _length, record in read_json_records(path, warnings):
        yield offset, record


def _replay(path: Path, warnings: list[str]) -> tuple[dict, list[tuple[int, dict]]]:
    """Apply the op log: (metadata, billed messages deduped by id, last wins)."""
    meta: dict = {}
    messages: dict[str, tuple[int, dict]] = {}

    def take(offset: int, message: object) -> None:
        if not isinstance(message, dict):
            return
        message_id = message.get("id")
        if isinstance(message_id, str) and message_id:
            key = message_id
        else:
            # No id: a deterministic key so an identical re-emitted line still dedups.
            raw = message.get("tokens")
            shape = json.dumps(raw, sort_keys=True) if isinstance(raw, dict) else ""
            key = f"~{message.get('timestamp')}|{message.get('type')}|{shape}"
        messages[key] = (offset, message)

    first = True
    for offset, record in _read_ops(path, warnings):
        if "$rewindTo" in record:
            continue  # rewound turns were still billed: nothing to undo
        update = record.get("$set")
        if isinstance(update, dict):
            for key, value in update.items():
                if key == "messages":
                    for message in value if isinstance(value, list) else []:
                        take(offset, message)
                elif value is not None:
                    meta[key] = value
            continue
        if first and "sessionId" in record and "type" not in record:
            meta.update(record)
        else:
            take(offset, record)
        first = False
    return meta, list(messages.values())


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    meta, billed = _replay(path, warnings)
    session_id = meta.get("sessionId")
    if not isinstance(session_id, str) or not session_id:
        session_id = path.stem
    cwd = _project_root(path, meta.get("directories"))
    project = project_of(cwd)
    if project is None:
        slug_dir = _slug_dir(path)
        project = slug_dir.name if slug_dir is not None else None
    summary = meta.get("summary")
    title = summary if isinstance(summary, str) and summary.strip() else None
    sidechain = meta.get("kind") == "subagent" or _is_nested(path)

    for offset, message in billed:
        tokens_raw = message.get("tokens")
        if message.get("type") != "gemini" or not isinstance(tokens_raw, dict):
            continue
        tokens = _tokens_of(tokens_raw)
        if tokens is None:
            continue
        message_id = message.get("id")
        model = message.get("model")
        yield UsageEvent(
            source=SOURCE_ID,
            client=SOURCE_ID,
            provider="google",
            model=model if isinstance(model, str) and model else None,
            timestamp=parse_timestamp(message.get("timestamp"), path),
            session_id=session_id,
            request_id=f"{SOURCE_ID}:{session_id}:{message_id}" if message_id else None,
            tokens=tokens,
            is_sidechain=sidechain,
            project=project,
            working_directory=cwd,
            title=title if title else title_of(project, session_id),
            title_source="tool" if title else "folder",
            source_file=str(path),
            record_offset=offset,
        )


SOURCE = Source(
    id=SOURCE_ID,
    label="Gemini CLI",
    clients={SOURCE_ID: "Gemini CLI"},
    default_roots=default_roots,
    files=session_files,
    parse=parse,
    token_data="full",
    display_path="$GEMINI_CLI_HOME/.gemini/tmp/<slug>/chats/session-*.jsonl",
    capabilities=Capabilities(tokens="measured", cost="derived"),
    experimental=True,
)
