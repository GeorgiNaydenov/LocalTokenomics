# Direction: from cost dashboard to local agent observability

Status: phases 1 to 3 are built. Spans, per-session economics, context snapshots, outcomes,
redacted content read-through and a local-compute collector spike all ship on this branch.
What follows is the direction, the audit it was planned against, and what building it proved
or disproved.

## The question the product should answer

What happened during this task, where did time and tokens go, and what caused success or failure?

Today the tool answers only "what did it cost". The gap is that cost is an outcome of behaviour, and
none of the behaviour is currently visible: no tool calls, no retries, no context growth, no
timeline, no notion of whether the task even succeeded.

## Core entities

Every source normalizes into:

| Entity | Meaning |
|---|---|
| Session | One conversation or agent run |
| Task | A user-level objective, possibly spanning several turns |
| Turn | One user request and the activity it caused |
| Span | A model call, tool call, retrieval, compaction, error, or subagent operation |
| Usage | Tokens, cost, cache use, latency, context pressure |
| Artifact | Prompt, message, tool input/output, file, retrieval result, summary |
| Outcome | Successful, partial, failed, abandoned, unrated |
| Capability | Whether each value is measured, derived, estimated, inferred, or unavailable |

The capability field is the load-bearing one. An unavailable value must never be coerced to zero,
because a zero is indistinguishable from a real zero and silently corrupts every aggregate built on
top of it. This is the same principle the current cost states already enforce (`unavailable` is a
distinct state from `free`), extended to every metric rather than just cost.

## Capability audit against real logs

This section is the reason the branch exists. The product direction assumed a capability matrix; the
actual logs on this machine disagree with it in several places. Audited by aggregating record and
payload types across real sessions (30 Claude Code files, 40 recent Codex rollouts, 35 Antigravity
transcripts).

### What each source actually exposes

**Claude Code** (`~/.claude/projects/*/*.jsonl`)

- Record types: `user`, `assistant`, `system`, `attachment`, `queue-operation`, `last-prompt`,
  `bridge-session`, `custom-title`, `atis-latch`.
- `uuid` and `parentUuid` on every record. This is a real parent-child trace tree, not a flat log,
  so the execution structure can be reconstructed exactly rather than inferred from ordering.
- Content blocks: `assistant:tool_use`, `user:tool_result`, `assistant:thinking`, `assistant:text`.
  Tool spans pair up directly.
- `toolUseResult` carries `stdout`, `stderr`, `interrupted`, `isImage`, `noOutputExpected`, and
  `sourceToolAssistantUUID` linking a result back to the call that produced it.
- `isSidechain` marks subagent work; `requestId`, `apiBlockIndex`, `promptId`, `permissionMode`,
  `effort`, `cwd`, `gitBranch`, `version` are all present.
- Usage carries `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`,
  `output_tokens`, `output_tokens_details`, `service_tier`, `speed`, `inference_geo`, and
  `iterations`.
- **No duration on model or tool calls.** The only `durationMs` fields sit on attachments (47
  occurrences) and hook infos (1). Latency for Claude Code must be derived from timestamp deltas
  between adjacent records, which measures wall-clock gap, not model time.

**Codex** (`~/.codex/sessions/**/rollout-*.jsonl`)

- Paired tool spans: `response_item:custom_tool_call` / `custom_tool_call_output` (843 each) and
  `response_item:function_call` / `function_call_output` (156/158).
- `event_msg:item_completed` (2316) carries `started_at_ms`, `completed_at_ms` and `duration` per
  item. `event_msg:task_complete` carries `duration_ms` **and `time_to_first_token_ms`**.
  `event_msg:mcp_tool_call_end` carries `duration` and the full `invocation` (server, tool,
  arguments).
- `turn_id` and `thread_id` give real turn and session identity. `turn_context` carries `cwd`,
  `workspace_roots`, `approval_policy`, `sandbox_policy`, `timezone`.
- `event_msg:token_count.info` carries `total_token_usage`, `last_token_usage`, and
  **`model_context_window`**. Context capacity is measured, not assumed.
- `compacted` records carry `replacement_history`: the actual content that replaced the old history.
  `event_msg:context_compacted` and `response_item:compaction` mark the events.
- `event_msg:turn_aborted` carries `reason` (e.g. `interrupted`), `started_at`, `completed_at`,
  `duration_ms`. A direct, measured cancellation signal.
- `response_item:reasoning` (1223) and `inter_agent_communication_metadata` are present.

**Antigravity** (`~/.gemini/antigravity/brain/*/.system_generated/logs/transcript*.jsonl`)

- Records carry `step_index`, `source`, `type`, `status`, `created_at`, `content`, `tool_calls`,
  `thinking`, `truncated_fields`, `error`.
- Typed actions: `PLANNER_RESPONSE`, `VIEW_FILE`, `CODE_ACTION`, `RUN_COMMAND`, `LIST_DIRECTORY`,
  `GREP_SEARCH`, `USER_INPUT`, `SYSTEM_MESSAGE`, `CONVERSATION_HISTORY`, `EPHEMERAL_MESSAGE`.
- `status` and `error` are per-step outcome signals. `truncated_fields` is a built-in
  data-completeness marker the capability model can consume directly.
- Still **no token counts of any kind**, consistent with the current adapter emitting `tokens=None`.

### Corrected capability matrix

The proposed matrix understated two sources and overstated latency for a third. Corrected against
the logs above:

| Source | Trace | Tokens | Cost | Context | Latency | Outcome signal |
|---|---|---|---|---|---|---|
| Codex | Full, typed, paired | Measured | Measured | **Measured capacity + explicit compaction** | **Measured, incl. TTFT** | `turn_aborted.reason` |
| Claude Code | Full, exact parent/child tree | Measured | Measured | Derived from per-call input tokens | **Derived only** (timestamp deltas) | `interrupted` on tool results |
| Antigravity | Full, typed steps | Unavailable | Unavailable | Unavailable | Derived from `created_at` | `status`, `error` |
| Cursor | Not yet audited | Unknown | Unknown | Unknown | Unknown | Unknown |
| Ollama / Jan / Dyad / Copilot Chat | Session only | Unavailable | Unavailable | Unavailable | Unavailable | None |

Two corrections worth carrying into the UI:

1. **Codex has the strongest context story, not a partial one.** It reports the context window
   capacity and logs compaction events with the replaced history attached. Phase 3's context work is
   therefore mostly a Codex feature at first, and mostly reconstruction for Claude Code.
2. **Claude Code has the strongest trace story but the weakest latency story.** The `uuid`/
   `parentUuid` tree is exact, so the agent tree needs no inference at all, but any duration shown
   for a Claude Code model call is a wall-clock gap between log records, and must be labelled
   derived, never measured. Presenting the two sources' durations in the same column without that
   label would be the single easiest way to make this product quietly dishonest.

## Phase 1 shape

Phase 1 is trace foundation: make a session followable chronologically without opening raw JSONL,
while preserving current usage and pricing behaviour exactly.

The existing pipeline runs `sources`, then `UsageEvent`, `store`, `price`, `aggregate`, `report`.
`UsageEvent` is a billing record: one row per priced request. A span is a different shape. It has a
parent, a duration, a kind, and often no tokens at all.

The smallest change that supports this is a second stream alongside the existing one rather than a
rewrite of it:

- Sources gain an optional `spans(path, warnings)` generator beside the existing `parse`, so a
  source that cannot produce spans simply does not implement it and its capability registry entry
  says so. `Source` already carries `token_data` and `display_path`; a `capabilities` field extends
  the same pattern.
- A `Span` model: `span_id`, `parent_id`, `session_id`, `turn_id`, `kind` (model call, tool call,
  retrieval, compaction, error, subagent), `started_at`, `ended_at`, `duration` plus its provenance,
  `tool_name`, `status`, `tokens` (optional), `error`, and an artifact reference.
- A `spans` table keyed on a fingerprint, mirroring how `requests` already dedupes, so rescans stay
  idempotent.
- Provenance travels with the value, not in a separate lookup: every numeric field that can be
  measured by one source and derived by another needs its own capability marker, or the UI cannot
  label it correctly.

The existing `requests` table, pricing, and every current report stay untouched. Cost keeps being
computed at read time from `rates.json`.

## Privacy is now load-bearing, not a nice-to-have

Cost data is boring. Traces are not: they contain prompts, source code, file contents, command
output, and anything a secret-bearing environment variable happened to print. The current tool
stores no content at all, so it has never had to think about this.

Non-negotiable before any content capture ships:

- Metadata-only is the default; content capture is opt-in, not opt-out.
- Redaction happens **before** SQLite persistence, not at render time. A redacting UI over a
  plaintext store is not a privacy feature.
- Secret-pattern detection, per-project exclusion, a maximum stored content size, per-session
  delete, and separate retention for metadata and content.
- Exports redacted by default.

This is not hypothetical. While generating the README screenshots for the redesign on the previous
branch, three sources (Antigravity, Copilot Chat, Ollama) silently fell back to their real default
roots and pulled real personal data into what was supposed to be a synthetic capture. That was
caught before anything was committed, but it happened with a tool that stores no content. The same
class of mistake with trace content in the store is a different order of problem.

## Open questions

- **Task identity.** Codex gives `turn_id`/`thread_id` and explicit `task_started`/`task_complete`
  boundaries. Claude Code gives a prompt tree but no task concept. Does "task" mean one user turn,
  or a user-labelled grouping spanning turns? The metrics that matter most (cost per successful
  task) depend entirely on this answer, and the two sources will not agree naturally.
- **Outcome capture.** Manual classification is the honest starting point, but it only gets used if
  it is nearly free at the moment of review. Automatic signals exist per source (`turn_aborted`,
  `interrupted`, Antigravity's `status`/`error`) but they detect *abandonment*, not *success*.
- **Context reconstruction confidence.** For Codex the compaction record states what was replaced.
  For Claude Code, context composition is inferred from the visible message tree, which is not the
  same as the server-side context. Any contributor breakdown for Claude Code is an estimate and has
  to say so.
- **Scale.** 806 log files and 43k requests already produce a 16k-session report. Spans are roughly
  an order of magnitude more numerous than requests. The current "load everything into memory and
  filter in Python" pipeline will not survive that, so Phase 1 should assume span queries are
  answered by SQL, not by list comprehensions.
- **Cursor.** Not audited yet. Nothing should be claimed about it until its format is examined the
  same way the three above were.

## Non-goals

Exact cloud GPU utilization or energy. Decrypting hidden reasoning. Claiming reconstructed context
equals server-side context. Replaying sessions. Universal support for undocumented formats.
Treating subscription pricing as equivalent to API cost.

Local compute instrumentation (Phase 6) is explicitly a separate collector: GPU, VRAM, power and
throughput must be sampled live and correlated with model-call timestamps. It cannot be
reconstructed afterwards from coding-client logs, so it does not belong in the adapter model at all.

## What building it changed

### Two defects in the shipped cost path, found by building on top of it

**Codex session identity was wrong.** The reader accepted any payload `id` of eight characters
or more as the session id, and recent rollouts carry such an id on every response item. One
session was therefore reported as hundreds: across the logs on this machine, 419 real sessions
appeared as 16,677, and 302 of 483 rollout files yielded more than one id. The "16k-session
report" this document previously cited as a scale problem was mostly this bug. Session identity
now comes only from the `session_meta` record. Costs, tokens and request counts were never
affected; only the grouping was.

**Codex span ids collided across files.** Fixing session identity meant one session now spans
many rollout files, and per-file counters plus the log's own repeated `turn_id` values
(`external-import-turn-1` appears in eight files) collided. The store silently discarded 6,939
spans, about 6% of the total, through `INSERT OR IGNORE`. Span ids are now scoped to the file
that produced them.

Both were found only because the trace layer forced a second, independent reading of the same
logs. Neither would have surfaced from the cost totals, which looked correct throughout.

### The ingest trap, confirmed

`files` now records the parser version alongside mtime and size. Without it every file already
ingested for its token counts would have been skipped forever and never gained spans. This cost
one full reparse on upgrade and cannot recur silently.

### Corrections to the capability matrix above

Measured against real logs while building, not assumed:

- **Antigravity is richer than "typed steps".** It logs subagent invocations carrying the child
  conversation id, and those children are themselves scanned sessions, so its subagent topology
  is an exact cross-session link rather than an inference. It also reports command exit codes:
  74 across these logs, which Phase 5's automated outcome signal can read directly.
- **Claude Code subagents join exactly.** Each `subagents/agent-*.jsonl` has a sibling
  `.meta.json` carrying the `toolUseId` of the spawning call, plus the agent type and spawn
  depth, so the link holds even when the parent never recorded a result.
- **Codex `item_completed` is not universal.** It appears only in recent rollouts; older ones
  have no per-item timing at all, and their durations are honestly derived or absent. The
  adapter is tested against both shapes.
- **Real zeros exist.** Some Codex spans have a genuine zero duration, from two records inside
  the same millisecond. They are measured zeros, not missing values, and the distinction is
  visible in the UI.
- **Tokens per second is almost never available.** It requires both tokens and duration to be
  measured on the same span, which did not occur in any real session sampled. It renders as
  unavailable rather than as a number.

### What the local-compute spike found

What the collector can measure depends entirely on which interface the machine exposes, so it
picks a backend at runtime and records which one produced each row:

| Backend | Utilisation | VRAM used | VRAM total | Power |
|---|---|---|---|---|
| `nvidia-smi` | measured | measured | measured | measured |
| `rocm-smi` | measured | measured | measured | measured where the card reports it |
| Windows performance counters | measured | measured | not exposed | not exposed |
| none available | nothing is sampled | | | |

The counter fallback is the important case, because it is what a machine without vendor tooling
falls back to, and it cannot report watts at all. Energy is therefore never measured: it is
computed from a `--tdp-watts` figure the user supplies, labelled estimated, and simply absent
when no figure is given. There is no default wattage, because a guessed one would silently turn
an unknown into a number.

Two limits shape how useful any of this is. Sampling through the counter fallback costs several
seconds per reading, since it spawns a shell and enumerates every GPU engine instance, so the
effective floor is roughly one sample every five to seven seconds. That is meaningful across a
turn or a session and meaningless for a single tool call. And every one of these interfaces is
machine-wide: a sample reflects everything using the GPU, not the agent alone. Ollama's
`/api/ps` is polled opportunistically to record which models were resident, but it is optional
and never gates a sample.

Correlation with spans stays a time join, never an adapter, and cloud-model sessions never show
hardware numbers at all.

## Still open

- **Task identity.** Outcomes are per session. Turns are spans, but nothing groups several
  turns into one user-level task, so cost per successful task is really cost per successful
  session.
- **Outcome capture.** Manual rating works and the automatic signals (aborted turns,
  interrupted tools, error spans, exit codes) are all captured, but they detect abandonment,
  not success. Nothing yet reads a test result.
- **Ratings are read at scan time**, so a session rated in the UI moves into its bucket only
  after the next rescan.
- **Cursor.** Still unaudited. It ships as a capability row with everything unavailable.
- **Cross-file span dedupe.** Spans do not dedupe across files the way requests do, so span
  counts run about 0.2% above request counts on real Codex data where a resumed session
  re-lists history.
