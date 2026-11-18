---
title: Traceability Matrices
aliases: []
tags: [catalog, generated, matrix]
area: catalogs
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
---

# Traceability Matrices

Which component owns which entity and how many interfaces each exposes. Empty cells are counted, never hidden.

%% generated:matrices start (do not edit; run brain docs generate) %%
### Data entity by component

<<<<<<< HEAD
| Entity | `(root)` | `src/ai_usage_cost` | `src/ai_usage_cost/render` | `src/ai_usage_cost/sources` | `(root)` | `web/src` | `web/src/components` | `web/src/components/ui` | [[Web prototype Overview|web/src/prototype]] |
=======
| Entity | `(root)` | `src/ai_usage_cost` | `src/ai_usage_cost/render` | `src/ai_usage_cost/sources` | [[localtokenomics root Overview|(root)]] | [[localtokenomics root Overview|web/src]] | [[localtokenomics root Overview|web/src/components]] | [[localtokenomics root Overview|web/src/components/ui]] | [[localtokenomics root Overview|web/src/prototype]] |
>>>>>>> docs/chunk-ch-localtokenomics-root
|---|---|---|---|---|---|---|---|---|---|
| `AlertDecision` |  | x |  |  |  |  |  |  |  |
| `Analysis` |  | x |  |  |  |  |  |  |  |
| `Bucket` |  | x |  |  |  |  |  |  |  |
| `Capabilities` |  | x |  |  |  |  |  |  |  |
| `ClientInfo` |  | x |  |  |  |  |  |  |  |
| `Config` |  | x |  |  |  |  |  |  |  |
| `ContextSnapshot` |  | x |  |  |  |  |  |  |  |
| `CostBreakdown` |  | x |  |  |  |  |  |  |  |
| `EconRow` |  | x |  |  |  |  |  |  |  |
| `Economics` |  | x |  |  |  |  |  |  |  |
| `Facets` |  | x |  |  |  |  |  |  |  |
| `IngestSummary` |  | x |  |  |  |  |  |  |  |
| `Insight` |  | x |  |  |  |  |  |  |  |
| `ItemTable` |  |  |  |  |  |  |  |  |  |
| `Meta` |  | x |  |  |  |  |  |  |  |
| `ModelMatch` |  | x |  |  |  |  |  |  |  |
| `OutcomeSignals` |  | x |  |  |  |  |  |  |  |
| `OutcomeUpdate` |  | x |  |  |  |  |  |  |  |
| `PartialRules` |  | x |  |  |  |  |  |  |  |
| `Period` |  | x |  |  |  |  |  |  |  |
| `Prefix` |  | x |  |  |  |  |  |  |  |
| `PriceSet` |  | x |  |  |  |  |  |  |  |
| `PricedEvent` |  | x |  |  |  |  |  |  |  |
| `ProviderRules` |  | x |  |  |  |  |  |  |  |
| `RateTable` |  | x |  |  |  |  |  |  |  |
| `Report` |  | x |  |  |  |  |  |  |  |
| `Sample` |  | x |  |  |  |  |  |  |  |
| `Scanned` |  |  |  |  |  |  |  |  |  |
| `SeriesPoint` |  | x |  |  |  |  |  |  |  |
| `SessionRow` |  | x |  |  |  |  |  |  |  |
| `Source` |  | x |  |  |  |  |  |  |  |
| `SourceInfo` |  | x |  |  |  |  |  |  |  |
| `Span` |  | x |  |  |  |  |  |  |  |
| `SpanContent` |  | x |  |  |  |  |  |  |  |
| `Spec` |  | x |  |  |  |  |  |  |  |
| `TokenUsage` |  | x |  |  |  |  |  |  |  |
| `Totals` |  | x |  |  |  |  |  |  |  |
| `Trace` |  | x |  |  |  |  |  |  |  |
| `UnknownModel` |  | x |  |  |  |  |  |  |  |
| `UnpricedModel` |  | x |  |  |  |  |  |  |  |
| `UsageEvent` |  | x |  |  |  |  |  |  |  |
| `WarningGroup` |  | x |  |  |  |  |  |  |  |
| `WarningInstance` |  | x |  |  |  |  |  |  |  |
| `WarningSummary` |  | x |  |  |  |  |  |  |  |
| `apps` |  | x |  |  |  |  |  |  |  |
| `chats` |  | x |  |  |  |  |  |  |  |
| `cursorDiskKV` |  |  |  |  |  |  |  |  |  |
| `files` |  | x |  |  |  |  |  |  |  |
| `message` |  |  |  |  |  |  |  |  |  |
| `messages` |  | x |  |  |  |  |  |  |  |
| `outcomes` |  | x |  |  |  |  |  |  |  |
| `part` |  |  |  |  |  |  |  |  |  |
| `requests` |  | x |  |  |  |  |  |  |  |
| `samples` |  | x |  |  |  |  |  |  |  |
| `session` |  |  |  |  |  |  |  |  |  |
| `session_exclusions` |  | x |  |  |  |  |  |  |  |
| `sessions` |  |  |  |  |  |  |  |  |  |
| `trace_events` |  | x |  |  |  |  |  |  |  |
| `turns` |  |  |  |  |  |  |  |  |  |

Entities with no owning component: 8.

### Routes by component

| Component | Routes |
|---|---|
| `(root)` | 0 |
| `src/ai_usage_cost` | 12 |
| `src/ai_usage_cost/render` | 0 |
| `src/ai_usage_cost/sources` | 0 |
<<<<<<< HEAD
| `(root)` | 0 |
| `web/src` | 0 |
| `web/src/components` | 0 |
| `web/src/components/ui` | 0 |
| [[Web prototype Overview\|web/src/prototype]] | 0 |
=======
| [[localtokenomics root Overview\|(root)]] | 0 |
| [[localtokenomics root Overview\|web/src]] | 0 |
| [[localtokenomics root Overview\|web/src/components]] | 0 |
| [[localtokenomics root Overview\|web/src/components/ui]] | 0 |
| [[localtokenomics root Overview\|web/src/prototype]] | 0 |
>>>>>>> docs/chunk-ch-localtokenomics-root

Components with no routes: 8.
%% generated:matrices end %%
