# ai-usage-cost

Reads the logs that **Claude Code** and **Codex CLI** already write on your machine and
tells you what that usage would have cost at **API list prices** — in the terminal, or in
a local dashboard.

Everything runs offline and read-only. No API key, no network calls, nothing uploaded.

```
$ ai-usage-cost scan
╭─────────────────────────────── Total ────────────────────────────────╮
│ $175.95 API-equivalent cost                                          │
│ 181,102,758 tokens across 1,816 requests in 90 sessions              │
│ 2026-07-16 to 2026-08-28 · 90 log files · rates as of 2026-08-29     │
│ Prompt caching saved $466.00 (would have been $641.96)               │
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
ai-usage-cost scan                     # terminal summary, broken down by model
ai-usage-cost scan --by day            # or: tool | project | day
ai-usage-cost scan --since 2026-08-01 --no-sidechains -v
ai-usage-cost serve                    # dashboard at http://127.0.0.1:8420
ai-usage-cost export report.json       # or report.png
```

Point it at logs elsewhere with `--claude-dir` / `--codex-dir`.

## Where it reads

| Tool | Path | What is parsed |
|---|---|---|
| Claude Code | `~/.claude/projects/*/*.jsonl` | `type: "assistant"` records, `message.usage` |
| Codex CLI | `~/.codex/sessions/**/rollout-*.jsonl` | `token_count` events, `info.last_token_usage` |

On Windows these resolve to `%USERPROFILE%\.claude\projects` and `%USERPROFILE%\.codex\sessions`.

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

Two provider differences matter, and are handled in the parsers:

- **Anthropic** reports the buckets disjointly — `input_tokens` already excludes cache
  reads and writes — and splits cache writes by TTL under `usage.cache_creation`, which
  is why the 5m/1h distinction is preserved rather than flattened.
- **OpenAI/Codex** reports `cached_input_tokens` as a *subset* of `input_tokens`, so the
  uncached input billed is the difference. `reasoning_output_tokens` is likewise a subset
  of `output_tokens`. Anthropic's `thinking_tokens` is a subset of `output_tokens` too.
  Subsets are shown for interest and never added to a total.

A few things the parsers deliberately do:

- Claude Code assistant records are **deduplicated** on `(message.id, requestId)` —
  resumed sessions and sidechain copies repeat them across files.
- `usage.iterations` is **not** summed; the top-level usage block is already its total.
- Codex per-turn deltas are **reconciled** against each session's own running total, and
  any drift over 1% is reported as a warning rather than hidden.
- A model with no entry in `rates.json` is **never silently priced at $0** — it is listed
  with its token count and excluded from totals.

### Caveats worth knowing

- These are **list-price equivalents for the tokens you actually spent** — what the same
  work would have cost through the API. It is not what your Claude or ChatGPT
  subscription billed you, and the two are not comparable directly.
- `rates.json` is a snapshot (see its `as_of` field), not a live feed. Edit it freely;
  the pre-2025 model rates in particular are best-effort and worth checking before you
  trust totals over old logs.
- Only requests that reached the model are counted, because only those are logged.

## Editing prices

`src/ai_usage_cost/rates.json` is plain data. Add a model:

```json
{"match": "claude-opus-6", "provider": "anthropic", "display": "Claude Opus 6",
 "input": 5.0, "output": 25.0}
```

`match` is a prefix; the longest match wins, so `claude-opus-4-5-20251101` resolves to the
`claude-opus-4-5` entry. Pass `--rates path.json` to use a different file.

## Adding another CLI

`src/ai_usage_cost/sources/base.py` is the extension point. A new source is one module:

```python
class GeminiSource(JsonlSource):
    id = "gemini-cli"
    label = "Gemini CLI"

    def default_roots(self) -> list[Path]: ...
    def iter_file(self, path, warnings) -> Iterator[UsageEvent]: ...

register(GeminiSource())
```

Import it in `sources/base.registry()` and everything downstream — pricing, aggregation,
the API, the dashboard — picks it up unchanged. Nothing after parsing knows which CLI an
event came from beyond its `tool` id.

## Layout

```
src/ai_usage_cost/
  models.py     TokenUsage / UsageEvent / CostBreakdown  (pydantic)
  pricing.py    rate lookup + cost arithmetic
  rates.json    the editable price table
  sources/      one module per CLI  <- extension point
  aggregate.py  group by day / model / project / tool / session
  pipeline.py   scan -> price -> filter -> report
  api.py        FastAPI JSON API + static host for the dashboard
  cli.py        scan | serve | export
  render/       terminal (rich), png (matplotlib)
web/            React + Vite + Tailwind + Recharts dashboard source
```

## Development

```bash
.venv/bin/pytest              # parser + pricing tests
.venv/bin/ruff check src tests
.venv/bin/mypy src

python scripts/demo_logs.py /tmp/demo     # synthetic logs to develop against
ai-usage-cost serve --claude-dir /tmp/demo/claude --codex-dir /tmp/demo/codex

cd web && npm install && npm run build     # writes into src/ai_usage_cost/web/dist
```

The built dashboard bundle is committed, so `serve` works without Node installed.
