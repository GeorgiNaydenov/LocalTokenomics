from __future__ import annotations

import json
import random
import sqlite3
import uuid
from contextlib import closing
from datetime import UTC, datetime, timedelta
from pathlib import Path

from .pipeline import DEFAULT_DB_PATH
from .sources import registry

DEMO_DIR = DEFAULT_DB_PATH.parent / "demo"
DEMO_DB_PATH = DEMO_DIR / "usage.db"

CLAUDE_MODELS = [("claude-opus-5", 0.55), ("claude-sonnet-5", 0.35), ("claude-haiku-4-5", 0.10)]
CODEX_MODELS = [("gpt-5-codex", 0.6), ("gpt-5.6-terra", 0.3), ("gpt-5.6-luna", 0.1)]
JAN_MODELS = [
    ("llama3.1-8b-instruct", 0.5),
    ("qwen2.5-7b-instruct", 0.3),
    ("mistral-7b-instruct", 0.2),
]
JAN_ENGINES = [("llama.cpp", 0.6), ("nitro", 0.4)]
PROJECTS = ["indotalent", "ai-usage-cost", "portfolio-site", "scratch"]

DYAD_APPS_SCHEMA = """
CREATE TABLE apps (
    id INTEGER PRIMARY KEY,
    name TEXT,
    path TEXT,
    created_at INTEGER,
    updated_at INTEGER,
    github_org TEXT,
    github_repo TEXT,
    chat_context TEXT,
    github_branch TEXT,
    vercel_project_id TEXT,
    vercel_project_name TEXT,
    vercel_team_id TEXT,
    vercel_deployment_url TEXT,
    neon_project_id TEXT,
    neon_development_branch_id TEXT,
    neon_preview_branch_id TEXT
);

CREATE TABLE chats (
    id INTEGER PRIMARY KEY,
    app_id INTEGER,
    title TEXT,
    created_at INTEGER,
    initial_commit_hash TEXT
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    chat_id INTEGER,
    role TEXT,
    content TEXT,
    created_at INTEGER,
    approval_state TEXT,
    commit_hash TEXT
);
"""


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
                    "message": {
                        "id": f"msg_{uuid.uuid4().hex[:20]}",
                        "model": model,
                        "usage": usage,
                    },
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


def write_jan(root: Path, rng: random.Random, days: int) -> None:
    root.mkdir(parents=True, exist_ok=True)
    end = datetime.now(tz=UTC).replace(hour=9, minute=0, second=0, microsecond=0)
    for offset in range(days):
        day = end - timedelta(days=offset)
        if day.weekday() >= 5 and rng.random() < 0.7:
            continue
        if rng.random() < 0.75:
            continue
        project = pick([(p, 1 / len(PROJECTS)) for p in PROJECTS], rng)
        engine = pick(JAN_ENGINES, rng)
        model = pick(JAN_MODELS, rng)
        thread_id = f"thread-{uuid.uuid4().hex[:12]}"
        thread_dir = root / thread_id
        thread_dir.mkdir(parents=True, exist_ok=True)
        start = day + timedelta(hours=rng.randint(0, 9))
        thread = {
            "id": thread_id,
            "created": int(start.timestamp() * 1000),
            "updated": int(start.timestamp() * 1000),
            "title": f"{project} chat",
            "assistants": [
                {
                    "assistant_id": "jan-assistant",
                    "assistant_name": "Jan",
                    "model": {"id": model, "engine": engine, "parameters": {}, "settings": {}},
                }
            ],
            "object": "thread",
        }
        lines = []
        stamp = start
        for turn in range(rng.randint(2, 10)):
            stamp = stamp + timedelta(minutes=rng.randint(1, 6))
            role = "user" if turn % 2 == 0 else "assistant"
            lines.append(
                json.dumps(
                    {
                        "id": f"msg-{uuid.uuid4().hex[:12]}",
                        "object": "thread.message",
                        "role": role,
                        "status": "ready",
                        "thread_id": thread_id,
                        "created": int(stamp.timestamp() * 1000),
                        "updated": int(stamp.timestamp() * 1000),
                    }
                )
            )
        thread["updated"] = int(stamp.timestamp() * 1000)
        (thread_dir / "thread.json").write_text(json.dumps(thread), encoding="utf-8")
        (thread_dir / "messages.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_dyad(root: Path, rng: random.Random, days: int) -> None:
    root.mkdir(parents=True, exist_ok=True)
    db_path = root / "sqlite.db"
    db_path.unlink(missing_ok=True)
    end = datetime.now(tz=UTC).replace(hour=9, minute=0, second=0, microsecond=0)
    with closing(sqlite3.connect(db_path)) as conn:
        conn.executescript(DYAD_APPS_SCHEMA)
        message_id = 1
        for app_id, project in enumerate(PROJECTS, start=1):
            has_github = app_id % 2 == 1
            org, repo, branch = (
                ("acme", f"{project}-app", "main") if has_github else (None, None, None)
            )
            created_at = int((end - timedelta(days=days)).timestamp())
            conn.execute(
                "INSERT INTO apps VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    app_id,
                    project,
                    f"/home/user/{project}",
                    created_at,
                    created_at,
                    org,
                    repo,
                    None,
                    branch,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ),
            )
            chat_id = app_id
            conn.execute(
                "INSERT INTO chats VALUES (?,?,?,?,?)",
                (chat_id, app_id, f"{project} chat", created_at, None),
            )
            for offset in range(days):
                day = end - timedelta(days=offset)
                if day.weekday() >= 5 and rng.random() < 0.7:
                    continue
                if rng.random() < 0.7:
                    continue
                for _ in range(rng.randint(1, 3)):
                    stamp = day + timedelta(hours=rng.randint(0, 9), minutes=rng.randint(0, 59))
                    conn.execute(
                        "INSERT INTO messages VALUES (?,?,?,?,?,?,?)",
                        (
                            message_id,
                            chat_id,
                            "assistant",
                            "done",
                            int(stamp.timestamp()),
                            None,
                            None,
                        ),
                    )
                    message_id += 1
        conn.commit()


def demo_roots(target: Path) -> dict[str, Path]:
    known = {
        "claude-code": target / "claude",
        "codex": target / "codex",
        "jan": target / "jan",
        "dyad": target / "dyad" / "sqlite.db",
    }
    return {source_id: known.get(source_id, target / source_id) for source_id in registry()}


def generate(target: Path, days: int = 45, seed: int = 7) -> None:
    rng = random.Random(seed)
    claude_root = target / "claude"
    codex_root = target / "codex"
    jan_root = target / "jan"
    dyad_root = target / "dyad"
    end = datetime.now(tz=UTC).replace(hour=9, minute=0, second=0, microsecond=0)
    for offset in range(days):
        day = end - timedelta(days=offset)
        if day.weekday() >= 5 and rng.random() < 0.7:
            continue
        for _ in range(rng.randint(1, 3)):
            write_claude(claude_root, day + timedelta(hours=rng.randint(0, 9)), rng)
        if rng.random() < 0.6:
            write_codex(codex_root, day + timedelta(hours=rng.randint(0, 9)), rng)
    write_jan(jan_root, rng, days)
    write_dyad(dyad_root, rng, days)
