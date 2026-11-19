---
title: Ai usage cost Overview
aliases: []
tags: [module, overview]
area: application
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/*]
verified-against: 1445ea834ab7
chunk: ch-localtokenomics-src-ai-usage-cost
approved-by: human
approved-at: '2026-11-19T06:39:06+00:00'
---

# Ai usage cost Overview

What Ai usage cost is made of and how it connects to the rest of the code.

## How it works

Ai usage cost holds 38 source files and 9978 lines, with 12 routes declared in 1 files, 51 entities, 719 tests that live in it or import its files. The most depended-on files are `src/ai_usage_cost/models.py`, `src/ai_usage_cost/trace.py`, `src/ai_usage_cost/sources/base.py`. It uses [[Ai usage cost render Overview]], [[Ai usage cost sources Overview]]. It is used by [[Ai usage cost sources Overview]], [[Ai usage cost render Overview]].

The purpose column quotes each file's own header comment where it has one. Every file is cited by its full line range, and every public name by the line that declares it.

### What the package is for

The package reads usage records that AI coding tools already write on the machine, turns each record into a priced request, and reports spend by client, provider, model and project. The tool is read only toward the logs: it opens source databases in read only mode (`src/ai_usage_cost/sources/base.py:117-129`) and keeps its own results in a separate SQLite store (`src/ai_usage_cost/store.py:140-151`).

The default store lives under the home folder in `.ai-usage-cost/usage.db` (`src/ai_usage_cost/pipeline.py:28`). The version string is `0.2.0` (`src/ai_usage_cost/__init__.py:1`).

### Four layers

The core files fall into four layers, from the entry points down to the data models.

1. Entry points. The command line has the commands `scan`, `serve`, `demo`, `export`, `collect`, `sql`, `alert` and `tui` (`src/ai_usage_cost/cli.py:71-376`), and the HTTP interface is built by `create_app` (`src/ai_usage_cost/api.py:198-404`).
2. Pipeline. `analyze` reads the store and prices every event, and `report_of` filters and summarises the result (`src/ai_usage_cost/pipeline.py:166-245`, `src/ai_usage_cost/pipeline.py:305-349`).
3. Cost model. `RateTable`, `price_event` and `cost_of` turn tokens into dollars (`src/ai_usage_cost/pricing.py:252-372`, `src/ai_usage_cost/pricing.py:429-437`, `src/ai_usage_cost/pricing.py:495-562`).
4. Data. Pydantic models describe tokens, events, costs and buckets (`src/ai_usage_cost/models.py:12-134`), and the SQLite store persists requests, files, spans, outcomes and exclusions (`src/ai_usage_cost/store.py:21-87`).

### Why the cost is "what it would have cost"

Cost is computed from token counts and a published rate table, not read from a bill. Where a tool also logs its own cost, that figure is kept beside the computed one and never replaces it (`src/ai_usage_cost/models.py:70-72`). The pipeline raises a warning when the two disagree by more than five percent of the reported figure or one cent (`src/ai_usage_cost/pipeline.py:118-138`).

### What a reader must know

A request whose log has no token counts is not treated as free. Its cost state is `unavailable`, which is different from `unpriced` (known tokens, no rate) and `free` (a local provider priced at zero) (`src/ai_usage_cost/pricing.py:417-426`). The four states are drawn in [[Cost state of a request]].

The pipeline never silently guesses a price. A model priced from a shorter id prefix is marked `estimated` and produces a warning (`src/ai_usage_cost/pipeline.py:221-227`), and a model with no rate is excluded from totals but its tokens are still counted (`src/ai_usage_cost/pipeline.py:212-220`).

Days are the machine's local calendar days. Logs carry different offsets, so one function resolves the day and both bucketing and since and until filtering use it (`src/ai_usage_cost/models.py:137-146`).

Related notes: [[Ai usage cost API]], [[Ai usage cost Data Model]], [[Ai usage cost Workflows]], [[Ai usage cost Security]], [[Ai usage cost Diagrams]].

## Reference

%% generated:chunk-files start (do not edit; run brain docs generate) %%
### Files

| File | Purpose | Lines | Imports | Imported by | Code |
|---|---|---|---|---|---|
| `src/ai_usage_cost/__init__.py` | - | 1 | 0 | 17 | [[src/ai_usage_cost/__init__.py]] `src/ai_usage_cost/__init__.py:1` |
| `src/ai_usage_cost/aggregate.py` | - | 723 | 4 | 11 | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:1-723` |
| `src/ai_usage_cost/api.py` | - | 404 | 9 | 2 | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:1-404` |
| `src/ai_usage_cost/cli.py` | - | 380 | 8 | 2 | [[src/ai_usage_cost/cli.py]] `src/ai_usage_cost/cli.py:1-380` |
| `src/ai_usage_cost/collect.py` | - | 282 | 2 | 2 | [[src/ai_usage_cost/collect.py]] `src/ai_usage_cost/collect.py:1-282` |
| `src/ai_usage_cost/demo.py` | - | 369 | 3 | 3 | [[src/ai_usage_cost/demo.py]] `src/ai_usage_cost/demo.py:1-369` |
| `src/ai_usage_cost/models.py` | - | 146 | 0 | 51 | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:1-146` |
| `src/ai_usage_cost/pipeline.py` | - | 349 | 9 | 15 | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:1-349` |
| `src/ai_usage_cost/pricing.py` | - | 562 | 1 | 15 | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:1-562` |
| `src/ai_usage_cost/privacy.py` | - | 116 | 1 | 6 | [[src/ai_usage_cost/privacy.py]] `src/ai_usage_cost/privacy.py:1-116` |
| `src/ai_usage_cost/render/__init__.py` | - | 0 | 0 | 0 | empty file |
| `src/ai_usage_cost/render/png.py` | - | 101 | 1 | 1 | [[src/ai_usage_cost/render/png.py]] `src/ai_usage_cost/render/png.py:1-101` |
| `src/ai_usage_cost/render/terminal.py` | - | 86 | 1 | 1 | [[src/ai_usage_cost/render/terminal.py]] `src/ai_usage_cost/render/terminal.py:1-86` |
| `src/ai_usage_cost/sources/__init__.py` | - | 27 | 1 | 13 | [[src/ai_usage_cost/sources/__init__.py]] `src/ai_usage_cost/sources/__init__.py:1-27` |
| `src/ai_usage_cost/sources/antigravity.py` | - | 314 | 3 | 2 | [[src/ai_usage_cost/sources/antigravity.py]] `src/ai_usage_cost/sources/antigravity.py:1-314` |
| `src/ai_usage_cost/sources/base.py` | - | 176 | 2 | 28 | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:1-176` |
| `src/ai_usage_cost/sources/claude_code.py` | - | 690 | 3 | 3 | [[src/ai_usage_cost/sources/claude_code.py]] `src/ai_usage_cost/sources/claude_code.py:1-690` |
| `src/ai_usage_cost/sources/cline.py` | - | 442 | 3 | 3 | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:1-442` |
| `src/ai_usage_cost/sources/codex.py` | - | 962 | 3 | 2 | [[src/ai_usage_cost/sources/codex.py]] `src/ai_usage_cost/sources/codex.py:1-962` |
| `src/ai_usage_cost/sources/copilot_chat.py` | - | 72 | 3 | 1 | [[src/ai_usage_cost/sources/copilot_chat.py]] `src/ai_usage_cost/sources/copilot_chat.py:1-72` |
| `src/ai_usage_cost/sources/copilot_cli.py` | - | 275 | 3 | 1 | [[src/ai_usage_cost/sources/copilot_cli.py]] `src/ai_usage_cost/sources/copilot_cli.py:1-275` |
| `src/ai_usage_cost/sources/cursor.py` | - | 97 | 3 | 1 | [[src/ai_usage_cost/sources/cursor.py]] `src/ai_usage_cost/sources/cursor.py:1-97` |
| `src/ai_usage_cost/sources/dyad.py` | - | 64 | 3 | 1 | [[src/ai_usage_cost/sources/dyad.py]] `src/ai_usage_cost/sources/dyad.py:1-64` |
| `src/ai_usage_cost/sources/gemini_cli.py` | Gemini CLI (google-gemini/gemini-cli) session logs. | 225 | 3 | 1 | [[src/ai_usage_cost/sources/gemini_cli.py]] `src/ai_usage_cost/sources/gemini_cli.py:1-225` |
| `src/ai_usage_cost/sources/grok_build.py` | - | 123 | 3 | 1 | [[src/ai_usage_cost/sources/grok_build.py]] `src/ai_usage_cost/sources/grok_build.py:1-123` |
| `src/ai_usage_cost/sources/jan.py` | - | 110 | 3 | 1 | [[src/ai_usage_cost/sources/jan.py]] `src/ai_usage_cost/sources/jan.py:1-110` |
| `src/ai_usage_cost/sources/kilo_code.py` | Kilo Code v7 -- an OpenCode fork storing kilo.db; same parser, different roots. | 17 | 1 | 1 | [[src/ai_usage_cost/sources/kilo_code.py]] `src/ai_usage_cost/sources/kilo_code.py:1-17` |
| `src/ai_usage_cost/sources/kilo_legacy.py` | Kilo Code legacy v5 task dirs: see cline.py for the format. | 33 | 1 | 1 | [[src/ai_usage_cost/sources/kilo_legacy.py]] `src/ai_usage_cost/sources/kilo_legacy.py:1-33` |
| `src/ai_usage_cost/sources/muse_code.py` | - | 295 | 3 | 1 | [[src/ai_usage_cost/sources/muse_code.py]] `src/ai_usage_cost/sources/muse_code.py:1-295` |
| `src/ai_usage_cost/sources/ollama_app.py` | - | 56 | 3 | 1 | [[src/ai_usage_cost/sources/ollama_app.py]] `src/ai_usage_cost/sources/ollama_app.py:1-56` |
| `src/ai_usage_cost/sources/openai_compat.py` | - | 96 | 3 | 1 | [[src/ai_usage_cost/sources/openai_compat.py]] `src/ai_usage_cost/sources/openai_compat.py:1-96` |
| `src/ai_usage_cost/sources/opencode.py` | OpenCode (anomalyco/opencode, formerly sst/opencode) -- SQLite opencode.db. | 352 | 3 | 2 | [[src/ai_usage_cost/sources/opencode.py]] `src/ai_usage_cost/sources/opencode.py:1-352` |
| `src/ai_usage_cost/sources/qwen_code.py` | Qwen Code (QwenLM/qwen-code, a Gemini CLI fork) session logs. | 175 | 3 | 1 | [[src/ai_usage_cost/sources/qwen_code.py]] `src/ai_usage_cost/sources/qwen_code.py:1-175` |
| `src/ai_usage_cost/sources/roo_code.py` | Roo Code (final release 3.53.0, archived 2026-05-15): see cline.py for the format. | 29 | 1 | 1 | [[src/ai_usage_cost/sources/roo_code.py]] `src/ai_usage_cost/sources/roo_code.py:1-29` |
| `src/ai_usage_cost/sources/windsurf.py` | - | 92 | 3 | 1 | [[src/ai_usage_cost/sources/windsurf.py]] `src/ai_usage_cost/sources/windsurf.py:1-92` |
| `src/ai_usage_cost/store.py` | - | 727 | 3 | 12 | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:1-727` |
| `src/ai_usage_cost/trace.py` | - | 877 | 2 | 30 | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:1-877` |
| `src/ai_usage_cost/tui.py` | - | 133 | 1 | 1 | [[src/ai_usage_cost/tui.py]] `src/ai_usage_cost/tui.py:1-133` |
%% generated:chunk-files end %%

%% generated:chunk-interface start (do not edit; run brain docs generate) %%
### Public interface

| Name | Kind | File | Code |
|---|---|---|---|
| `TokenUsage` | class | `src/ai_usage_cost/models.py` | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:12` |
| `UsageEvent` | class | `src/ai_usage_cost/models.py` | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:49` |
| `CostBreakdown` | class | `src/ai_usage_cost/models.py` | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:75` |
| `PricedEvent` | class | `src/ai_usage_cost/models.py` | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:117` |
| `Bucket` | class | `src/ai_usage_cost/models.py` | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:123` |
| `local_day` | function | `src/ai_usage_cost/models.py` | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:137` |
| `Span` | class | `src/ai_usage_cost/trace.py` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:55` |
| `Capabilities` | class | `src/ai_usage_cost/trace.py` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:104` |
| `ContextSnapshot` | class | `src/ai_usage_cost/trace.py` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:112` |
| `OutcomeSignals` | class | `src/ai_usage_cost/trace.py` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:134` |
| `OutcomeUpdate` | class | `src/ai_usage_cost/trace.py` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:141` |
| `Outcome` | class | `src/ai_usage_cost/trace.py` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:147` |
| `EconRow` | class | `src/ai_usage_cost/trace.py` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:154` |
| `Economics` | class | `src/ai_usage_cost/trace.py` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:177` |
| `Insight` | class | `src/ai_usage_cost/trace.py` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:184` |
| `Trace` | class | `src/ai_usage_cost/trace.py` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:192` |
| `SpanContent` | class | `src/ai_usage_cost/trace.py` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:201` |
| `amplification` | function | `src/ai_usage_cost/trace.py` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:208` |
| `Source` | class | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:18` |
| `present_roots` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:47` |
| `scan` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:52` |
| `read_json_lines` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:69` |
| `read_json_records` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:87` |
| `read_sqlite` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:117` |
| `jsonl_files` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:132` |
| `single_file` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:136` |
| `parse_timestamp` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:140` |
| `project_of` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:159` |
| `as_int` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:165` |
| `title_of` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:169` |
| `SourceInfo` | class | `src/ai_usage_cost/pipeline.py` | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:31` |
| `Analysis` | class | `src/ai_usage_cost/pipeline.py` | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:45` |
| `unknown_models` | function | `src/ai_usage_cost/pipeline.py` | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:66` |
| `estimated_models` | function | `src/ai_usage_cost/pipeline.py` | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:100` |
| `tier_unpriced_models` | function | `src/ai_usage_cost/pipeline.py` | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:107` |
| `reported_cost_divergences` | function | `src/ai_usage_cost/pipeline.py` | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:118` |
| `analyze` | function | `src/ai_usage_cost/pipeline.py` | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:166` |
| `filter_events` | function | `src/ai_usage_cost/pipeline.py` | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:248` |
| `report_of` | function | `src/ai_usage_cost/pipeline.py` | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:305` |
| `PriceSet` | class | `src/ai_usage_cost/pricing.py` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:29` |
| `Band` | class | `src/ai_usage_cost/pricing.py` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:40` |
| `Peak` | class | `src/ai_usage_cost/pricing.py` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:47` |
| `Period` | class | `src/ai_usage_cost/pricing.py` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:68` |
| `ProviderRules` | class | `src/ai_usage_cost/pricing.py` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:101` |
| `PartialRules` | class | `src/ai_usage_cost/pricing.py` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:109` |
| `merge_rules` | function | `src/ai_usage_cost/pricing.py` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:120` |
| `ModelRate` | class | `src/ai_usage_cost/pricing.py` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:126` |
| `Prefix` | class | `src/ai_usage_cost/pricing.py` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:169` |
| `ModelMatch` | class | `src/ai_usage_cost/pricing.py` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:224` |
| `UnpricedModel` | class | `src/ai_usage_cost/pricing.py` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:232` |
| `effective_prefixes` | function | `src/ai_usage_cost/pricing.py` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:245` |
| `registry` | function | `src/ai_usage_cost/sources/__init__.py` | [[src/ai_usage_cost/sources/__init__.py]] `src/ai_usage_cost/sources/__init__.py:11` |
| `client_labels` | function | `src/ai_usage_cost/sources/__init__.py` | [[src/ai_usage_cost/sources/__init__.py]] `src/ai_usage_cost/sources/__init__.py:23` |
| `IngestSummary` | class | `src/ai_usage_cost/store.py` | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:134` |
| `open_store` | function | `src/ai_usage_cost/store.py` | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:140` |
| `fingerprint_of` | function | `src/ai_usage_cost/store.py` | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:154` |
| `ingest` | function | `src/ai_usage_cost/store.py` | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:190` |
| `load_spans` | function | `src/ai_usage_cost/store.py` | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:531` |
| `get_outcome` | function | `src/ai_usage_cost/store.py` | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:551` |
| `put_outcome` | function | `src/ai_usage_cost/store.py` | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:568` |
| `delete_session` | function | `src/ai_usage_cost/store.py` | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:595` |
| `session_exists` | function | `src/ai_usage_cost/store.py` | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:609` |
| `session_flags` | function | `src/ai_usage_cost/store.py` | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:628` |
| `file_counts` | function | `src/ai_usage_cost/store.py` | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:664` |
| `load` | function | `src/ai_usage_cost/store.py` | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:668` |
| `Totals` | class | `src/ai_usage_cost/aggregate.py` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:26` |
| `SeriesPoint` | class | `src/ai_usage_cost/aggregate.py` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:37` |
| `SessionRow` | class | `src/ai_usage_cost/aggregate.py` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:48` |
| `UnknownModel` | class | `src/ai_usage_cost/aggregate.py` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:77` |
| `WarningSeverity` | class | `src/ai_usage_cost/aggregate.py` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:83` |
| `WarningInstance` | class | `src/ai_usage_cost/aggregate.py` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:100` |
| `WarningGroup` | class | `src/ai_usage_cost/aggregate.py` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:115` |
| `warning_groups_of` | function | `src/ai_usage_cost/aggregate.py` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:385` |
| `Facets` | class | `src/ai_usage_cost/aggregate.py` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:454` |
| `Report` | class | `src/ai_usage_cost/aggregate.py` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:462` |
| `totals_of` | function | `src/ai_usage_cost/aggregate.py` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:491` |
| `group` | function | `src/ai_usage_cost/aggregate.py` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:512` |
| `ContentUnavailable` | class | `src/ai_usage_cost/privacy.py` | [[src/ai_usage_cost/privacy.py]] `src/ai_usage_cost/privacy.py:48` |
| `Config` | class | `src/ai_usage_cost/privacy.py` | [[src/ai_usage_cost/privacy.py]] `src/ai_usage_cost/privacy.py:52` |
| `load_config` | function | `src/ai_usage_cost/privacy.py` | [[src/ai_usage_cost/privacy.py]] `src/ai_usage_cost/privacy.py:60` |

100 more public names are omitted; see the cited files.
%% generated:chunk-interface end %%
