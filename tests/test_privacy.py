from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from ai_usage_cost.privacy import (
    Config,
    ContentUnavailable,
    load_config,
    read_content,
    redact,
    truncate,
)
from ai_usage_cost.trace import Span

FAKE_PRIVATE_KEY = (
    "-----BEGIN RSA PRIVATE KEY-----\n"
    "MIIEowIBAAKCAQEAxfakefakefakefakefakefakefakefake\n"
    "ZmFrZWZha2VmYWtlZmFrZWZha2VmYWtlZmFrZWZha2U=\n"
    "-----END RSA PRIVATE KEY-----"
)
FAKE_AWS_ACCESS_KEY = "AKIAZZ4NOTAREALKEY99"
FAKE_AWS_SECRET_KEY = "wJalrFAKEfakeEXAMPLEKEY/K7MDENGbPxRfiCYz"
FAKE_GITHUB_TOKEN = "ghp_" + "F" * 36
FAKE_ANTHROPIC_KEY = "sk-ant-api03-" + "z" * 40
FAKE_OPENAI_KEY = "sk-proj-" + "q" * 40
FAKE_JWT = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmYWtlIn0.c2lnbmF0dXJlLWZha2U"
FAKE_BEARER_TOKEN = "ABCDEFabcdef0123456789"


@pytest.mark.parametrize(
    ("text", "secret", "name"),
    [
        (FAKE_PRIVATE_KEY, "MIIEowIBAAKCAQEA", "private_key"),
        (f"export AWS_ACCESS_KEY_ID={FAKE_AWS_ACCESS_KEY}", FAKE_AWS_ACCESS_KEY, "aws_access_key"),
        (
            f"aws_secret_access_key = {FAKE_AWS_SECRET_KEY}",
            FAKE_AWS_SECRET_KEY,
            "aws_secret_key",
        ),
        (f"git remote token {FAKE_GITHUB_TOKEN} used", FAKE_GITHUB_TOKEN, "github_token"),
        (f"the key is {FAKE_ANTHROPIC_KEY} ok", FAKE_ANTHROPIC_KEY, "anthropic_key"),
        (f"the key is {FAKE_OPENAI_KEY} ok", FAKE_OPENAI_KEY, "openai_key"),
        (f"cookie session {FAKE_JWT} end", FAKE_JWT, "jwt"),
        (
            f"Authorization: Bearer {FAKE_BEARER_TOKEN}",
            FAKE_BEARER_TOKEN,
            "bearer",
        ),
        ("DATABASE_PASSWORD=hunter2hunter2", "hunter2hunter2", "assignment"),
    ],
)
def test_each_pattern_replaces_its_secret(text: str, secret: str, name: str) -> None:
    cleaned, count = redact(text)

    assert secret not in cleaned
    assert f"[REDACTED:{name}]" in cleaned
    assert count >= 1


def test_specific_pattern_wins_over_generic_assignment() -> None:
    cleaned, count = redact(f"ANTHROPIC_API_KEY={FAKE_ANTHROPIC_KEY}")

    assert cleaned == "ANTHROPIC_API_KEY=[REDACTED:anthropic_key]"
    assert count == 1


def test_redaction_count_covers_every_occurrence() -> None:
    text = f"{FAKE_ANTHROPIC_KEY} and {FAKE_OPENAI_KEY} and {FAKE_GITHUB_TOKEN}"

    cleaned, count = redact(text)

    assert count == 3
    assert "sk-" not in cleaned


def test_plain_text_is_untouched() -> None:
    assert redact("the monkey ate a banana") == ("the monkey ate a banana", 0)


def test_truncate_keeps_short_text() -> None:
    assert truncate("hello", 64) == ("hello", False)


def test_truncate_counts_bytes_without_splitting_a_character() -> None:
    text = "aé" + "b" * 10

    cut, truncated = truncate(text, 2)

    assert truncated is True
    assert cut == "a"
    assert len(text.encode("utf-8")) == 13


def test_missing_config_file_gives_defaults(tmp_path: Path) -> None:
    config = load_config(tmp_path / "nope.json")

    assert config == Config()
    assert config.metadata_only is True
    assert config.max_content_bytes == 65_536


def test_malformed_config_file_gives_defaults(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    path.write_text("{not json at all", "utf-8")

    assert load_config(path) == Config()


def test_invalid_config_values_give_defaults(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"metadata_only": "banana"}), "utf-8")

    assert load_config(path) == Config()


def test_config_file_is_read(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"metadata_only": False, "exclude_projects": ["secret-app"]}))

    config = load_config(path)

    assert config.metadata_only is False
    assert config.exclude_projects == ["secret-app"]


def _span(path: Path, offset: int, length: int, content_path: str | None) -> Span:
    return Span(
        span_id="s1",
        source="claude-code",
        session_id="sess",
        seq=0,
        kind="tool_result",
        started_at=datetime(2026, 9, 1, 12, 0, tzinfo=UTC),
        source_file=str(path),
        record_offset=offset,
        record_length=length,
        content_path=content_path,
    )


def _jsonl(tmp_path: Path) -> tuple[Path, int, int]:
    first = json.dumps({"type": "user", "message": {"content": "ignored"}}) + "\n"
    record = json.dumps(
        {
            "type": "user",
            "toolUseResult": {"stdout": f"ANTHROPIC_API_KEY={FAKE_ANTHROPIC_KEY}\ndone"},
        }
    )
    path = tmp_path / "session.jsonl"
    path.write_bytes((first + record + "\n").encode("utf-8"))
    return path, len(first.encode("utf-8")), len(record.encode("utf-8"))


def test_read_content_is_unavailable_under_metadata_only(tmp_path: Path) -> None:
    path, offset, length = _jsonl(tmp_path)

    with pytest.raises(ContentUnavailable):
        read_content(_span(path, offset, length, "toolUseResult.stdout"), Config())


def test_read_content_is_unavailable_without_a_content_path(tmp_path: Path) -> None:
    path, offset, length = _jsonl(tmp_path)

    with pytest.raises(ContentUnavailable):
        read_content(_span(path, offset, length, None), Config(metadata_only=False))


def test_read_content_is_unavailable_for_an_unknown_path(tmp_path: Path) -> None:
    path, offset, length = _jsonl(tmp_path)

    with pytest.raises(ContentUnavailable):
        read_content(_span(path, offset, length, "message.nope"), Config(metadata_only=False))


def test_read_content_is_unavailable_for_a_missing_file(tmp_path: Path) -> None:
    span = _span(tmp_path / "gone.jsonl", 0, 10, "toolUseResult.stdout")

    with pytest.raises(ContentUnavailable):
        read_content(span, Config(metadata_only=False))


def test_read_content_reads_the_record_and_redacts_it(tmp_path: Path) -> None:
    path, offset, length = _jsonl(tmp_path)

    span = _span(path, offset, length, "toolUseResult.stdout")

    content = read_content(span, Config(metadata_only=False))

    assert content.span_id == "s1"
    assert content.content == "ANTHROPIC_API_KEY=[REDACTED:anthropic_key]\ndone"
    assert content.redactions == 1
    assert content.truncated is False


def test_read_content_truncates_before_redacting(tmp_path: Path) -> None:
    path, offset, length = _jsonl(tmp_path)
    config = Config(metadata_only=False, max_content_bytes=20)

    content = read_content(_span(path, offset, length, "toolUseResult.stdout"), config)

    assert content.truncated is True
    assert len(content.content.encode("utf-8")) <= 20


def test_read_content_serialises_a_non_string_value(tmp_path: Path) -> None:
    record = json.dumps({"message": {"content": [{"type": "text", "text": "hi"}]}})
    path = tmp_path / "session.jsonl"
    path.write_bytes((record + "\n").encode("utf-8"))
    span = _span(path, 0, len(record.encode("utf-8")), "message.content.0")

    content = read_content(span, Config(metadata_only=False))

    assert json.loads(content.content) == {"type": "text", "text": "hi"}
