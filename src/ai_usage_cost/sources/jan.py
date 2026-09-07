from __future__ import annotations

import json
import os
import platform
from collections.abc import Iterator
from pathlib import Path

from ..models import UsageEvent
from .base import Source, parse_timestamp, read_json_lines

_LOCAL_ENGINES = {"nitro", "llama.cpp", "cortex", "llamacpp"}


def default_roots() -> list[Path]:
    home = Path.home()
    roots = []
    app_data = os.environ.get("APPDATA")
    if app_data:
        roots.append(Path(app_data) / "Jan" / "data" / "threads")
    roots.append(home / "Library" / "Application Support" / "Jan" / "data" / "threads")
    roots.append(home / ".local" / "share" / "Jan" / "data" / "threads")
    roots.append(home / "jan" / "threads")
    return roots


def jan_files(root: Path) -> list[Path]:
    return sorted(p for p in root.glob("*/messages.jsonl") if p.is_file())


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    thread_id = path.parent.name
    model, engine = _thread_model(path.parent / "thread.json")
    provider = _provider(engine)
    for record in read_json_lines(path, warnings):
        if record.get("role") != "assistant":
            continue
        message_id = record.get("id")
        yield UsageEvent(
            source="jan",
            client="jan",
            provider=provider,
            model=model,
            timestamp=parse_timestamp(record.get("created"), path),
            session_id=thread_id,
            request_id=f"jan:{message_id}" if message_id else None,
            tokens=None,
            machine=platform.node(),
            source_file=str(path),
        )


def _thread_model(path: Path) -> tuple[str | None, str | None]:
    if not path.is_file():
        return None, None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, None
    assistants = data.get("assistants")
    if not isinstance(assistants, list) or not assistants:
        return None, None
    first = assistants[0]
    if not isinstance(first, dict):
        return None, None
    model_obj = first.get("model")
    if not isinstance(model_obj, dict):
        return None, None
    model_id = model_obj.get("id")
    engine = model_obj.get("engine")
    return (
        model_id if isinstance(model_id, str) else None,
        engine if isinstance(engine, str) else None,
    )


def _provider(engine: str | None) -> str | None:
    if engine is None:
        return None
    return "local" if engine.lower() in _LOCAL_ENGINES else engine


SOURCE = Source(
    id="jan",
    label="Jan",
    clients={"jan": "Jan"},
    default_roots=default_roots,
    files=jan_files,
    parse=parse,
)
