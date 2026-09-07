from __future__ import annotations

import platform
import re
from collections.abc import Iterator
from pathlib import Path

from ..models import UsageEvent
from .base import Source, parse_timestamp, project_of, read_json_lines

MODEL_SWITCH_RE = re.compile(
    r"`Model Selection`\s+from\s+.+?\s+to\s+(.+?)\.(?=</USER_SETTINGS_CHANGE>|\s|$)"
)


def default_roots() -> list[Path]:
    return [Path.home() / ".gemini" / "antigravity" / "brain"]


def antigravity_files(root: Path) -> list[Path]:
    chosen: list[Path] = []
    for sub in root.iterdir():
        if not sub.is_dir():
            continue
        full = sub / ".system_generated" / "logs" / "transcript_full.jsonl"
        basic = sub / ".system_generated" / "logs" / "transcript.jsonl"
        if full.is_file():
            chosen.append(full)
        elif basic.is_file():
            chosen.append(basic)
    return sorted(chosen)


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    session_id = path.parent.parent.parent.name
    model: str | None = None
    cwd: str | None = None
    for record in read_json_lines(path, warnings):
        content = record.get("content")
        if record.get("type") == "USER_INPUT" and isinstance(content, str):
            match = MODEL_SWITCH_RE.search(content)
            if match:
                model = match.group(1).strip()
        if record.get("type") != "PLANNER_RESPONSE":
            continue
        cwd = _cwd_from_tool_calls(record.get("tool_calls")) or cwd
        yield UsageEvent(
            source="antigravity",
            client="antigravity",
            provider="google",
            model=model,
            timestamp=parse_timestamp(record.get("created_at"), path),
            session_id=session_id,
            request_id=f"antigravity:{session_id}:{record.get('step_index')}",
            tokens=None,
            working_directory=cwd,
            project=project_of(cwd),
            machine=platform.node(),
            source_file=str(path),
        )


def _cwd_from_tool_calls(tool_calls: object) -> str | None:
    if not isinstance(tool_calls, list):
        return None
    for call in tool_calls:
        if not isinstance(call, dict):
            continue
        args = call.get("args")
        if isinstance(args, dict) and isinstance(args.get("Cwd"), str):
            return args["Cwd"]
    return None


SOURCE = Source(
    id="antigravity",
    label="Antigravity",
    clients={"antigravity": "Antigravity"},
    default_roots=default_roots,
    files=antigravity_files,
    parse=parse,
)
