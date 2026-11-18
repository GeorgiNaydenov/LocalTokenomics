---
title: Data Entity Catalog
aliases: []
tags: [catalog, data, generated]
area: catalogs
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
---

# Data Entity Catalog

Every entity or table with the component that defines it.

%% generated:entity-catalog start (do not edit; run brain docs generate) %%
| Entity | Table | Columns | Relations | Component | Source | Code |
|---|---|---|---|---|---|---|
| `AlertDecision` | - | 2 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/cli.py]] `src/ai_usage_cost/cli.py:252` |
| `Analysis` | - | 9 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:45` |
| `Bucket` | - | 7 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:123` |
| `Capabilities` | - | 5 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:104` |
| `ClientInfo` | - | 2 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:86` |
| `Config` | - | 5 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/privacy.py]] `src/ai_usage_cost/privacy.py:52` |
| `ContextSnapshot` | - | 14 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:112` |
| `CostBreakdown` | - | 7 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:75` |
| `EconRow` | - | 19 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:154` |
| `Economics` | - | 4 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:177` |
| `Facets` | - | 5 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:454` |
| `IngestSummary` | - | 3 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:134` |
| `Insight` | - | 5 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:184` |
| `ItemTable` | `ItemTable` | 1 | 0 | - | sql | [[tests/test_windsurf.py]] `tests/test_windsurf.py:52` |
| `ItemTable` | `ItemTable` | 1 | 0 | - | sql | [[tests/fixtures/cursor/no_table.sql]] `tests/fixtures/cursor/no_table.sql:1` |
| `ItemTable` | `ItemTable` | 1 | 0 | - | sql | [[tests/fixtures/windsurf/basic.sql]] `tests/fixtures/windsurf/basic.sql:1` |
| `ItemTable` | `ItemTable` | 1 | 0 | - | sql | [[tests/fixtures/windsurf/empty.sql]] `tests/fixtures/windsurf/empty.sql:1` |
| `ItemTable` | `ItemTable` | 1 | 0 | - | sql | [[tests/fixtures/windsurf/malformed.sql]] `tests/fixtures/windsurf/malformed.sql:1` |
| `ItemTable` | `ItemTable` | 1 | 0 | - | sql | [[tests/fixtures/windsurf/no_chat_key.sql]] `tests/fixtures/windsurf/no_chat_key.sql:1` |
| `Meta` | - | 18 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:105` |
| `ModelMatch` | - | 2 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:224` |
| `OutcomeSignals` | - | 4 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:134` |
| `OutcomeUpdate` | - | 3 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:141` |
| `PartialRules` | - | 5 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:109` |
| `Period` | - | 11 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:68` |
| `Prefix` | - | 2 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:169` |
| `PriceSet` | - | 5 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:29` |
| `PricedEvent` | - | 3 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:117` |
| `ProviderRules` | - | 5 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:101` |
| `RateTable` | - | 11 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:252` |
| `Report` | - | 20 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:462` |
| `Sample` | - | 7 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/collect.py]] `src/ai_usage_cost/collect.py:49` |
| `Scanned` | - | 2 | 0 | - | type | [[tests/test_codex.py]] `tests/test_codex.py:20` |
| `Scanned` | - | 2 | 0 | - | type | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:23` |
| `Scanned` | - | 2 | 0 | - | type | [[tests/test_grok_build.py]] `tests/test_grok_build.py:15` |
| `Scanned` | - | 2 | 0 | - | type | [[tests/test_muse_code.py]] `tests/test_muse_code.py:22` |
| `Scanned` | - | 2 | 0 | - | type | [[tests/test_trace_codex.py]] `tests/test_trace_codex.py:28` |
| `SeriesPoint` | - | 8 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:37` |
| `SessionRow` | - | 26 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:48` |
| `Source` | - | 12 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:18` |
| `SourceInfo` | - | 10 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:31` |
| `Span` | - | 30 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:55` |
| `SpanContent` | - | 4 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:201` |
| `Spec` | - | 5 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:82` |
| `TokenUsage` | - | 6 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:12` |
| `Totals` | - | 8 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:26` |
| `Trace` | - | 6 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:192` |
| `UnknownModel` | - | 3 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:77` |
| `UnpricedModel` | - | 3 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:232` |
| `UsageEvent` | - | 21 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:49` |
| `WarningGroup` | - | 11 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:115` |
| `WarningInstance` | - | 10 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:100` |
| `WarningSummary` | - | 4 | 0 | src/ai_usage_cost | type | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:91` |
| `apps` | `apps` | 16 | 0 | src/ai_usage_cost | sql | [[src/ai_usage_cost/demo.py]] `src/ai_usage_cost/demo.py:52` |
| `apps` | `apps` | 16 | 0 | - | sql | [[tests/fixtures/dyad/basic.sql]] `tests/fixtures/dyad/basic.sql:1` |
| `apps` | `apps` | 16 | 0 | - | sql | [[tests/fixtures/dyad/null_title.sql]] `tests/fixtures/dyad/null_title.sql:1` |
| `chats` | `chats` | 5 | 0 | src/ai_usage_cost | sql | [[src/ai_usage_cost/demo.py]] `src/ai_usage_cost/demo.py:71` |
| `chats` | `chats` | 5 | 0 | - | sql | [[tests/fixtures/dyad/basic.sql]] `tests/fixtures/dyad/basic.sql:20` |
| `chats` | `chats` | 5 | 0 | - | sql | [[tests/fixtures/dyad/null_title.sql]] `tests/fixtures/dyad/null_title.sql:20` |
| `cursorDiskKV` | `cursorDiskKV` | 1 | 0 | - | sql | [[tests/test_cursor.py]] `tests/test_cursor.py:62` |
| `cursorDiskKV` | `cursorDiskKV` | 1 | 0 | - | sql | [[tests/fixtures/cursor/basic.sql]] `tests/fixtures/cursor/basic.sql:1` |
| `cursorDiskKV` | `cursorDiskKV` | 1 | 0 | - | sql | [[tests/fixtures/cursor/empty.sql]] `tests/fixtures/cursor/empty.sql:1` |
| `files` | `files` | 10 | 0 | src/ai_usage_cost | sql | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:36` |
| `message` | `message` | 5 | 0 | - | sql | [[tests/test_opencode.py]] `tests/test_opencode.py:20` |
| `message` | `message` | 3 | 0 | - | sql | [[tests/test_opencode.py]] `tests/test_opencode.py:318` |
| `messages` | `messages` | 7 | 0 | src/ai_usage_cost | sql | [[src/ai_usage_cost/demo.py]] `src/ai_usage_cost/demo.py:79` |
| `messages` | `messages` | 7 | 0 | - | sql | [[tests/fixtures/dyad/basic.sql]] `tests/fixtures/dyad/basic.sql:28` |
| `messages` | `messages` | 7 | 0 | - | sql | [[tests/fixtures/dyad/null_title.sql]] `tests/fixtures/dyad/null_title.sql:28` |
| `messages` | `messages` | 14 | 0 | - | sql | [[tests/fixtures/ollama_app/basic.sql]] `tests/fixtures/ollama_app/basic.sql:1` |
| `outcomes` | `outcomes` | 6 | 0 | src/ai_usage_cost | sql | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:63` |
| `part` | `part` | 6 | 0 | - | sql | [[tests/test_opencode.py]] `tests/test_opencode.py:22` |
| `part` | `part` | 3 | 0 | - | sql | [[tests/test_opencode.py]] `tests/test_opencode.py:319` |
| `requests` | `requests` | 26 | 0 | src/ai_usage_cost | sql | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:23` |
| `samples` | `samples` | 7 | 0 | src/ai_usage_cost | sql | [[src/ai_usage_cost/collect.py]] `src/ai_usage_cost/collect.py:19` |
| `session` | `session` | 15 | 0 | - | sql | [[tests/test_opencode.py]] `tests/test_opencode.py:15` |
| `session` | `session` | 1 | 0 | - | sql | [[tests/test_opencode.py]] `tests/test_opencode.py:317` |
| `session_exclusions` | `session_exclusions` | 3 | 0 | src/ai_usage_cost | sql | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:69` |
| `sessions` | `sessions` | 10 | 0 | - | sql | [[tests/fixtures/copilot_chat/basic.sql]] `tests/fixtures/copilot_chat/basic.sql:1` |
| `sessions` | `sessions` | 10 | 0 | - | sql | [[tests/fixtures/copilot_chat/empty.sql]] `tests/fixtures/copilot_chat/empty.sql:1` |
| `trace_events` | `trace_events` | 34 | 0 | src/ai_usage_cost | sql | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:43` |
| `turns` | `turns` | 6 | 1 | - | sql | [[tests/fixtures/copilot_chat/basic.sql]] `tests/fixtures/copilot_chat/basic.sql:14` |
| `turns` | `turns` | 6 | 1 | - | sql | [[tests/fixtures/copilot_chat/empty.sql]] `tests/fixtures/copilot_chat/empty.sql:14` |
%% generated:entity-catalog end %%
