from __future__ import annotations

import json
import re
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

from .trace import Span, SpanContent

MAX_CONTENT_BYTES = 65_536
DEFAULT_CONFIG_PATH = Path.home() / ".ai-usage-cost" / "config.json"

SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "private_key",
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
            re.DOTALL,
        ),
    ),
    ("aws_access_key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    (
        "aws_secret_key",
        re.compile(
            r"(?i)aws[a-z0-9_.\-]{0,32}(?:secret|private)[a-z0-9_.\-]{0,32}[\"']?\s*[=:]\s*"
            r"[\"']?(?!\[REDACTED:)[A-Za-z0-9/+=]{40}",
        ),
    ),
    (
        "github_token",
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{22,})\b"),
    ),
    ("anthropic_key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{16,}")),
    ("openai_key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_\-]{16,}")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+")),
    ("bearer", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._\-+/=]{16,}")),
    (
        "assignment",
        re.compile(
            r"(?i)\b(?:[A-Za-z0-9]+[_.\-])*(?:key|token|secret|password|passwd)"
            r"(?:[_.\-][A-Za-z0-9]+)*[\"']?\s*[=:]\s*[\"']?(?!\[REDACTED:)[^\s\"',]{8,}",
        ),
    ),
]


class ContentUnavailable(Exception):
    pass


class Config(BaseModel):
    metadata_only: bool = True
    exclude_projects: list[str] = Field(default_factory=list)
    max_content_bytes: int = MAX_CONTENT_BYTES
    metadata_retention_days: int | None = None
    content_retention_days: int | None = None


def load_config(path: Path | None = None) -> Config:
    try:
        raw = json.loads((path or DEFAULT_CONFIG_PATH).read_text("utf-8"))
    except (OSError, ValueError):
        return Config()
    try:
        return Config.model_validate(raw)
    except ValidationError:
        return Config()


def truncate(text: str, max_bytes: int) -> tuple[str, bool]:
    raw = text.encode("utf-8")
    if len(raw) <= max_bytes:
        return text, False
    return raw[: max(max_bytes, 0)].decode("utf-8", "ignore"), True


def redact(text: str) -> tuple[str, int]:
    total = 0
    for name, pattern in SECRET_PATTERNS:
        text, count = pattern.subn(f"[REDACTED:{name}]", text)
        total += count
    return text, total


def read_content(span: Span, config: Config) -> SpanContent:
    if config.metadata_only or span.content_path is None:
        raise ContentUnavailable(span.span_id)
    try:
        with open(span.source_file, "rb") as handle:
            handle.seek(span.record_offset)
            record = json.loads(handle.read(span.record_length))
    except (OSError, ValueError) as exc:
        raise ContentUnavailable(span.span_id) from exc
    value = resolve_path(record, span.content_path)
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    text, truncated = truncate(text, config.max_content_bytes)
    text, redactions = redact(text)
    return SpanContent(
        span_id=span.span_id, content=text, truncated=truncated, redactions=redactions
    )


def resolve_path(record: object, content_path: str) -> object:
    current = record
    for segment in content_path.split("."):
        if segment.isdigit() and isinstance(current, list):
            index = int(segment)
            if index >= len(current):
                raise ContentUnavailable(content_path)
            current = current[index]
        elif isinstance(current, dict) and segment in current:
            current = current[segment]
        else:
            raise ContentUnavailable(content_path)
    return current
