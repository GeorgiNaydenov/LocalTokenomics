# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.2.0] - 2026-10-01

### Added

- Nine experimental source parsers: Gemini CLI, Qwen Code, OpenCode, Kilo Code (v7), Cline,
  Roo Code, Kilo Code (legacy) and GitHub Copilot CLI, plus Muse Code. Each is flagged
  `experimental` in `/api/meta`. See Notes.
- Pricing schema v2 for `rates.json`, additive (a v1 file still loads and prices
  identically): exact per-model cache read and write prices, input-size bands that price the
  whole request, service-tier variants (`fast`, `priority`, `flex`, `batch`, `ultrafast`),
  dated price periods, a recurring UTC peak window (used for DeepSeek), and a per-row
  `cache_rules` that merges over the provider block instead of replacing it. Every row now
  carries `source`, `verified` and `status`.
- The file is validated on load: duplicate `match` keys, rows whose provider has no block,
  overlapping periods and malformed peak windows are rejected.
- Match kinds: `exact`, `suffix` (dated snapshot, `[1m]`, Bedrock `-vN:M`, `-latest`; quiet)
  and `estimated` (any other prefix-only match). An estimated model is priced from its
  parent row, shown under its own id, and raises a caution warning.
- Gateway prefixes are stripped repeatedly (`openrouter/anthropic/<id>`), and dotted Claude
  ids (`claude-sonnet-4.6`) resolve to their dashed rows.
- 148 rows re-read against vendor pricing pages on 2026-10-01, including Claude Opus 5.5 and
  Sonnet 5.5, the GPT-6 family, GPT-5.6 Cyber, Grok 4.7, Meta Muse Spark, TypeSafe Jev and
  DeepSeek V4.1 Flash. Meta and TypeSafe are new providers. Gemini 4 Argon is a watchlist
  entry because it has no API id yet.
- Tool-reported cost (`reported_cost`) is kept next to the cost computed from tokens, with a
  divergence warning when they disagree.
- Codex `service_tier` is read and used to pick a price variant.
- A stale-rates notice: info after 30 days, caution after 90.
- `scripts/rates_diff.py`, a maintainer tool that compares `rates.json` with LiteLLM's public
  catalogue. It never writes the file; the app itself still fetches nothing.
- The demo now includes one deliberately estimated model and one unpriced model so every cost
  state is visible, and takes context windows from `rates.json`.

### Changed

- Prices and history will change after upgrading. Cost is computed on load from `rates.json`,
  so every past request is repriced with the new table; the earlier figures were wrong or
  stale in the ways listed under Fixed. On the author's own logs the net effect was Opus 5.5
  down about $51, GPT-5.6 Sol up about $134 and GPT-5.5 up about $11, and GPT-6 Sol newly
  priced; yours will differ.
- Mistral, MiniMax and Amazon Nova rows were re-keyed to the vendors' real API ids.
- `PARSER_VERSION` is now 6, so an existing store reparses all log files once on the first
  scan after upgrading.
- The package description and `pyproject.toml` version reflect multi-tool coverage.
- The demo's model lists now live in one place (`ai_usage_cost.demo`) and are imported by
  `scripts/demo_logs.py`; both use current models.

### Fixed

- Claude Opus 5.5 was billed at Claude Opus 5 prices: its id only started like the older
  row's, so it was matched by prefix, priced and labelled as the older model. Opus 5.5 now
  has its own row ($4 input, $20 output, cache read $0.20) and its totals fall.
- The `gpt-5.6` alias was priced at $2/$12 (the Terra price) although OpenAI routes it to
  GPT-5.6 Sol. It now follows Sol's price, tiers and bands, so requests logged under the
  plain `gpt-5.6` id cost more than before.
- GPT-5.6 Sol history is priced at the price in force on each date: $5/$30 before the
  2026-08-21 cut and $4/$20 after it, instead of one flat rate for all dates. Requests
  before the cut therefore cost more than the previous table showed.
- Prefix collisions: a model id that merely begins like an older row no longer silently takes
  that row's price and name. It is `estimated` and flagged unless the extra text is a known
  benign suffix.
- GPT-5.5 requests over 272K input tokens are priced at the long-context rate, which raises
  totals slightly.
- `gpt-5.3-codex-spark` has no list price and is recorded as unpriced rather than being
  priced as `gpt-5.3-codex` by prefix.

### Notes

- The nine new parsers were written from each tool's source code or documentation and tested
  on synthetic fixtures. None has been confirmed against a real session. GitHub Copilot CLI
  persists only cumulative per-session totals at shutdown, so a session that never shut down
  cleanly has no usage. Muse Code's format is undocumented and was reconstructed from
  third-party parsers.
- Codex logs the service tier a request asked for, not the one OpenAI billed. A Fast request
  that OpenAI downgraded is priced slightly high.
- Not modelled: Anthropic `inference_geo` +10% and Bedrock or Vertex regional uplifts, OpenAI
  regional +10%, Gemini cache storage per hour and audio rates, the Qwen thinking-output
  price split, DeepSeek Chinese public-holiday off-peak pricing, and web-search fees.
- `codex-auto-review` has no published per-token price and stays unpriced.
- Amazon and older Claude 3 prices could not be confirmed against a vendor page.

## [0.1.0] - 2026-09-10

### Added

- LocalTokenomics (`ai-usage-cost`): a local, read-only tool that reads the logs and data
  stores AI coding tools already write on your machine (Claude Code, Codex, Antigravity,
  Cursor, Windsurf, Grok Build, GitHub Copilot Chat, Dyad, Jan, Ollama and any
  OpenAI-compatible export), prices them at published API list rates, and reports them in the
  terminal or a local dashboard. No network call is made to price usage.
- Session traces for the sources that log enough detail: model and tool calls, per-turn cost
  and duration, and context window occupancy. Every value is labelled measured, derived,
  estimated, inferred or unavailable.
- A recency-aware dashboard, a SQLite store, optional Datasette, alert and Textual extras, and
  a synthetic `ai-usage-cost demo` mode.
- Metric explanations on every figure, session titles taken from each tool's own name for the
  session, and incremental reads of Claude Code logs.

### Fixed

- A broad audit of cost and token accuracy: streaming assistant messages are deduplicated so
  the final record wins (earlier output and reasoning tokens were undercounted), repeated
  usage snapshots are no longer summed, forked threads and counter resets are recognised,
  several rates were added or corrected, and models priced by prefix inheritance are flagged.
  Session duration, retry and tool-error counts were corrected, and CI was added.
