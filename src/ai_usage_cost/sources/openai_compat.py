from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from ..models import TokenUsage, UsageEvent
from .base import Source, as_int, jsonl_files, parse_timestamp, read_json_lines


def default_roots() -> list[Path]:
    return []


def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
    for record in read_json_lines(path, warnings):
        response = record
        usage = response.get("usage")
        if not isinstance(usage, dict):
            nested = record.get("response")
            if isinstance(nested, dict):
                response = nested
                usage = response.get("usage")
        if not isinstance(usage, dict):
            continue

        prompt_tokens = as_int(usage.get("prompt_tokens"))
        completion_tokens = as_int(usage.get("completion_tokens"))
        if prompt_tokens == 0 and completion_tokens == 0:
            continue

        tokens = _tokens_from_usage(usage, prompt_tokens, completion_tokens)

        model = response.get("model")
        provider = record.get("provider")
        request_id = response.get("id")

        yield UsageEvent(
            source="openai-compat",
            client="openai-compat",
            provider=provider.lower() if isinstance(provider, str) else None,
            model=model if isinstance(model, str) else None,
            timestamp=parse_timestamp(response.get("created"), path),
            session_id=_session_id(record, path),
            request_id=request_id if isinstance(request_id, str) else None,
            tokens=tokens,
            source_file=str(path),
        )


def _tokens_from_usage(usage: dict, prompt_tokens: int, completion_tokens: int) -> TokenUsage:
    prompt_details = usage.get("prompt_tokens_details")
    cached = as_int(prompt_details.get("cached_tokens")) if isinstance(prompt_details, dict) else 0
    if prompt_tokens:
        cached = min(cached, prompt_tokens)

    completion_details = usage.get("completion_tokens_details")
    reasoning = (
        as_int(completion_details.get("reasoning_tokens"))
        if isinstance(completion_details, dict)
        else 0
    )

    return TokenUsage(
        uncached_input=max(0, prompt_tokens - cached),
        cache_read=cached,
        output=completion_tokens,
        reasoning_output=reasoning,
    )


def _session_id(record: dict, path: Path) -> str:
    for key in ("session_id", "conversation_id"):
        value = record.get(key)
        if isinstance(value, str) and value:
            return value
    return path.stem


SOURCE = Source(
    id="openai-compat",
    label="OpenAI-compatible",
    clients={"openai-compat": "OpenAI-compatible"},
    default_roots=default_roots,
    files=jsonl_files,
    parse=parse,
)
