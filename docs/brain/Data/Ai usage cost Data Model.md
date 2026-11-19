---
title: Ai usage cost Data Model
aliases: []
tags: [data, erd]
area: data
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

# Ai usage cost Data Model

The entities owned by the Ai usage cost chunk.

## How it works

51 entities were found with their columns, defaults, keys, relations and enumerated values. This is the data dictionary of the chunk; tables created only by demo, fixture or seed files are listed here and kept out of the diagrams; the conceptual, logical and physical diagrams are listed in [[Ai usage cost Diagrams]].

### Two kinds of entity

The 51 entities are of two kinds. Most are Pydantic models that exist only in memory and in the JSON the interface returns. Six are SQLite tables the package owns: `requests`, `files`, `trace_events`, `outcomes`, `session_exclusions` and `samples` (`src/ai_usage_cost/store.py:21-87`, `src/ai_usage_cost/collect.py:18-25`). The tables `apps`, `chats` and `messages` that the entity list also shows belong to the demo data generator and are kept out of the diagrams (`src/ai_usage_cost/demo.py:52-79`).

### The core chain

One log record becomes a `UsageEvent` (`src/ai_usage_cost/models.py:49-72`). Its optional `TokenUsage` holds uncached input, cache read, two cache write buckets, output and reasoning output (`src/ai_usage_cost/models.py:12-18`). Pricing wraps the event in a `PricedEvent` with a `CostBreakdown` and a cost state (`src/ai_usage_cost/models.py:117-120`). Grouping sums priced events into `Bucket` rows (`src/ai_usage_cost/models.py:123-134`, `src/ai_usage_cost/aggregate.py:512-536`), and `Report` holds the buckets, the sessions and the warnings (`src/ai_usage_cost/aggregate.py:462-482`). The relationships are drawn in [[Usage cost conceptual model]].

### Rules the models enforce

- Token totals are derived, not stored: `cache_write` is the sum of the two write buckets, `input_total` adds uncached input, cache read and cache write, and `total` adds output. Reasoning output is not added again (`src/ai_usage_cost/models.py:20-33`).
- A cost breakdown keeps a `no_cache_equivalent` figure and derives `cache_savings` as the difference between it and the total (`src/ai_usage_cost/models.py:80`, `src/ai_usage_cost/models.py:100-103`).
- `estimated` on a breakdown is true once any event folded into it was priced from a shorter id prefix. It is also readable under the older name `inherited` for existing consumers (`src/ai_usage_cost/models.py:81-93`).
- A span's duration, tokens and context capacity must each be empty exactly when their provenance is `unavailable` (`src/ai_usage_cost/trace.py:88-101`).
- A rate table is rejected at load when two rows share a match key, when a row names a provider with no rules block, or when a row has overlapping periods (`src/ai_usage_cost/pricing.py:152-160`, `src/ai_usage_cost/pricing.py:271-283`).
- A peak window must use weekdays 0 to 6 and hour ranges that satisfy `0 <= start < end <= 24`, so a range that wraps midnight has to be split in the file (`src/ai_usage_cost/pricing.py:53-60`).

### How the store is shaped

The `requests` table is keyed by a fingerprint, not an id. When the log has a request id the key is the source plus that id, otherwise it is built from session, time, model, token total, file and offset (`src/ai_usage_cost/store.py:154-167`). Five migrations add the trace tables, titles, resume columns and the reported cost, and the store version is stored in `PRAGMA user_version` (`src/ai_usage_cost/store.py:21-87`, `src/ai_usage_cost/store.py:140-151`).

Time stamps are stored as UTC text (`src/ai_usage_cost/store.py:170-171`, `src/ai_usage_cost/store.py:322`).

## Reference

%% generated:chunk-entities start (do not edit; run brain docs generate) %%
### Entity summary

| Entity | Table | Columns | Key | Relations | Referenced by | Code |
|---|---|---|---|---|---|---|
| Totals | - | 8 | - | 0 | - | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:26-34` |
| SeriesPoint | - | 8 | - | 0 | - | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:37-45` |
| SessionRow | - | 26 | - | 0 | - | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:48-74` |
| UnknownModel | - | 3 | - | 0 | - | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:77-80` |
| WarningInstance | - | 10 | - | 0 | - | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:100-111` |
| WarningGroup | - | 11 | - | 0 | - | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:115-127` |
| Facets | - | 5 | - | 0 | - | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:454-459` |
| Report | - | 20 | - | 0 | - | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:462-482` |
| ClientInfo | - | 2 | - | 0 | - | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:86-88` |
| WarningSummary | - | 4 | - | 0 | - | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:91-102` |
| Meta | - | 18 | - | 0 | - | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:105-128` |
| AlertDecision | - | 2 | - | 0 | - | [[src/ai_usage_cost/cli.py]] `src/ai_usage_cost/cli.py:252-254` |
| Sample | - | 7 | - | 0 | - | [[src/ai_usage_cost/collect.py]] `src/ai_usage_cost/collect.py:49-56` |
| samples | `samples` | 7 | - | 0 | - | [[src/ai_usage_cost/collect.py]] `src/ai_usage_cost/collect.py:19-23` |
| apps | `apps` | 16 | `id` | 0 | - | [[src/ai_usage_cost/demo.py]] `src/ai_usage_cost/demo.py:52-69` |
| chats | `chats` | 5 | `id` | 0 | - | [[src/ai_usage_cost/demo.py]] `src/ai_usage_cost/demo.py:71-77` |
| messages | `messages` | 7 | `id` | 0 | - | [[src/ai_usage_cost/demo.py]] `src/ai_usage_cost/demo.py:79-87` |
| TokenUsage | - | 6 | - | 0 | - | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:12-43` |
| UsageEvent | - | 21 | - | 0 | - | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:49-72` |
| CostBreakdown | - | 7 | - | 0 | - | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:75-114` |
| PricedEvent | - | 3 | - | 0 | - | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:117-120` |
| Bucket | - | 7 | - | 0 | - | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:123-134` |
| SourceInfo | - | 10 | - | 0 | - | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:31-41` |
| Analysis | - | 9 | - | 0 | - | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:45-63` |
| PriceSet | - | 5 | - | 0 | - | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:29-37` |
| Period | - | 11 | - | 0 | - | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:68-98` |
| ProviderRules | - | 5 | - | 0 | - | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:101-106` |
| PartialRules | - | 5 | - | 0 | - | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:109-117` |
| Prefix | - | 2 | - | 0 | - | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:169-171` |
| ModelMatch | - | 2 | - | 0 | - | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:224-229` |
| UnpricedModel | - | 3 | - | 0 | - | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:232-242` |
| RateTable | - | 11 | - | 0 | - | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:252-372` |
| Config | - | 5 | - | 0 | - | [[src/ai_usage_cost/privacy.py]] `src/ai_usage_cost/privacy.py:52-57` |
| Source | - | 12 | - | 0 | - | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:18-44` |
| Spec | - | 5 | - | 0 | - | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:82-87` |
| IngestSummary | - | 3 | - | 0 | - | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:134-137` |
| requests | `requests` | 26 | `fingerprint` | 0 | - | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:23-85` |
| files | `files` | 10 | `path` | 0 | - | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:36-82` |
| trace_events | `trace_events` | 34 | `span_id` | 0 | - | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:43-60` |
| outcomes | `outcomes` | 6 | `source`, `session_id` | 0 | - | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:63-68` |
| session_exclusions | `session_exclusions` | 3 | `source`, `session_id` | 0 | - | [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:69-72` |
| Span | - | 30 | - | 0 | - | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:55-101` |
| Capabilities | - | 5 | - | 0 | - | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:104-109` |
| ContextSnapshot | - | 14 | - | 0 | - | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:112-131` |
| OutcomeSignals | - | 4 | - | 0 | - | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:134-138` |
| OutcomeUpdate | - | 3 | - | 0 | - | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:141-144` |
| EconRow | - | 19 | - | 0 | - | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:154-174` |
| Economics | - | 4 | - | 0 | - | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:177-181` |
| Insight | - | 5 | - | 0 | - | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:184-189` |
| Trace | - | 6 | - | 0 | - | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:192-198` |
| SpanContent | - | 4 | - | 0 | - | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:201-205` |

### Totals

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:26-34`. Specification note: Totals.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `tokens` | `TokenUsage` | yes |  | - | - |
| `cost` | `CostBreakdown` | yes |  | - | - |
| `reported_cost` | `float \| None` | yes |  | - | - |
| `events` | `int` | yes |  | - | - |
| `priced_events` | `int` | yes |  | - | - |
| `sessions` | `int` | yes |  | - | - |
| `first_event` | `datetime \| None` | yes |  | - | - |
| `last_event` | `datetime \| None` | yes |  | - | - |

No relations were extracted.

### SeriesPoint

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:37-45`. Specification note: SeriesPoint.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `day` | `date` | yes |  | - | - |
| `client` | `str` | yes |  | - | - |
| `provider` | `str` | yes |  | - | - |
| `model` | `str` | yes |  | - | - |
| `source` | `str` | yes |  | - | - |
| `cost` | `float` | yes |  | - | - |
| `tokens` | `int` | yes |  | - | - |
| `events` | `int` | yes |  | - | - |

No relations were extracted.

### SessionRow

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:48-74`. Specification note: SessionRow.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `session_id` | `str` | yes |  | - | - |
| `source` | `str` | yes |  | - | - |
| `client` | `str` | yes |  | - | - |
| `provider` | `str` | yes |  | - | - |
| `models` | `list[str]` | yes |  | - | - |
| `start_time` | `datetime` | yes |  | - | - |
| `end_time` | `datetime` | yes |  | - | - |
| `request_count` | `int` | yes |  | - | - |
| `tokens` | `TokenUsage \| None` | yes |  | - | - |
| `cost` | `CostBreakdown \| None` | yes |  | - | - |
| `reported_cost` | `float \| None` | yes |  | - | - |
| `cost_state` | `CostState` | yes |  | - | values of `CostState` |
| `cost_states` | `list[CostState]` | yes |  | - | - |
| `is_sidechain` | `bool` | yes |  | - | - |
| `has_sidechain` | `bool` | yes |  | - | - |
| `currency` | `str` | yes |  | - | - |
| `project` | `str \| None` | yes |  | - | - |
| `working_directory` | `str \| None` | yes |  | - | - |
| `repository` | `str \| None` | yes |  | - | - |
| `branch` | `str \| None` | yes |  | - | - |
| `machine` | `str` | yes |  | - | - |
| `raw_source` | `list[str]` | yes |  | - | - |
| `outcome` | `OutcomeLabel` | yes |  | - | values of `OutcomeLabel` |
| `traced` | `bool` | yes |  | - | - |
| `error_count` | `int` | yes |  | - | - |
| `title` | `str \| None` | yes |  | - | - |

No relations were extracted.

### UnknownModel

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:77-80`. Specification note: UnknownModel.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `model` | `str` | yes |  | - | - |
| `tokens` | `int` | yes |  | - | - |
| `events` | `int` | yes |  | - | - |

No relations were extracted.

### WarningInstance

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:100-111`. Specification note: WarningInstance.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `kind` | `str` | yes |  | - | - |
| `message` | `str` | yes |  | - | - |
| `source` | `str` | yes |  | - | - |
| `file` | `str \| None` | yes |  | - | - |
| `session_id` | `str \| None` | yes |  | - | - |
| `severity` | `WarningSeverity` | yes |  | - | values of `WarningSeverity` |
| `delta_tokens` | `int \| None` | yes |  | - | - |
| `delta_cost` | `float \| None` | yes |  | - | - |
| `likely_cause` | `str \| None` | yes |  | - | - |
| `auto_corrected` | `bool` | yes |  | - | - |

No relations were extracted.

### WarningGroup

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:115-127`. Specification note: WarningGroup.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `kind` | `str` | yes |  | - | - |
| `label` | `str` | yes |  | - | - |
| `count` | `int` | yes |  | - | - |
| `summary` | `str` | yes |  | - | - |
| `severity` | `WarningSeverity` | yes |  | - | values of `WarningSeverity` |
| `total_delta_tokens` | `int` | yes |  | - | - |
| `total_delta_cost` | `float` | yes |  | - | - |
| `worst_example` | `WarningInstance \| None` | yes |  | - | - |
| `affected_sessions` | `int` | yes |  | - | - |
| `instances` | `list[WarningInstance]` | yes |  | - | - |
| `warnings` | `list[str]` | yes |  | - | - |

No relations were extracted.

### Facets

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:454-459`. Specification note: Facets.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `states` | `dict[str, int]` | yes |  | - | - |
| `clients` | `dict[str, int]` | yes |  | - | - |
| `models` | `dict[str, int]` | yes |  | - | - |
| `projects` | `dict[str, int]` | yes |  | - | - |
| `outcomes` | `dict[str, int]` | yes |  | - | - |

No relations were extracted.

### Report

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:462-482`. Specification note: Report.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `generated_at` | `datetime` | yes |  | - | - |
| `rates_as_of` | `str` | yes |  | - | - |
| `rates_age_days` | `int \| None` | yes |  | - | - |
| `currency` | `str` | yes |  | - | - |
| `files_scanned` | `int` | yes |  | - | - |
| `files_in_slice` | `int` | yes |  | - | - |
| `totals` | `Totals` | yes |  | - | - |
| `by_client` | `list[Bucket]` | yes |  | - | - |
| `by_provider` | `list[Bucket]` | yes |  | - | - |
| `by_model` | `list[Bucket]` | yes |  | - | - |
| `by_project` | `list[Bucket]` | yes |  | - | - |
| `by_day` | `list[Bucket]` | yes |  | - | - |
| `series` | `list[SeriesPoint]` | yes |  | - | - |
| `sessions` | `list[SessionRow]` | yes |  | - | - |
| `unknown_models` | `list[UnknownModel]` | yes |  | - | - |
| `warnings` | `list[str]` | yes |  | - | - |
| `scan_warnings` | `list[str]` | yes |  | - | - |
| `warning_groups` | `list[WarningGroup]` | yes |  | - | - |
| `facets` | `Facets` | yes |  | - | - |
| `model_matches` | `dict[str, ModelMatch]` | yes |  | - | - |

No relations were extracted.

### ClientInfo

Defined at [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:86-88`. Specification note: ClientInfo.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `id` | `str` | yes |  | - | - |
| `label` | `str` | yes |  | - | - |

No relations were extracted.

### WarningSummary

Defined at [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:91-102`. Specification note: WarningSummary.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `critical` | `int` | yes |  | - | - |
| `caution` | `int` | yes |  | - | - |
| `info` | `int` | yes |  | - | - |
| `total_delta_cost` | `float` | yes |  | - | - |

No relations were extracted.

### Meta

Defined at [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:105-128`. Specification note: Meta.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `clients` | `list[ClientInfo]` | yes |  | - | - |
| `providers` | `list[str]` | yes |  | - | - |
| `models` | `list[str]` | yes |  | - | - |
| `projects` | `list[str]` | yes |  | - | - |
| `first_day` | `date \| None` | yes |  | - | - |
| `last_day` | `date \| None` | yes |  | - | - |
| `rates_as_of` | `str` | yes |  | - | - |
| `rates_age_days` | `int \| None` | yes |  | - | - |
| `currency` | `str` | yes |  | - | - |
| `files_scanned` | `int` | yes |  | - | - |
| `events` | `int` | yes |  | - | - |
| `warnings` | `list[str]` | yes |  | - | - |
| `warning_summary` | `WarningSummary` | yes |  | - | - |
| `session_warnings` | `dict[str, list[str]]` | yes |  | - | - |
| `sources` | `list[SourceInfo]` | yes |  | - | - |
| `client_last_seen` | `dict[str, str]` | yes |  | - | - |
| `model_last_seen` | `dict[str, str]` | yes |  | - | - |
| `project_last_seen` | `dict[str, str]` | yes |  | - | - |

No relations were extracted.

### AlertDecision

Defined at [[src/ai_usage_cost/cli.py]] `src/ai_usage_cost/cli.py:252-254`. Specification note: AlertDecision.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `fire` | `bool` | yes |  | - | - |
| `message` | `str` | yes |  | - | - |

No relations were extracted.

### Sample

Defined at [[src/ai_usage_cost/collect.py]] `src/ai_usage_cost/collect.py:49-56`. Specification note: Sample.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `machine` | `str` | yes |  | - | - |
| `sampled_at` | `datetime` | yes |  | - | - |
| `gpu_util` | `float \| None` | yes |  | - | - |
| `vram_used` | `int \| None` | yes |  | - | - |
| `vram_total` | `int \| None` | yes |  | - | - |
| `power_w` | `float \| None` | yes |  | - | - |
| `source` | `str` | yes |  | - | - |

No relations were extracted.

### samples

Defined at [[src/ai_usage_cost/collect.py]] `src/ai_usage_cost/collect.py:19-23`. Specification note: samples.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `machine` | `TEXT` | no |  | - | - |
| `sampled_at` | `TEXT` | no |  | - | - |
| `gpu_util` | `REAL` | yes |  | - | - |
| `vram_used` | `INTEGER` | yes |  | - | - |
| `vram_total` | `INTEGER` | yes |  | - | - |
| `power_w` | `REAL` | yes |  | - | - |
| `source` | `TEXT` | no |  | - | - |

No relations were extracted.

### apps

Defined at [[src/ai_usage_cost/demo.py]] `src/ai_usage_cost/demo.py:52-69`. Specification note: apps.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `id` | `INTEGER` | no | PK | - | - |
| `name` | `TEXT` | yes |  | - | - |
| `path` | `TEXT` | yes |  | - | - |
| `created_at` | `INTEGER` | yes |  | - | - |
| `updated_at` | `INTEGER` | yes |  | - | - |
| `github_org` | `TEXT` | yes |  | - | - |
| `github_repo` | `TEXT` | yes |  | - | - |
| `chat_context` | `TEXT` | yes |  | - | - |
| `github_branch` | `TEXT` | yes |  | - | - |
| `vercel_project_id` | `TEXT` | yes |  | - | - |
| `vercel_project_name` | `TEXT` | yes |  | - | - |
| `vercel_team_id` | `TEXT` | yes |  | - | - |
| `vercel_deployment_url` | `TEXT` | yes |  | - | - |
| `neon_project_id` | `TEXT` | yes |  | - | - |
| `neon_development_branch_id` | `TEXT` | yes |  | - | - |
| `neon_preview_branch_id` | `TEXT` | yes |  | - | - |

No relations were extracted.

### chats

Defined at [[src/ai_usage_cost/demo.py]] `src/ai_usage_cost/demo.py:71-77`. Specification note: chats.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `id` | `INTEGER` | no | PK | - | - |
| `app_id` | `INTEGER` | yes |  | - | - |
| `title` | `TEXT` | yes |  | - | - |
| `created_at` | `INTEGER` | yes |  | - | - |
| `initial_commit_hash` | `TEXT` | yes |  | - | - |

No relations were extracted.

### messages

Defined at [[src/ai_usage_cost/demo.py]] `src/ai_usage_cost/demo.py:79-87`. Specification note: messages.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `id` | `INTEGER` | no | PK | - | - |
| `chat_id` | `INTEGER` | yes |  | - | - |
| `role` | `TEXT` | yes |  | - | - |
| `content` | `TEXT` | yes |  | - | - |
| `created_at` | `INTEGER` | yes |  | - | - |
| `approval_state` | `TEXT` | yes |  | - | - |
| `commit_hash` | `TEXT` | yes |  | - | - |

No relations were extracted.

### TokenUsage

Defined at [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:12-43`. Specification note: TokenUsage.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `uncached_input` | `int` | yes |  | - | - |
| `cache_read` | `int` | yes |  | - | - |
| `cache_write_5m` | `int` | yes |  | - | - |
| `cache_write_1h` | `int` | yes |  | - | - |
| `output` | `int` | yes |  | - | - |
| `reasoning_output` | `int` | yes |  | - | - |

No relations were extracted.

### UsageEvent

Defined at [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:49-72`. Specification note: UsageEvent.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `source` | `str` | yes |  | - | - |
| `client` | `str` | yes |  | - | - |
| `provider` | `str \| None` | yes |  | - | - |
| `model` | `str \| None` | yes |  | - | - |
| `timestamp` | `datetime` | yes |  | - | - |
| `session_id` | `str` | yes |  | - | - |
| `request_id` | `str \| None` | yes |  | - | - |
| `tokens` | `TokenUsage \| None` | yes |  | - | - |
| `is_sidechain` | `bool` | yes |  | - | - |
| `tier` | `str` | yes |  | - | - |
| `project` | `str \| None` | yes |  | - | - |
| `working_directory` | `str \| None` | yes |  | - | - |
| `repository` | `str \| None` | yes |  | - | - |
| `branch` | `str \| None` | yes |  | - | - |
| `title` | `str \| None` | yes |  | - | - |
| `title_source` | `Literal['tool', 'summary', 'prompt', 'folder']` | yes |  | - | - |
| `machine` | `str` | yes |  | - | - |
| `source_file` | `str` | yes |  | - | - |
| `record_offset` | `int \| None` | yes |  | - | - |
| `raw` | `dict[str, RawScalar]` | yes |  | - | - |
| `reported_cost` | `float \| None` | yes |  | - | - |

No relations were extracted.

### CostBreakdown

Defined at [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:75-114`. Specification note: CostBreakdown.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `uncached_input` | `float` | yes |  | - | - |
| `cache_read` | `float` | yes |  | - | - |
| `cache_write` | `float` | yes |  | - | - |
| `output` | `float` | yes |  | - | - |
| `no_cache_equivalent` | `float` | yes |  | - | - |
| `estimated` | `bool` | yes |  | - | - |
| `tier_unpriced` | `bool` | yes |  | - | - |

No relations were extracted.

### PricedEvent

Defined at [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:117-120`. Specification note: PricedEvent.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `event` | `UsageEvent` | yes |  | - | - |
| `cost` | `CostBreakdown \| None` | yes |  | - | - |
| `state` | `CostState` | yes |  | - | values of `CostState` |

No relations were extracted.

### Bucket

Defined at [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:123-134`. Specification note: Bucket.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `key` | `str` | yes |  | - | - |
| `label` | `str` | yes |  | - | - |
| `tokens` | `TokenUsage` | yes |  | - | - |
| `cost` | `CostBreakdown` | yes |  | - | - |
| `events` | `int` | yes |  | - | - |
| `sessions` | `int` | yes |  | - | - |
| `reported_cost` | `float \| None` | yes |  | - | - |

No relations were extracted.

### SourceInfo

Defined at [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:31-41`. Specification note: SourceInfo.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `id` | `str` | yes |  | - | - |
| `label` | `str` | yes |  | - | - |
| `clients` | `list[str]` | yes |  | - | - |
| `token_data` | `TokenData` | yes |  | - | values of `TokenData` |
| `path` | `str` | yes |  | - | - |
| `root_hint` | `str` | yes |  | - | - |
| `detected` | `bool` | yes |  | - | - |
| `files` | `int` | yes |  | - | - |
| `capabilities` | `Capabilities` | yes |  | - | - |
| `experimental` | `bool` | yes |  | - | - |

No relations were extracted.

### Analysis

Defined at [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:45-63`. Specification note: Analysis.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `events` | `list[PricedEvent]` | yes |  | - | - |
| `table` | `RateTable` | yes |  | - | - |
| `files` | `int` | yes |  | - | - |
| `warnings` | `list[str]` | yes |  | - | - |
| `scan_warnings` | `list[str]` | yes |  | - | - |
| `sources` | `list[SourceInfo]` | yes |  | - | - |
| `session_flags` | `dict[tuple[str, str], tuple[bool, int, str]]` | yes |  | - | - |
| `db_path` | `Path \| None` | yes |  | - | - |
| `today` | `date \| None` | yes |  | - | - |

No relations were extracted.

### PriceSet

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:29-37`. Specification note: PriceSet.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `input` | `float` | yes |  | - | - |
| `output` | `float` | yes |  | - | - |
| `cache_read` | `float \| None` | yes |  | - | - |
| `cache_write_5m` | `float \| None` | yes |  | - | - |
| `cache_write_1h` | `float \| None` | yes |  | - | - |

No relations were extracted.

### Period

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:68-98`. Specification note: Period.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `model_config` | `ConfigDict` | yes |  | - | - |
| `from_` | `date \| None` | yes |  | - | - |
| `until` | `date \| None` | yes |  | - | - |
| `input` | `float \| None` | yes |  | - | - |
| `output` | `float \| None` | yes |  | - | - |
| `cache_read` | `float \| None` | yes |  | - | - |
| `cache_write_5m` | `float \| None` | yes |  | - | - |
| `cache_write_1h` | `float \| None` | yes |  | - | - |
| `variants` | `dict[str, PriceSet] \| None` | yes |  | - | - |
| `bands` | `list[Band] \| None` | yes |  | - | - |
| `peak` | `Peak \| None` | yes |  | - | - |

No relations were extracted.

### ProviderRules

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:101-106`. Specification note: ProviderRules.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `cache_read` | `float` | yes |  | - | - |
| `cache_write_5m` | `float` | yes |  | - | - |
| `cache_write_1h` | `float` | yes |  | - | - |
| `batch` | `float` | yes |  | - | - |
| `free` | `bool` | yes |  | - | - |

No relations were extracted.

### PartialRules

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:109-117`. Specification note: PartialRules.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `cache_read` | `float \| None` | yes |  | - | - |
| `cache_write_5m` | `float \| None` | yes |  | - | - |
| `cache_write_1h` | `float \| None` | yes |  | - | - |
| `batch` | `float \| None` | yes |  | - | - |
| `free` | `bool \| None` | yes |  | - | - |

No relations were extracted.

### Prefix

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:169-171`. Specification note: Prefix.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `prefix` | `str` | yes |  | - | - |
| `provider` | `str \| None` | yes |  | - | - |

No relations were extracted.

### ModelMatch

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:224-229`. Specification note: ModelMatch.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `match` | `str \| None` | yes |  | - | - |
| `kind` | `Literal['exact', 'suffix', 'estimated', 'none']` | yes |  | - | - |

No relations were extracted.

### UnpricedModel

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:232-242`. Specification note: UnpricedModel.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `match` | `str` | yes |  | - | - |
| `note` | `str` | yes |  | - | - |
| `status` | `Literal['watchlist', 'no_list_price'] \| None` | yes |  | - | - |

No relations were extracted.

### RateTable

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:252-372`. Specification note: RateTable.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `as_of` | `str` | yes |  | - | - |
| `currency` | `str` | yes |  | - | - |
| `units` | `str` | yes |  | - | - |
| `notes` | `list[str]` | yes |  | - | - |
| `prefixes` | `list[Prefix]` | yes |  | - | - |
| `providers` | `dict[str, ProviderRules]` | yes |  | - | - |
| `models` | `list[ModelRate]` | yes |  | - | - |
| `unpriced_models` | `list[UnpricedModel]` | yes |  | - | - |
| `_lookup_cache` | `dict[str, ModelRate \| None]` | yes |  | - | - |
| `_rules_cache` | `dict[str, ProviderRules]` | yes |  | - | - |
| `_prefix_cache` | `list[Prefix] \| None` | yes |  | - | - |

No relations were extracted.

### Config

Defined at [[src/ai_usage_cost/privacy.py]] `src/ai_usage_cost/privacy.py:52-57`. Specification note: Config.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `metadata_only` | `bool` | yes |  | - | - |
| `exclude_projects` | `list[str]` | yes |  | - | - |
| `max_content_bytes` | `int` | yes |  | - | - |
| `metadata_retention_days` | `int \| None` | yes |  | - | - |
| `content_retention_days` | `int \| None` | yes |  | - | - |

No relations were extracted.

### Source

Defined at [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:18-44`. Specification note: Source.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `id` | `str` | yes |  | - | - |
| `label` | `str` | yes |  | - | - |
| `clients` | `dict[str, str]` | yes |  | - | - |
| `default_roots` | `Callable[[], list[Path]]` | yes |  | - | - |
| `files` | `Callable[[Path], list[Path]]` | yes |  | - | - |
| `parse` | `Callable[[Path, list[str]], Iterator[UsageEvent]]` | yes |  | - | - |
| `token_data` | `TokenData` | yes |  | - | values of `TokenData` |
| `display_path` | `str` | yes |  | - | - |
| `spans` | `Callable[[Path, list[str]], Iterator[Span]] \| None` | yes |  | - | - |
| `capabilities` | `Capabilities` | yes |  | - | - |
| `experimental` | `bool` | yes |  | - | - |
| `parse_resume` | `Callable[[Path, list[str], int, str \| None], Iterator[UsageEvent]] \| None` | yes |  | - | - |

No relations were extracted.

### Spec

Defined at [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:82-87`. Specification note: Spec.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `source_id` | `str` | yes |  | - | - |
| `client` | `str` | yes |  | - | - |
| `ext_id` | `str` | yes |  | - | - |
| `tokens_in_inclusive` | `bool` | yes |  | - | - |
| `sdk` | `bool` | yes |  | - | - |

No relations were extracted.

### IngestSummary

Defined at [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:134-137`. Specification note: IngestSummary.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `files_parsed` | `int` | yes |  | - | - |
| `files_skipped` | `int` | yes |  | - | - |
| `warnings` | `list[str]` | yes |  | - | - |

No relations were extracted.

### requests

Defined at [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:23-85`. Specification note: requests.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `fingerprint` | `TEXT` | no | PK | - | - |
| `source` | `TEXT` | no |  | - | - |
| `client` | `TEXT` | no |  | - | - |
| `provider` | `TEXT` | yes |  | - | - |
| `model` | `TEXT` | yes |  | - | - |
| `session_id` | `TEXT` | no |  | - | - |
| `timestamp` | `TEXT` | no |  | - | - |
| `request_id` | `TEXT` | yes |  | - | - |
| `uncached_input` | `INTEGER` | yes |  | - | - |
| `cache_read` | `INTEGER` | yes |  | - | - |
| `cache_write_5m` | `INTEGER` | yes |  | - | - |
| `cache_write_1h` | `INTEGER` | yes |  | - | - |
| `output` | `INTEGER` | yes |  | - | - |
| `reasoning_output` | `INTEGER` | yes |  | - | - |
| `is_sidechain` | `INTEGER` | no |  | - | - |
| `tier` | `TEXT` | no |  | - | - |
| `project` | `TEXT` | yes |  | - | - |
| `working_directory` | `TEXT` | yes |  | - | - |
| `repository` | `TEXT` | yes |  | - | - |
| `branch` | `TEXT` | yes |  | - | - |
| `machine` | `TEXT` | no |  | - | - |
| `source_file` | `TEXT` | no |  | - | - |
| `raw` | `TEXT` | no |  | - | - |
| `title` | `TEXT` | yes |  | - | - |
| `title_source` | `TEXT` | no |  | `'folder'` | - |
| `reported_cost` | `REAL` | yes |  | - | - |

No relations were extracted.

### files

Defined at [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:36-82`. Specification note: files.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `path` | `TEXT` | no | PK | - | - |
| `source` | `TEXT` | no |  | - | - |
| `mtime` | `REAL` | no |  | - | - |
| `size` | `INTEGER` | no |  | - | - |
| `ingested_at` | `TEXT` | no |  | - | - |
| `warnings` | `TEXT` | no |  | - | - |
| `parser_version` | `INTEGER` | no |  | `0` | - |
| `ingested_offset` | `INTEGER` | no |  | `0` | - |
| `boundary_hash` | `TEXT` | yes |  | - | - |
| `title_seed` | `TEXT` | yes |  | - | - |

No relations were extracted.

### trace_events

Defined at [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:43-60`. Specification note: trace_events.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `span_id` | `TEXT` | no | PK | - | - |
| `parent_id` | `TEXT` | yes |  | - | - |
| `record_parent` | `TEXT` | yes |  | - | - |
| `source` | `TEXT` | no |  | - | - |
| `session_id` | `TEXT` | no |  | - | - |
| `turn_id` | `TEXT` | yes |  | - | - |
| `agent_id` | `TEXT` | yes |  | - | - |
| `is_sidechain` | `INTEGER` | no |  | - | - |
| `seq` | `INTEGER` | no |  | - | - |
| `kind` | `TEXT` | no |  | - | - |
| `name` | `TEXT` | yes |  | - | - |
| `model` | `TEXT` | yes |  | - | - |
| `status` | `TEXT` | no |  | - | - |
| `started_at` | `TEXT` | no |  | - | - |
| `ended_at` | `TEXT` | yes |  | - | - |
| `duration_ms` | `INTEGER` | yes |  | - | - |
| `duration_provenance` | `TEXT` | no |  | - | - |
| `ttft_ms` | `INTEGER` | yes |  | - | - |
| `uncached_input` | `INTEGER` | yes |  | - | - |
| `cache_read` | `INTEGER` | yes |  | - | - |
| `cache_write_5m` | `INTEGER` | yes |  | - | - |
| `cache_write_1h` | `INTEGER` | yes |  | - | - |
| `output` | `INTEGER` | yes |  | - | - |
| `reasoning_output` | `INTEGER` | yes |  | - | - |
| `tokens_provenance` | `TEXT` | no |  | - | - |
| `context_capacity` | `INTEGER` | yes |  | - | - |
| `capacity_provenance` | `TEXT` | no |  | - | - |
| `retry_attempt` | `INTEGER` | yes |  | - | - |
| `error` | `TEXT` | yes |  | - | - |
| `source_file` | `TEXT` | no |  | - | - |
| `record_offset` | `INTEGER` | no |  | - | - |
| `record_length` | `INTEGER` | no |  | - | - |
| `content_path` | `TEXT` | yes |  | - | - |
| `detail` | `TEXT` | no |  | - | - |

No relations were extracted.

### outcomes

Defined at [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:63-68`. Specification note: outcomes.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `source` | `TEXT` | no | PK | - | - |
| `session_id` | `TEXT` | no | PK | - | - |
| `outcome` | `TEXT` | no |  | - | - |
| `notes` | `TEXT` | no |  | - | - |
| `tags` | `TEXT` | no |  | - | - |
| `updated_at` | `TEXT` | no |  | - | - |

No relations were extracted.

### session_exclusions

Defined at [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:69-72`. Specification note: session_exclusions.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `source` | `TEXT` | no | PK | - | - |
| `session_id` | `TEXT` | no | PK | - | - |
| `excluded_at` | `TEXT` | no |  | - | - |

No relations were extracted.

### Span

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:55-101`. Specification note: Span.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `model_config` | `ConfigDict` | yes |  | - | - |
| `span_id` | `str` | yes |  | - | - |
| `parent_id` | `str \| None` | yes |  | - | - |
| `record_parent` | `str \| None` | yes |  | - | - |
| `source` | `str` | yes |  | - | - |
| `session_id` | `str` | yes |  | - | - |
| `turn_id` | `str \| None` | yes |  | - | - |
| `agent_id` | `str \| None` | yes |  | - | - |
| `is_sidechain` | `bool` | yes |  | - | - |
| `seq` | `int` | yes |  | - | - |
| `kind` | `SpanKind` | yes |  | - | values of `SpanKind` |
| `name` | `str \| None` | yes |  | - | - |
| `model` | `str \| None` | yes |  | - | - |
| `status` | `SpanStatus` | yes |  | - | values of `SpanStatus` |
| `started_at` | `datetime` | yes |  | - | - |
| `ended_at` | `datetime \| None` | yes |  | - | - |
| `duration_ms` | `int \| None` | yes |  | - | - |
| `duration_provenance` | `Provenance` | yes |  | - | values of `Provenance` |
| `ttft_ms` | `int \| None` | yes |  | - | - |
| `tokens` | `TokenUsage \| None` | yes |  | - | - |
| `tokens_provenance` | `Provenance` | yes |  | - | values of `Provenance` |
| `context_capacity` | `int \| None` | yes |  | - | - |
| `capacity_provenance` | `Provenance` | yes |  | - | values of `Provenance` |
| `retry_attempt` | `int \| None` | yes |  | - | - |
| `error` | `str \| None` | yes |  | - | - |
| `source_file` | `str` | yes |  | - | - |
| `record_offset` | `int` | yes |  | - | - |
| `record_length` | `int` | yes |  | - | - |
| `content_path` | `str \| None` | yes |  | - | - |
| `detail` | `dict[str, RawScalar]` | yes |  | - | - |

No relations were extracted.

### Capabilities

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:104-109`. Specification note: Capabilities.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `trace` | `Provenance` | yes |  | - | values of `Provenance` |
| `tokens` | `Provenance` | yes |  | - | values of `Provenance` |
| `cost` | `Provenance` | yes |  | - | values of `Provenance` |
| `context` | `Provenance` | yes |  | - | values of `Provenance` |
| `latency` | `Provenance` | yes |  | - | values of `Provenance` |

No relations were extracted.

### ContextSnapshot

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:112-131`. Specification note: ContextSnapshot.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `span_id` | `str` | yes |  | - | - |
| `model` | `str \| None` | yes |  | - | - |
| `started_at` | `datetime` | yes |  | - | - |
| `input_total` | `int \| None` | yes |  | - | - |
| `tokens_provenance` | `Provenance` | yes |  | - | values of `Provenance` |
| `capacity` | `int \| None` | yes |  | - | - |
| `capacity_provenance` | `Provenance` | yes |  | - | values of `Provenance` |
| `occupancy` | `float \| None` | yes |  | - | - |
| `occupancy_provenance` | `Provenance` | yes |  | - | values of `Provenance` |
| `delta_input` | `int \| None` | yes |  | - | - |
| `added_span_ids` | `list[str]` | yes |  | - | - |
| `compacted_before` | `bool` | yes |  | - | - |
| `composition` | `dict[str, float]` | yes |  | - | - |
| `model_config` | `ConfigDict` | yes |  | - | - |

No relations were extracted.

### OutcomeSignals

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:134-138`. Specification note: OutcomeSignals.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `aborted_turns` | `int` | yes |  | - | - |
| `interrupted_tools` | `int` | yes |  | - | - |
| `errors` | `int` | yes |  | - | - |
| `last_turn_status` | `SpanStatus` | yes |  | - | values of `SpanStatus` |

No relations were extracted.

### OutcomeUpdate

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:141-144`. Specification note: OutcomeUpdate.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `outcome` | `OutcomeLabel` | yes |  | - | values of `OutcomeLabel` |
| `notes` | `str` | yes |  | - | - |
| `tags` | `list[str]` | yes |  | - | - |

No relations were extracted.

### EconRow

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:154-174`. Specification note: EconRow.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `key` | `str` | yes |  | - | - |
| `label` | `str \| None` | yes |  | - | - |
| `ordinal` | `int \| None` | yes |  | - | - |
| `started_at` | `datetime \| None` | yes |  | - | - |
| `is_sidechain` | `bool` | yes |  | - | - |
| `model_calls` | `int` | yes |  | - | - |
| `tool_calls` | `int` | yes |  | - | - |
| `tokens` | `TokenUsage \| None` | yes |  | - | - |
| `tokens_provenance` | `Provenance` | yes |  | - | values of `Provenance` |
| `cost` | `CostBreakdown \| None` | yes |  | - | - |
| `cost_state` | `CostState` | yes |  | - | values of `CostState` |
| `duration_ms` | `int \| None` | yes |  | - | - |
| `duration_provenance` | `Provenance` | yes |  | - | values of `Provenance` |
| `errors` | `int` | yes |  | - | - |
| `retries` | `int \| None` | yes |  | - | - |
| `amplification` | `float \| None` | yes |  | - | - |
| `cache_hit_ratio` | `float \| None` | yes |  | - | - |
| `tokens_per_second` | `float \| None` | yes |  | - | - |
| `model_config` | `ConfigDict` | yes |  | - | - |

No relations were extracted.

### Economics

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:177-181`. Specification note: Economics.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `totals` | `EconRow` | yes |  | - | - |
| `by_turn` | `list[EconRow]` | yes |  | - | - |
| `by_model` | `list[EconRow]` | yes |  | - | - |
| `by_tool` | `list[EconRow]` | yes |  | - | - |

No relations were extracted.

### Insight

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:184-189`. Specification note: Insight.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `kind` | `str` | yes |  | - | - |
| `severity` | `Literal['info', 'warning', 'critical']` | yes |  | - | - |
| `span_id` | `str` | yes |  | - | - |
| `message` | `str` | yes |  | - | - |
| `count` | `int` | yes |  | - | - |

No relations were extracted.

### Trace

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:192-198`. Specification note: Trace.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `source` | `str` | yes |  | - | - |
| `session_id` | `str` | yes |  | - | - |
| `capabilities` | `Capabilities` | yes |  | - | - |
| `spans` | `list[Span]` | yes |  | - | - |
| `outcome` | `Outcome \| None` | yes |  | - | - |
| `insights` | `list[Insight]` | yes |  | - | - |

No relations were extracted.

### SpanContent

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:201-205`. Specification note: SpanContent.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `span_id` | `str` | yes |  | - | - |
| `content` | `str` | yes |  | - | - |
| `truncated` | `bool` | yes |  | - | - |
| `redactions` | `int` | yes |  | - | - |

No relations were extracted.

### Enumerated values

| Type | Values | Code |
|---|---|---|
| `CostState` | `priced`, `free`, `unpriced`, `unavailable` | [[web/src/api.ts]] `web/src/api.ts:61` |
| `OutcomeLabel` | `successful`, `partial`, `failed`, `abandoned`, `unrated` | [[web/src/api.ts]] `web/src/api.ts:82` |
| `Provenance` | `measured`, `derived`, `estimated`, `inferred`, `unavailable` | [[web/src/api.ts]] `web/src/api.ts:63` |
| `SpanKind` | `turn`, `user`, `assistant`, `reasoning`, `model_call`, `tool_call`, `tool_result`, `retrieval`, `compaction`, `error`, `subagent` | [[web/src/api.ts]] `web/src/api.ts:67-78` |
| `SpanStatus` | `ok`, `error`, `interrupted`, `aborted`, `running`, `unknown` | [[web/src/api.ts]] `web/src/api.ts:80` |
| `TokenData` | `full`, `session` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:14` |
| `WarningSeverity` | `info`, `caution`, `critical` | [[web/src/api.ts]] `web/src/api.ts:289` |
%% generated:chunk-entities end %%
