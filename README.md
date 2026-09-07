# ai-usage-cost

Reads the local logs and data files that AI coding tools already write on your machine —
Claude Code, Codex, Ollama, Jan, Dyad, GitHub Copilot Chat, Google Antigravity, and any
OpenAI-compatible gateway export — and tells you what that usage would have cost at API
list prices, across every provider, client, and project. In the terminal, or in a local
dashboard.

Everything runs offline and read-only. No API key, no network calls, nothing uploaded.

```
$ ai-usage-cost scan
╭─────────────────────────────── Total ────────────────────────────────╮
│ $3,431.96 API-equivalent cost                                        │
│ 40,194 requests across 787 log files · rates as of 2026-09-07        │
╰──────────────────────────────────────────────────────────────────────╯
```

## Install

```bash
uv tool install git+https://github.com/GeorgiNaydenov/ai-usage-cost
# or, from a clone:
uv venv && uv pip install -e ".[png,dev]"
```

Python 3.11+. `[png]` adds the matplotlib exporter; `[dev]` adds the test tools.

## Use

```bash
ai-usage-cost scan                          # terminal summary, broken down by model
ai-usage-cost scan --by client               # or: provider | model | project | day
ai-usage-cost scan --since 2026-08-01 --no-sidechains -v
ai-usage-cost serve                          # dashboard at http://127.0.0.1:8420
ai-usage-cost export report.json             # or report.png
```

Point a source at logs elsewhere with `--root SOURCE=PATH` (repeatable), e.g.
`--root claude-code=/tmp/demo/claude --root openai-compat=/tmp/gateway-logs`.
`--db PATH` picks a different SQLite store; `--rebuild` discards it and reparses
everything from scratch.

## Where it reads

| Source | Client(s) | Path | Token data |
|---|---|---|---|
| Claude Code | `claude-code` | `~/.claude/projects/*/*.jsonl` | full |
| Codex | `codex-cli`, `codex-desktop` | `~/.codex/sessions/**/rollout-*.jsonl` | full |
| Ollama app | `ollama-app` | `%LOCALAPPDATA%\Ollama\db.sqlite` (and platform equivalents) | none — session only |
| Jan | `jan` | `~/jan/threads`, `<app-data>/Jan/data/threads` | none — session only |
| Dyad | `dyad` | `<app-data>/dyad/sqlite.db` | none — session only |
| GitHub Copilot Chat | `copilot-chat` | `<vscode-data>/User/globalStorage/github.copilot-chat/session-store.db` | none — session only |
| Google Antigravity | `antigravity` | `~/.gemini/antigravity/brain/*/.system_generated/logs/transcript*.jsonl` | none — session only |
| OpenAI-compatible | `openai-compat` | none by default — pass `--root openai-compat=PATH` | full, when the log has `usage` |

On Windows, `~` resolves to `%USERPROFILE%`. Most clients log a session but not token
counts — see Cost states below for how that's represented rather than hidden or guessed.

## Cost states

Every request lands in exactly one state, shown per-session in the dashboard and CLI:

- **priced** — has a rate in `rates.json`. Counted in every total.
- **free** — the provider is marked free (a local model runtime). Counted at $0.00.
- **unpriced** — token counts exist but no rate entry matches the model. Listed with its
  token count and excluded from cost totals until you add a price.
- **unavailable** — the client's log carries no token counts at all. The request and
  session are still counted, cost is never fabricated.

A model is never silently priced at $0.

## Storage

Requests are deduplicated and persisted in a local SQLite store at
`~/.ai-usage-cost/usage.db` (override with `--db`). A scan only reparses files that
changed since the last run; a file that disappears keeps its rows. Cost is never
stored — it's computed at read time from `rates.json`, so editing prices reprices
history immediately.

Cross-source dedup uses each request's own id when the log has one (Claude's message
id, an OpenAI-compatible `id`), or a fallback of session + timestamp + model + token
total when it doesn't — so the same request logged by two overlapping tools (a Codex
CLI rollout and its desktop app telemetry, for instance) is counted once.

## How the cost is worked out

Tokens are normalised into four **disjoint** billable buckets — uncached input, cache
read, cache write, output — and priced from `src/ai_usage_cost/rates.json`. Multipliers
apply to the model's base input price:

| | multiplier |
|---|---|
| cache read | 0.1× |
| cache write, 5-minute TTL | 1.25× |
| cache write, 1-hour TTL | 2.0× |
| batch tier | 0.5× on everything |

Provider is resolved per request: an adapter that knows who's billing declares it
directly; otherwise a gateway prefix in the model id (`us.anthropic.` → Bedrock,
`openrouter/` → OpenRouter) or, failing that, the matched rate entry's own vendor,
resolves it. `rates.json` is a snapshot (see its `as_of` field), not a live feed — edit
it freely.

### Caveats worth knowing

- These are **list-price equivalents for the tokens you actually spent** — not what a
  subscription billed you, and the two are not comparable directly.
- Only requests that reached the model and were logged are counted.
- Several sources here (Ollama app, Jan, Dyad, Copilot Chat, Antigravity) log sessions
  but no token counts on this machine's real data — see Cost states above.

## Editing prices

`src/ai_usage_cost/rates.json` is plain data. Add a model:

```json
{"match": "claude-opus-6", "provider": "anthropic", "display": "Claude Opus 6",
 "input": 5.0, "output": 25.0}
```

`match` is a prefix; the longest match wins. Add `"providers": {"my-provider": {"free": true}}`
to mark a provider's models as always free (a local runtime, for instance).

## Adding another source

`src/ai_usage_cost/sources/base.py` defines the contract:

```python
class Source:
    id: str
    label: str
    clients: dict[str, str]
    default_roots: Callable[[], list[Path]]
    files: Callable[[Path], list[Path]]
    parse: Callable[[Path, list[str]], Iterator[UsageEvent]]
```

A new source is one module ending in `SOURCE = Source(...)`; every module under
`sources/` is discovered automatically, so nothing else needs to change. Steps:

1. `src/ai_usage_cost/sources/<name>.py` — a `parse(path, warnings)` generator yielding
   `UsageEvent`s, plus the `SOURCE` constant.
2. A fixture under `tests/fixtures/<name>/`.
3. `tests/test_<name>.py` asserting the parsed events.

Run `pytest`. The CLI, API, storage, and dashboard pick up the new source with no
further edits.

## Layout

```
src/ai_usage_cost/
  models.py     UsageEvent / TokenUsage / CostBreakdown / cost states  (pydantic)
  pricing.py    rate lookup, provider resolution, cost arithmetic
  rates.json    the editable price table
  store.py      SQLite storage: migrations, idempotent ingest, dedup
  sources/      one module per source  <- extension point
  aggregate.py  group by day / model / client / provider / project / session
  pipeline.py   ingest -> load -> price -> filter -> report
  api.py        FastAPI JSON API + static host for the dashboard
  cli.py        scan | serve | export
  render/       terminal (rich), png (matplotlib)
web/            React + Vite + Tailwind + Recharts dashboard source
```

## Development

```bash
pytest
ruff check src tests
mypy src

python scripts/demo_logs.py /tmp/demo     # synthetic logs to develop against
ai-usage-cost serve --root claude-code=/tmp/demo/claude --root codex=/tmp/demo/codex \
  --root jan=/tmp/demo/jan --root dyad=/tmp/demo/dyad/sqlite.db --db /tmp/demo/usage.db

cd web && npm install && npm run build     # writes into src/ai_usage_cost/web/dist
```

The built dashboard bundle is committed, so `serve` works without Node installed.
