"""Generate synthetic Claude Code and Codex logs for developing the dashboard.

Not test data -- the numbers are plausible rather than exact. Use it to run the UI
without touching real logs:

    python scripts/demo_logs.py /tmp/demo
    ai-usage-cost serve --claude-dir /tmp/demo/claude --codex-dir /tmp/demo/codex
"""

from __future__ import annotations

import json
import random
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

CLAUDE_MODELS = [("claude-opus-5", 0.55), ("claude-sonnet-5", 0.35), ("claude-haiku-4-5", 0.10)]
CODEX_MODELS = [("gpt-5-codex", 0.6), ("gpt-5.6-terra", 0.3), ("gpt-5.6-luna", 0.1)]
PROJECTS = ["indotalent", "ai-usage-cost", "portfolio-site", "scratch"]


def pick(weighted: list[tuple[str, float]], rng: random.Random) -> str:
    roll = rng.random()
    cumulative = 0.0
    for name, weight in weighted:
        cumulative += weight
        if roll <= cumulative:
            return name
    return weighted[-1][0]


def write_claude(root: Path, day: datetime, rng: random.Random) -> None:
    project = pick([(p, 1 / len(PROJECTS)) for p in PROJECTS], rng)
    session = str(uuid.uuid4())
    folder = root / f"-home-user-{project}"
    folder.mkdir(parents=True, exist_ok=True)
    model = pick(CLAUDE_MODELS, rng)
    cache_read = 0
    lines = []
    for turn in range(rng.randint(6, 40)):
        stamp = day + timedelta(minutes=turn * rng.randint(1, 6))
        cache_write = rng.randint(2000, 60000) if turn == 0 or rng.random() < 0.15 else 0
        cache_read = cache_read + cache_write if turn else cache_write
        usage = {
            "input_tokens": rng.randint(1, 200),
            "cache_creation_input_tokens": cache_write,
            "cache_read_input_tokens": cache_read if turn else 0,
            "output_tokens": rng.randint(200, 3000),
            "output_tokens_details": {"thinking_tokens": rng.randint(0, 1200)},
            "cache_creation": {
                "ephemeral_1h_input_tokens": cache_write if rng.random() < 0.7 else 0,
                "ephemeral_5m_input_tokens": 0 if rng.random() < 0.7 else cache_write,
            },
            "service_tier": "standard",
            "speed": "standard",
        }
        lines.append(
            json.dumps(
                {
                    "type": "assistant",
                    "timestamp": stamp.isoformat().replace("+00:00", "Z"),
                    "sessionId": session,
                    "requestId": f"req_{uuid.uuid4().hex[:16]}",
                    "cwd": f"/home/user/{project}",
                    "isSidechain": rng.random() < 0.12,
                    "message": {"id": f"msg_{uuid.uuid4().hex[:20]}", "model": model, "usage": usage},
                }
            )
        )
    (folder / f"{session}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_codex(root: Path, day: datetime, rng: random.Random) -> None:
    project = pick([(p, 1 / len(PROJECTS)) for p in PROJECTS], rng)
    session = str(uuid.uuid4())
    folder = root / f"{day:%Y/%m/%d}"
    folder.mkdir(parents=True, exist_ok=True)
    model = pick(CODEX_MODELS, rng)
    lines = [
        json.dumps(
            {
                "timestamp": day.isoformat().replace("+00:00", "Z"),
                "type": "session_meta",
                "payload": {"id": session, "cwd": f"/home/user/{project}", "model": model},
            }
        )
    ]
    running = {
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "cache_write_input_tokens": 0,
        "output_tokens": 0,
        "reasoning_output_tokens": 0,
        "total_tokens": 0,
    }
    for turn in range(rng.randint(4, 25)):
        stamp = day + timedelta(minutes=turn * rng.randint(1, 8))
        total_input = rng.randint(8000, 90000)
        last = {
            "input_tokens": total_input,
            "cached_input_tokens": int(total_input * rng.uniform(0.5, 0.92)) if turn else 0,
            "cache_write_input_tokens": 0,
            "output_tokens": rng.randint(300, 4000),
            "reasoning_output_tokens": rng.randint(0, 1500),
            "total_tokens": 0,
        }
        last["total_tokens"] = last["input_tokens"] + last["output_tokens"]
        for field, value in last.items():
            running[field] += value
        lines.append(
            json.dumps(
                {
                    "timestamp": stamp.isoformat().replace("+00:00", "Z"),
                    "type": "event_msg",
                    "payload": {
                        "type": "token_count",
                        "info": {
                            "total_token_usage": dict(running),
                            "last_token_usage": last,
                            "model_context_window": 400000,
                        },
                    },
                }
            )
        )
    name = f"rollout-{day:%Y-%m-%dT%H-%M-%S}-{session}.jsonl"
    (folder / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(target: Path, days: int = 45, seed: int = 7) -> None:
    rng = random.Random(seed)
    claude_root = target / "claude"
    codex_root = target / "codex"
    end = datetime.now(tz=timezone.utc).replace(hour=9, minute=0, second=0, microsecond=0)
    for offset in range(days):
        day = end - timedelta(days=offset)
        if day.weekday() >= 5 and rng.random() < 0.7:
            continue
        for _ in range(rng.randint(1, 3)):
            write_claude(claude_root, day + timedelta(hours=rng.randint(0, 9)), rng)
        if rng.random() < 0.6:
            write_codex(codex_root, day + timedelta(hours=rng.randint(0, 9)), rng)
    print(f"demo logs written to {target}")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/demo"))
