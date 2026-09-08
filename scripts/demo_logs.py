"""Generate synthetic Claude Code and Codex logs for developing the dashboard.

Not test data -- the numbers are plausible rather than exact. Use it to run the UI
without touching real logs:

    python scripts/demo_logs.py /tmp/demo
    ai-usage-cost serve --root claude-code=/tmp/demo/claude --root codex=/tmp/demo/codex \
      --root jan=/tmp/demo/jan --root dyad=/tmp/demo/dyad/sqlite.db --db /tmp/demo/usage.db
"""

from __future__ import annotations

import json
import random
import sqlite3
import sys
import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path

CLAUDE_MODELS = [("claude-opus-5", 0.55), ("claude-sonnet-5", 0.35), ("claude-haiku-4-5", 0.10)]
CODEX_MODELS = [("gpt-5-codex", 0.6), ("gpt-5.6-terra", 0.3), ("gpt-5.6-luna", 0.1)]
JAN_MODELS = [
    ("llama3.1-8b-instruct", 0.5),
    ("qwen2.5-7b-instruct", 0.3),
    ("mistral-7b-instruct", 0.2),
]
JAN_ENGINES = [("llama.cpp", 0.6), ("nitro", 0.4)]
PROJECTS = ["checkout-api", "ai-usage-cost", "portfolio-site", "scratch"]

MODULES = ["src/service.py", "src/api.py", "src/models.py", "tests/test_service.py", "README.md"]
CLAUDE_PROMPTS = [
    "Add a health check endpoint",
    "Fix the failing regression test",
    "Rename the config loader and update its callers",
    "Document the deploy steps in the readme",
    "Speed up the nightly export job",
]
CLAUDE_THINKING = [
    "The service has no health route yet, so the router needs a new entry.",
    "The failing assertion looks like a stale fixture rather than a real regression.",
    "Renaming touches three call sites; do the loader first, then the imports.",
]
CLAUDE_REPLIES = [
    "Added /healthz with a readiness probe and a test for it.",
    "The fixture was stale. Updated it and the suite is green again.",
    "Renamed the loader and updated the three call sites.",
]
CLAUDE_AGENT_TASKS = [
    "Research readiness probe patterns",
    "Find every caller of the config loader",
    "Summarise the nightly job timings",
]
CLAUDE_API_ERRORS = [
    ("500 status code (no body)", 500),
    ("429 rate limit exceeded", 429),
    ("overloaded_error: server is overloaded", 529),
]
CODEX_PROMPTS = [
    "add a regression test for the parser",
    "why is the nightly export slow?",
    "rename the config loader and fix the imports",
    "write the deploy notes",
]
CODEX_REASONING = [
    "read the test file first, then patch the parser",
    "check the export query plan before touching the loop",
    "list the callers before renaming anything",
]
CODEX_REPLIES = [
    "the regression test passes now",
    "the export loop ran one query per row; batched it",
    "renamed the loader and updated four imports",
]
CODEX_COMMANDS = [
    (["pytest", "-q"], "14 passed in 2.31s"),
    (["ruff", "check", "src"], "All checks passed!"),
    (["git", "status", "--short"], " M src/service.py"),
    (["npm", "run", "build"], "built in 4.10s"),
]
CODEX_ERRORS = [
    "stream disconnected before completion",
    "request timed out after 60s",
]

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


def iso(stamp: datetime) -> str:
    return stamp.isoformat().replace("+00:00", "Z")


def epoch_ms(stamp: datetime) -> int:
    return int(stamp.timestamp() * 1000)


def claude_record(
    lines: list[str],
    session: str,
    cwd: str,
    stamp: datetime,
    parent: str | None,
    body: dict,
    *,
    agent_id: str | None = None,
) -> str:
    ident = str(uuid.uuid4())
    record: dict = {
        "parentUuid": parent,
        "isSidechain": agent_id is not None,
        "uuid": ident,
        "timestamp": iso(stamp),
        "sessionId": session,
        "cwd": cwd,
    }
    if agent_id is not None:
        record["agentId"] = agent_id
    record.update(body)
    lines.append(json.dumps(record))
    return ident


def claude_usage(
    index: int, cache_read: int, ceiling: int, rng: random.Random
) -> tuple[dict, int]:
    cache_write = rng.randint(2000, 60000) if index == 0 or rng.random() < 0.15 else 0
    cache_read = min(cache_read + cache_write, ceiling) if index else cache_write
    usage = {
        "input_tokens": rng.randint(1, 200),
        "cache_creation_input_tokens": cache_write,
        "cache_read_input_tokens": cache_read if index else 0,
        "output_tokens": rng.randint(200, 3000),
        "output_tokens_details": {"thinking_tokens": rng.randint(0, 1200)},
        "cache_creation": {
            "ephemeral_1h_input_tokens": cache_write if rng.random() < 0.7 else 0,
            "ephemeral_5m_input_tokens": 0 if rng.random() < 0.7 else cache_write,
        },
        "service_tier": "standard",
        "speed": "standard",
    }
    return usage, cache_read


def context_ceiling(model: str) -> int:
    return 135_000 if "haiku" in model else 900_000


def claude_tool(project: str, rng: random.Random) -> tuple[str, dict, str]:
    path = f"/home/user/{project}/{rng.choice(MODULES)}"
    return rng.choice(
        [
            (
                "Bash",
                {"command": "pytest -q", "description": "Run the suite"},
                "14 passed in 2.31s",
            ),
            ("Read", {"file_path": path}, "     1\tfrom __future__ import annotations"),
            (
                "Edit",
                {"file_path": path, "old_string": "return None", "new_string": "return ok()"},
                f"Applied 1 edit to {path}",
            ),
            (
                "Grep",
                {"pattern": "def handler", "path": f"/home/user/{project}"},
                f"{path}:12:def handler(request):",
            ),
            (
                "WebSearch",
                {"query": "liveness and readiness probe patterns"},
                "3 results about health probe conventions.",
            ),
        ]
    )


def write_subagent(
    folder: Path,
    session: str,
    project: str,
    agent_id: str,
    tool_use_id: str,
    description: str,
    start: datetime,
    duration_ms: int,
    rng: random.Random,
) -> tuple[int, int]:
    directory = folder / session / "subagents"
    directory.mkdir(parents=True, exist_ok=True)
    cwd = f"/home/user/{project}"
    model = pick(CLAUDE_MODELS, rng)
    ceiling = context_ceiling(model)
    lines: list[str] = []
    steps = rng.randint(1, 3)
    gap = timedelta(milliseconds=duration_ms / (steps * 2 + 1))
    prompt_id = str(uuid.uuid4())
    clock = start
    parent = claude_record(
        lines,
        session,
        cwd,
        clock,
        None,
        {
            "type": "user",
            "promptId": prompt_id,
            "version": "2.1.260",
            "gitBranch": "main",
            "message": {"role": "user", "content": description},
        },
        agent_id=agent_id,
    )
    total = 0
    tool_uses = 0
    cache_read = 0
    for step in range(steps):
        usage, cache_read = claude_usage(step, cache_read, ceiling, rng)
        total += (
            usage["input_tokens"]
            + usage["cache_read_input_tokens"]
            + usage["cache_creation_input_tokens"]
            + usage["output_tokens"]
        )
        tool_use_ref = f"toolu_{uuid.uuid4().hex[:16]}"
        block: dict
        if step == steps - 1:
            block = {"type": "text", "text": rng.choice(CLAUDE_REPLIES)}
            stop_reason = "end_turn"
            output = ""
        else:
            name, tool_input, output = claude_tool(project, rng)
            block = {"type": "tool_use", "id": tool_use_ref, "name": name, "input": tool_input}
            stop_reason = "tool_use"
            tool_uses += 1
        clock += gap
        parent = claude_record(
            lines,
            session,
            cwd,
            clock,
            parent,
            {
                "type": "assistant",
                "requestId": f"req_{uuid.uuid4().hex[:16]}",
                "apiBlockIndex": 0,
                "attributionAgent": "general-purpose",
                "message": {
                    "id": f"msg_{uuid.uuid4().hex[:20]}",
                    "type": "message",
                    "role": "assistant",
                    "model": model,
                    "stop_reason": stop_reason,
                    "content": [block],
                    "usage": usage,
                },
            },
            agent_id=agent_id,
        )
        if stop_reason == "end_turn":
            continue
        clock += gap
        parent = claude_record(
            lines,
            session,
            cwd,
            clock,
            parent,
            {
                "type": "user",
                "promptId": prompt_id,
                "toolUseResult": {
                    "stdout": output,
                    "stderr": "",
                    "interrupted": False,
                    "is_error": False,
                },
                "message": {
                    "role": "user",
                    "content": [
                        {"type": "tool_result", "tool_use_id": tool_use_ref, "content": output}
                    ],
                },
            },
            agent_id=agent_id,
        )
    (directory / f"agent-{agent_id}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (directory / f"agent-{agent_id}.meta.json").write_text(
        json.dumps(
            {
                "agentType": "general-purpose",
                "description": description,
                "toolUseId": tool_use_id,
                "spawnDepth": 1,
            }
        ),
        encoding="utf-8",
    )
    return total, tool_uses


def write_claude(root: Path, day: datetime, rng: random.Random) -> None:
    project = pick([(p, 1 / len(PROJECTS)) for p in PROJECTS], rng)
    session = str(uuid.uuid4())
    folder = root / f"-home-user-{project}"
    folder.mkdir(parents=True, exist_ok=True)
    model = pick(CLAUDE_MODELS, rng)
    if rng.random() < 0.12:
        model = f"{model}[1m]"
    ceiling = context_ceiling(model)
    cwd = f"/home/user/{project}"
    calls = rng.randint(6, 40)
    lines: list[str] = []
    clock = day
    parent: str | None = None
    cache_read = 0
    made = 0
    while made < calls:
        prompt_id = str(uuid.uuid4())
        clock += timedelta(seconds=rng.randint(20, 240))
        parent = claude_record(
            lines,
            session,
            cwd,
            clock,
            parent,
            {
                "type": "user",
                "promptId": prompt_id,
                "version": "2.1.260",
                "permissionMode": "acceptEdits",
                "gitBranch": "main",
                "message": {"role": "user", "content": rng.choice(CLAUDE_PROMPTS)},
            },
        )
        steps = min(rng.randint(1, 5), calls - made)
        for step in range(steps):
            if rng.random() < 0.08:
                message, status = rng.choice(CLAUDE_API_ERRORS)
                clock += timedelta(seconds=rng.randint(1, 4))
                claude_record(
                    lines,
                    session,
                    cwd,
                    clock,
                    parent,
                    {
                        "type": "system",
                        "subtype": "api_error",
                        "level": "error",
                        "source": "request_retry",
                        "retryAttempt": rng.randint(1, 3),
                        "retryInMs": 600,
                        "maxRetries": 10,
                        "error": {"message": message, "status": status},
                    },
                )
            usage, cache_read = claude_usage(made, cache_read, ceiling, rng)
            if rng.random() < 0.15:
                usage["iterations"] = [
                    {"input_tokens": usage["input_tokens"], "output_tokens": usage["output_tokens"]}
                ] * rng.randint(2, 3)
            blocks: list[dict] = []
            if rng.random() < 0.55:
                blocks.append({"type": "thinking", "thinking": rng.choice(CLAUDE_THINKING)})
            tool_use_id = f"toolu_{uuid.uuid4().hex[:16]}"
            description = rng.choice(CLAUDE_AGENT_TASKS)
            agent_id: str | None = None
            output = ""
            if step == steps - 1:
                blocks.append({"type": "text", "text": rng.choice(CLAUDE_REPLIES)})
                stop_reason = "end_turn"
            elif rng.random() < 0.18:
                agent_id = f"ag-{uuid.uuid4().hex[:8]}"
                blocks.append(
                    {
                        "type": "tool_use",
                        "id": tool_use_id,
                        "name": "Agent",
                        "input": {
                            "description": description,
                            "subagent_type": "general-purpose",
                        },
                    }
                )
                stop_reason = "tool_use"
            else:
                name, tool_input, output = claude_tool(project, rng)
                blocks.append(
                    {"type": "tool_use", "id": tool_use_id, "name": name, "input": tool_input}
                )
                stop_reason = "tool_use"

            message_id = f"msg_{uuid.uuid4().hex[:20]}"
            request_id = f"req_{uuid.uuid4().hex[:16]}"
            clock += timedelta(seconds=rng.randint(2, 12))
            for index, block in enumerate(blocks):
                if index:
                    clock += timedelta(milliseconds=rng.randint(400, 2600))
                parent = claude_record(
                    lines,
                    session,
                    cwd,
                    clock,
                    parent,
                    {
                        "type": "assistant",
                        "requestId": request_id,
                        "apiBlockIndex": index,
                        "message": {
                            "id": message_id,
                            "type": "message",
                            "role": "assistant",
                            "model": model,
                            "stop_reason": stop_reason,
                            "content": [block],
                            "usage": usage,
                        },
                    },
                )
            made += 1
            if stop_reason == "end_turn":
                continue

            interrupted = False
            if agent_id is not None:
                clock += timedelta(seconds=rng.randint(1, 4))
                duration_ms = rng.randint(8000, 90000)
                tokens, tool_uses = write_subagent(
                    folder,
                    session,
                    project,
                    agent_id,
                    tool_use_id,
                    description,
                    clock,
                    duration_ms,
                    rng,
                )
                clock += timedelta(milliseconds=duration_ms)
                outcome = {
                    "agentId": agent_id,
                    "description": description,
                    "totalDurationMs": duration_ms,
                    "totalTokens": tokens,
                    "totalToolUseCount": tool_uses,
                    "status": "completed",
                    "interrupted": False,
                }
                content = "Summarised the findings above."
            else:
                clock += timedelta(seconds=rng.randint(1, 40))
                roll = rng.random()
                interrupted = roll < 0.05
                failed = 0.05 <= roll < 0.12
                outcome = {
                    "stdout": "" if failed else output,
                    "stderr": "Traceback (most recent call last): SyntaxError" if failed else "",
                    "interrupted": interrupted,
                    "is_error": failed,
                }
                content = "The user interrupted this tool call." if interrupted else output
            parent = claude_record(
                lines,
                session,
                cwd,
                clock,
                parent,
                {
                    "type": "user",
                    "promptId": prompt_id,
                    "sourceToolAssistantUUID": parent,
                    "toolUseResult": outcome,
                    "message": {
                        "role": "user",
                        "content": [
                            {"type": "tool_result", "tool_use_id": tool_use_id, "content": content}
                        ],
                    },
                },
            )
            if interrupted:
                clock += timedelta(seconds=1)
                parent = claude_record(
                    lines,
                    session,
                    cwd,
                    clock,
                    parent,
                    {
                        "type": "user",
                        "promptId": prompt_id,
                        "message": {
                            "role": "user",
                            "content": [{"type": "text", "text": "[Request interrupted by user]"}],
                        },
                    },
                )
                break
        if rng.random() < 0.12:
            clock += timedelta(seconds=rng.randint(2, 20))
            duration_ms = rng.randint(2500, 9000)
            post_tokens = rng.randint(15000, 30000)
            boundary = claude_record(
                lines,
                session,
                cwd,
                clock,
                None,
                {
                    "type": "system",
                    "subtype": "compact_boundary",
                    "level": "info",
                    "logicalParentUuid": parent,
                    "content": "",
                    "compactMetadata": {
                        "trigger": rng.choice(["auto", "manual"]),
                        "preTokens": rng.randint(120000, 180000),
                        "durationMs": duration_ms,
                        "postTokens": post_tokens,
                    },
                },
            )
            cache_read = post_tokens
            clock += timedelta(milliseconds=duration_ms)
            parent = claude_record(
                lines,
                session,
                cwd,
                clock,
                boundary,
                {
                    "type": "user",
                    "promptId": prompt_id,
                    "isCompactSummary": True,
                    "isVisibleInTranscriptOnly": True,
                    "message": {
                        "role": "user",
                        "content": "Summary of the conversation so far: the endpoint was added.",
                    },
                },
            )
    (folder / f"{session}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")


def codex_record(stamp: datetime, record_type: str, payload: dict) -> str:
    return json.dumps({"timestamp": iso(stamp), "type": record_type, "payload": payload})


def codex_item(
    stamp: datetime,
    thread_id: str,
    turn_id: str,
    item: dict,
    started: datetime,
    completed: datetime,
) -> str:
    return codex_record(
        stamp,
        "event_msg",
        {
            "type": "item_completed",
            "thread_id": thread_id,
            "turn_id": turn_id,
            "item": item,
            "started_at_ms": epoch_ms(started),
            "completed_at_ms": epoch_ms(completed),
        },
    )


def write_codex(root: Path, day: datetime, rng: random.Random) -> None:
    project = pick([(p, 1 / len(PROJECTS)) for p in PROJECTS], rng)
    session = str(uuid.uuid4())
    folder = root / f"{day:%Y/%m/%d}"
    folder.mkdir(parents=True, exist_ok=True)
    model = pick(CODEX_MODELS, rng)
    cwd = f"/home/user/{project}"
    capacity = 400000
    clock = day
    lines = [
        codex_record(
            clock,
            "session_meta",
            {
                "id": session,
                "session_id": session,
                "timestamp": iso(clock),
                "cwd": cwd,
                "originator": "codex_cli_rs",
                "cli_version": "0.55.0",
                "model_provider": "openai",
                "model": model,
            },
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
    deltas = rng.randint(4, 25)
    thread_id = f"th_{uuid.uuid4().hex[:12]}"
    context = rng.randint(6000, 14000)
    growth = max(1000, (90000 - context) // max(deltas - 1, 1))
    made = 0
    turn = 0
    while made < deltas:
        turn += 1
        turn_id = str(uuid.uuid4())
        clock += timedelta(seconds=rng.randint(15, 300))
        turn_start = clock
        passthrough = {"internal_chat_message_metadata_passthrough": {"turn_id": turn_id}}
        lines.append(
            codex_record(
                clock,
                "event_msg",
                {
                    "type": "task_started",
                    "turn_id": turn_id,
                    "model_context_window": capacity,
                },
            )
        )
        lines.append(
            codex_record(
                clock,
                "turn_context",
                {
                    "turn_id": turn_id,
                    "cwd": cwd,
                    "model": model,
                    "effort": rng.choice(["low", "medium", "high"]),
                    "summary": "auto",
                },
            )
        )
        clock += timedelta(seconds=1)
        lines.append(
            codex_record(
                clock,
                "response_item",
                {
                    "type": "message",
                    "role": "user",
                    "content": [{"type": "input_text", "text": rng.choice(CODEX_PROMPTS)}],
                    **passthrough,
                },
            )
        )
        reply = ""
        steps = min(rng.randint(1, 3), deltas - made)
        for step in range(steps):
            reason_id = f"rs_{uuid.uuid4().hex[:16]}"
            clock += timedelta(milliseconds=rng.randint(300, 1500))
            if rng.random() < 0.75:
                spent = timedelta(milliseconds=rng.randint(900, 9000))
                lines.append(
                    codex_item(
                        clock + spent,
                        thread_id,
                        turn_id,
                        {"type": "Reasoning", "id": reason_id, "summary_text": []},
                        clock,
                        clock + spent,
                    )
                )
                clock += spent
            lines.append(
                codex_record(
                    clock,
                    "response_item",
                    {
                        "type": "reasoning",
                        "id": reason_id,
                        "summary": [
                            {"type": "summary_text", "text": rng.choice(CODEX_REASONING)}
                        ],
                        "encrypted_content": "gAAAAA-synthetic",
                        **passthrough,
                    },
                )
            )

            if step < steps - 1:
                call_id = f"call_{uuid.uuid4().hex[:12]}"
                clock += timedelta(milliseconds=rng.randint(200, 900))
                flavor = rng.random()
                if flavor < 0.18:
                    lines.append(
                        codex_record(
                            clock,
                            "response_item",
                            {
                                "type": "function_call",
                                "id": f"fc_{uuid.uuid4().hex[:12]}",
                                "name": "notes__search",
                                "arguments": json.dumps({"query": "export job"}),
                                "call_id": call_id,
                                **passthrough,
                            },
                        )
                    )
                    spent_ms = rng.randint(400, 6000)
                    clock += timedelta(milliseconds=spent_ms)
                    lines.append(
                        codex_record(
                            clock,
                            "event_msg",
                            {
                                "type": "mcp_tool_call_end",
                                "call_id": call_id,
                                "invocation": {
                                    "server": "notes",
                                    "tool": "search",
                                    "arguments": {"query": "export job"},
                                },
                                "duration": {
                                    "secs": spent_ms // 1000,
                                    "nanos": (spent_ms % 1000) * 1_000_000,
                                },
                                "result": {"Ok": {"content": [], "isError": False}},
                            },
                        )
                    )
                elif flavor < 0.45:
                    target = rng.choice(MODULES)
                    started = clock
                    lines.append(
                        codex_record(
                            clock,
                            "response_item",
                            {
                                "type": "custom_tool_call",
                                "id": f"ctc_{uuid.uuid4().hex[:12]}",
                                "status": "completed",
                                "call_id": call_id,
                                "name": "apply_patch",
                                "input": f"*** Begin Patch\n*** Update File: {target}\n"
                                "*** End Patch",
                                **passthrough,
                            },
                        )
                    )
                    clock += timedelta(milliseconds=rng.randint(200, 3000))
                    lines.append(
                        codex_item(
                            clock,
                            thread_id,
                            turn_id,
                            {
                                "type": "FileChange",
                                "id": f"chg-{turn}-{step}",
                                "status": "completed",
                                "changes": [{"path": f"{cwd}/{target}", "kind": "update"}],
                            },
                            started,
                            clock,
                        )
                    )
                    lines.append(
                        codex_record(
                            clock,
                            "response_item",
                            {
                                "type": "custom_tool_call_output",
                                "id": f"cto_{uuid.uuid4().hex[:12]}",
                                "call_id": call_id,
                                "output": [
                                    {"type": "output_text", "text": f"Success. Updated {target}"}
                                ],
                                **passthrough,
                            },
                        )
                    )
                else:
                    command, output = rng.choice(CODEX_COMMANDS)
                    started = clock
                    lines.append(
                        codex_record(
                            clock,
                            "response_item",
                            {
                                "type": "function_call",
                                "id": f"fc_{uuid.uuid4().hex[:12]}",
                                "name": "shell",
                                "arguments": json.dumps({"command": command, "workdir": cwd}),
                                "call_id": call_id,
                                **passthrough,
                            },
                        )
                    )
                    clock += timedelta(milliseconds=rng.randint(300, 12000))
                    exit_code = 0 if rng.random() < 0.88 else 1
                    lines.append(
                        codex_item(
                            clock,
                            thread_id,
                            turn_id,
                            {
                                "type": "CommandExecution",
                                "id": f"exec-{turn}-{step}",
                                "command": command,
                                "cwd": cwd,
                                "status": "completed" if exit_code == 0 else "failed",
                                "exit_code": exit_code,
                                "aggregated_output": output,
                            },
                            started,
                            clock,
                        )
                    )
                    clock += timedelta(milliseconds=rng.randint(50, 400))
                    lines.append(
                        codex_record(
                            clock,
                            "response_item",
                            {
                                "type": "function_call_output",
                                "id": f"fco_{uuid.uuid4().hex[:12]}",
                                "call_id": call_id,
                                "output": f"Exit code: {exit_code}\n{output}",
                                **passthrough,
                            },
                        )
                    )
            else:
                reply = rng.choice(CODEX_REPLIES)
                message_id = f"msg_{uuid.uuid4().hex[:16]}"
                clock += timedelta(milliseconds=rng.randint(200, 800))
                spent = timedelta(milliseconds=rng.randint(500, 4000))
                lines.append(
                    codex_item(
                        clock + spent,
                        thread_id,
                        turn_id,
                        {"type": "AgentMessage", "id": message_id, "content": []},
                        clock,
                        clock + spent,
                    )
                )
                clock += spent
                lines.append(
                    codex_record(
                        clock,
                        "response_item",
                        {
                            "type": "message",
                            "id": message_id,
                            "role": "assistant",
                            "content": [{"type": "output_text", "text": reply}],
                            **passthrough,
                        },
                    )
                )

            if rng.random() < 0.06:
                clock += timedelta(seconds=1)
                lines.append(
                    codex_record(
                        clock,
                        "event_msg",
                        {"type": "stream_error", "message": rng.choice(CODEX_ERRORS)},
                    )
                )

            if rng.random() < 0.1:
                clock += timedelta(seconds=1)
                started = clock
                lines.append(
                    codex_record(
                        clock,
                        "compacted",
                        {
                            "message": "context compacted",
                            "replacement_history": [
                                {"type": "message", "id": f"h_{index}", "role": role, "content": []}
                                for index, role in enumerate(["user", "assistant", "user"])
                            ],
                            "window_number": turn,
                            "window_id": f"w_{turn}",
                        },
                    )
                )
                lines.append(
                    codex_record(clock, "context_compacted", {"type": "context_compacted"})
                )
                clock += timedelta(milliseconds=rng.randint(1500, 8000))
                lines.append(
                    codex_item(
                        clock,
                        thread_id,
                        turn_id,
                        {"type": "ContextCompaction", "id": f"cc-{turn}"},
                        started,
                        clock,
                    )
                )
                context = rng.randint(8000, 20000)

            clock += timedelta(milliseconds=rng.randint(200, 1200))
            total_input = context
            context = min(context + growth, 92000)
            last = {
                "input_tokens": total_input,
                "cached_input_tokens": int(total_input * rng.uniform(0.5, 0.92)) if made else 0,
                "cache_write_input_tokens": 0,
                "output_tokens": rng.randint(300, 4000),
                "reasoning_output_tokens": rng.randint(0, 1500),
                "total_tokens": 0,
            }
            last["total_tokens"] = last["input_tokens"] + last["output_tokens"]
            for field, value in last.items():
                running[field] += value
            lines.append(
                codex_record(
                    clock,
                    "event_msg",
                    {
                        "type": "token_count",
                        "info": {
                            "total_token_usage": dict(running),
                            "last_token_usage": last,
                            "model_context_window": capacity,
                        },
                        "rate_limits": None,
                    },
                )
            )
            made += 1

        clock += timedelta(seconds=rng.randint(1, 5))
        duration_ms = int((clock - turn_start).total_seconds() * 1000)
        if rng.random() < 0.1:
            lines.append(
                codex_record(
                    clock,
                    "event_msg",
                    {
                        "type": "turn_aborted",
                        "turn_id": turn_id,
                        "reason": "interrupted",
                        "duration_ms": duration_ms,
                    },
                )
            )
        else:
            lines.append(
                codex_record(
                    clock,
                    "event_msg",
                    {
                        "type": "task_complete",
                        "turn_id": turn_id,
                        "last_agent_message": reply,
                        "duration_ms": duration_ms,
                        "time_to_first_token_ms": rng.randint(400, 3000),
                    },
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
    end = datetime.now(tz=UTC).replace(hour=9, minute=0, second=0, microsecond=0)
    with sqlite3.connect(db_path) as conn:
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


def main(target: Path, days: int = 45, seed: int = 7) -> None:
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
    print(f"demo logs written to {target}")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/demo"))
