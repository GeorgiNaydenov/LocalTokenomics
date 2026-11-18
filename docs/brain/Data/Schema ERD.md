---
title: Schema ERD
aliases: []
tags: [data, erd, generated]
area: data
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
---

# Schema ERD

Entities and relations found in the code, each with its definition site.

%% generated:schema start (do not edit; run brain docs generate) %%
### AlertDecision

Defined at [[src/ai_usage_cost/cli.py]] `src/ai_usage_cost/cli.py:252`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `fire` | `bool` | yes |  |
| `message` | `str` | yes |  |

### Analysis

Defined at [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:45`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `events` | `list[PricedEvent]` | yes |  |
| `table` | `RateTable` | yes |  |
| `files` | `int` | yes |  |
| `warnings` | `list[str]` | yes |  |
| `scan_warnings` | `list[str]` | yes |  |
| `sources` | `list[SourceInfo]` | yes |  |
| `session_flags` | `dict[tuple[str, str], tuple[bool, int, str]]` | yes |  |
| `db_path` | `Path \| None` | yes |  |
| `today` | `date \| None` | yes |  |

### Bucket

Defined at [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:123`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `key` | `str` | yes |  |
| `label` | `str` | yes |  |
| `tokens` | `TokenUsage` | yes |  |
| `cost` | `CostBreakdown` | yes |  |
| `events` | `int` | yes |  |
| `sessions` | `int` | yes |  |
| `reported_cost` | `float \| None` | yes |  |

### Capabilities

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:104`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `trace` | `Provenance` | yes |  |
| `tokens` | `Provenance` | yes |  |
| `cost` | `Provenance` | yes |  |
| `context` | `Provenance` | yes |  |
| `latency` | `Provenance` | yes |  |

### ClientInfo

Defined at [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:86`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `str` | yes |  |
| `label` | `str` | yes |  |

### Config

Defined at [[src/ai_usage_cost/privacy.py]] `src/ai_usage_cost/privacy.py:52`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `metadata_only` | `bool` | yes |  |
| `exclude_projects` | `list[str]` | yes |  |
| `max_content_bytes` | `int` | yes |  |
| `metadata_retention_days` | `int \| None` | yes |  |
| `content_retention_days` | `int \| None` | yes |  |

### ContextSnapshot

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:112`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `span_id` | `str` | yes |  |
| `model` | `str \| None` | yes |  |
| `started_at` | `datetime` | yes |  |
| `input_total` | `int \| None` | yes |  |
| `tokens_provenance` | `Provenance` | yes |  |
| `capacity` | `int \| None` | yes |  |
| `capacity_provenance` | `Provenance` | yes |  |
| `occupancy` | `float \| None` | yes |  |
| `occupancy_provenance` | `Provenance` | yes |  |
| `delta_input` | `int \| None` | yes |  |
| `added_span_ids` | `list[str]` | yes |  |
| `compacted_before` | `bool` | yes |  |
| `composition` | `dict[str, float]` | yes |  |
| `model_config` | `ConfigDict` | yes |  |

### CostBreakdown

Defined at [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:75`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `uncached_input` | `float` | yes |  |
| `cache_read` | `float` | yes |  |
| `cache_write` | `float` | yes |  |
| `output` | `float` | yes |  |
| `no_cache_equivalent` | `float` | yes |  |
| `estimated` | `bool` | yes |  |
| `tier_unpriced` | `bool` | yes |  |

### EconRow

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:154`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `key` | `str` | yes |  |
| `label` | `str \| None` | yes |  |
| `ordinal` | `int \| None` | yes |  |
| `started_at` | `datetime \| None` | yes |  |
| `is_sidechain` | `bool` | yes |  |
| `model_calls` | `int` | yes |  |
| `tool_calls` | `int` | yes |  |
| `tokens` | `TokenUsage \| None` | yes |  |
| `tokens_provenance` | `Provenance` | yes |  |
| `cost` | `CostBreakdown \| None` | yes |  |
| `cost_state` | `CostState` | yes |  |
| `duration_ms` | `int \| None` | yes |  |
| `duration_provenance` | `Provenance` | yes |  |
| `errors` | `int` | yes |  |
| `retries` | `int \| None` | yes |  |
| `amplification` | `float \| None` | yes |  |
| `cache_hit_ratio` | `float \| None` | yes |  |
| `tokens_per_second` | `float \| None` | yes |  |
| `model_config` | `ConfigDict` | yes |  |

### Economics

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:177`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `totals` | `EconRow` | yes |  |
| `by_turn` | `list[EconRow]` | yes |  |
| `by_model` | `list[EconRow]` | yes |  |
| `by_tool` | `list[EconRow]` | yes |  |

### Facets

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:454`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `states` | `dict[str, int]` | yes |  |
| `clients` | `dict[str, int]` | yes |  |
| `models` | `dict[str, int]` | yes |  |
| `projects` | `dict[str, int]` | yes |  |
| `outcomes` | `dict[str, int]` | yes |  |

### IngestSummary

Defined at [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:134`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `files_parsed` | `int` | yes |  |
| `files_skipped` | `int` | yes |  |
| `warnings` | `list[str]` | yes |  |

### Insight

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:184`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `kind` | `str` | yes |  |
| `severity` | `Literal['info', 'warning', 'critical']` | yes |  |
| `span_id` | `str` | yes |  |
| `message` | `str` | yes |  |
| `count` | `int` | yes |  |

### ItemTable

Defined at [[tests/test_windsurf.py]] `tests/test_windsurf.py:52`; table `ItemTable`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `value` | `TEXT` | yes |  |

### ItemTable

Defined at [[tests/fixtures/cursor/no_table.sql]] `tests/fixtures/cursor/no_table.sql:1`; table `ItemTable`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `value` | `TEXT` | yes |  |

### ItemTable

Defined at [[tests/fixtures/windsurf/basic.sql]] `tests/fixtures/windsurf/basic.sql:1`; table `ItemTable`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `value` | `TEXT` | yes |  |

### ItemTable

Defined at [[tests/fixtures/windsurf/empty.sql]] `tests/fixtures/windsurf/empty.sql:1`; table `ItemTable`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `value` | `TEXT` | yes |  |

### ItemTable

Defined at [[tests/fixtures/windsurf/malformed.sql]] `tests/fixtures/windsurf/malformed.sql:1`; table `ItemTable`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `value` | `TEXT` | yes |  |

### ItemTable

Defined at [[tests/fixtures/windsurf/no_chat_key.sql]] `tests/fixtures/windsurf/no_chat_key.sql:1`; table `ItemTable`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `value` | `TEXT` | yes |  |

### Meta

Defined at [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:105`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `clients` | `list[ClientInfo]` | yes |  |
| `providers` | `list[str]` | yes |  |
| `models` | `list[str]` | yes |  |
| `projects` | `list[str]` | yes |  |
| `first_day` | `date \| None` | yes |  |
| `last_day` | `date \| None` | yes |  |
| `rates_as_of` | `str` | yes |  |
| `rates_age_days` | `int \| None` | yes |  |
| `currency` | `str` | yes |  |
| `files_scanned` | `int` | yes |  |
| `events` | `int` | yes |  |
| `warnings` | `list[str]` | yes |  |
| `warning_summary` | `WarningSummary` | yes |  |
| `session_warnings` | `dict[str, list[str]]` | yes |  |
| `sources` | `list[SourceInfo]` | yes |  |
| `client_last_seen` | `dict[str, str]` | yes |  |
| `model_last_seen` | `dict[str, str]` | yes |  |
| `project_last_seen` | `dict[str, str]` | yes |  |

### ModelMatch

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:224`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `match` | `str \| None` | yes |  |
| `kind` | `Literal['exact', 'suffix', 'estimated', 'none']` | yes |  |

### OutcomeSignals

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:134`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `aborted_turns` | `int` | yes |  |
| `interrupted_tools` | `int` | yes |  |
| `errors` | `int` | yes |  |
| `last_turn_status` | `SpanStatus` | yes |  |

### OutcomeUpdate

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:141`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `outcome` | `OutcomeLabel` | yes |  |
| `notes` | `str` | yes |  |
| `tags` | `list[str]` | yes |  |

### PartialRules

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:109`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `cache_read` | `float \| None` | yes |  |
| `cache_write_5m` | `float \| None` | yes |  |
| `cache_write_1h` | `float \| None` | yes |  |
| `batch` | `float \| None` | yes |  |
| `free` | `bool \| None` | yes |  |

### Period

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:68`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `model_config` | `ConfigDict` | yes |  |
| `from_` | `date \| None` | yes |  |
| `until` | `date \| None` | yes |  |
| `input` | `float \| None` | yes |  |
| `output` | `float \| None` | yes |  |
| `cache_read` | `float \| None` | yes |  |
| `cache_write_5m` | `float \| None` | yes |  |
| `cache_write_1h` | `float \| None` | yes |  |
| `variants` | `dict[str, PriceSet] \| None` | yes |  |
| `bands` | `list[Band] \| None` | yes |  |
| `peak` | `Peak \| None` | yes |  |

### Prefix

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:169`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `prefix` | `str` | yes |  |
| `provider` | `str \| None` | yes |  |

### PriceSet

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:29`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `input` | `float` | yes |  |
| `output` | `float` | yes |  |
| `cache_read` | `float \| None` | yes |  |
| `cache_write_5m` | `float \| None` | yes |  |
| `cache_write_1h` | `float \| None` | yes |  |

### PricedEvent

Defined at [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:117`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `event` | `UsageEvent` | yes |  |
| `cost` | `CostBreakdown \| None` | yes |  |
| `state` | `CostState` | yes |  |

### ProviderRules

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:101`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `cache_read` | `float` | yes |  |
| `cache_write_5m` | `float` | yes |  |
| `cache_write_1h` | `float` | yes |  |
| `batch` | `float` | yes |  |
| `free` | `bool` | yes |  |

### RateTable

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:252`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `as_of` | `str` | yes |  |
| `currency` | `str` | yes |  |
| `units` | `str` | yes |  |
| `notes` | `list[str]` | yes |  |
| `prefixes` | `list[Prefix]` | yes |  |
| `providers` | `dict[str, ProviderRules]` | yes |  |
| `models` | `list[ModelRate]` | yes |  |
| `unpriced_models` | `list[UnpricedModel]` | yes |  |
| `_lookup_cache` | `dict[str, ModelRate \| None]` | yes |  |
| `_rules_cache` | `dict[str, ProviderRules]` | yes |  |
| `_prefix_cache` | `list[Prefix] \| None` | yes |  |

### Report

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:462`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `generated_at` | `datetime` | yes |  |
| `rates_as_of` | `str` | yes |  |
| `rates_age_days` | `int \| None` | yes |  |
| `currency` | `str` | yes |  |
| `files_scanned` | `int` | yes |  |
| `files_in_slice` | `int` | yes |  |
| `totals` | `Totals` | yes |  |
| `by_client` | `list[Bucket]` | yes |  |
| `by_provider` | `list[Bucket]` | yes |  |
| `by_model` | `list[Bucket]` | yes |  |
| `by_project` | `list[Bucket]` | yes |  |
| `by_day` | `list[Bucket]` | yes |  |
| `series` | `list[SeriesPoint]` | yes |  |
| `sessions` | `list[SessionRow]` | yes |  |
| `unknown_models` | `list[UnknownModel]` | yes |  |
| `warnings` | `list[str]` | yes |  |
| `scan_warnings` | `list[str]` | yes |  |
| `warning_groups` | `list[WarningGroup]` | yes |  |
| `facets` | `Facets` | yes |  |
| `model_matches` | `dict[str, ModelMatch]` | yes |  |

### Sample

Defined at [[src/ai_usage_cost/collect.py]] `src/ai_usage_cost/collect.py:49`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `machine` | `str` | yes |  |
| `sampled_at` | `datetime` | yes |  |
| `gpu_util` | `float \| None` | yes |  |
| `vram_used` | `int \| None` | yes |  |
| `vram_total` | `int \| None` | yes |  |
| `power_w` | `float \| None` | yes |  |
| `source` | `str` | yes |  |

### Scanned

Defined at [[tests/test_codex.py]] `tests/test_codex.py:20`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `events` | `list[UsageEvent]` | yes |  |
| `warnings` | `list[str]` | yes |  |

### Scanned

Defined at [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:23`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `events` | `list[UsageEvent]` | yes |  |
| `warnings` | `list[str]` | yes |  |

### Scanned

Defined at [[tests/test_grok_build.py]] `tests/test_grok_build.py:15`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `events` | `list[UsageEvent]` | yes |  |
| `warnings` | `list[str]` | yes |  |

### Scanned

Defined at [[tests/test_muse_code.py]] `tests/test_muse_code.py:22`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `events` | `list[UsageEvent]` | yes |  |
| `warnings` | `list[str]` | yes |  |

### Scanned

Defined at [[tests/test_trace_codex.py]] `tests/test_trace_codex.py:28`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `spans` | `list[Span]` | yes |  |
| `warnings` | `list[str]` | yes |  |

### SeriesPoint

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:37`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `day` | `date` | yes |  |
| `client` | `str` | yes |  |
| `provider` | `str` | yes |  |
| `model` | `str` | yes |  |
| `source` | `str` | yes |  |
| `cost` | `float` | yes |  |
| `tokens` | `int` | yes |  |
| `events` | `int` | yes |  |

### SessionRow

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:48`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `session_id` | `str` | yes |  |
| `source` | `str` | yes |  |
| `client` | `str` | yes |  |
| `provider` | `str` | yes |  |
| `models` | `list[str]` | yes |  |
| `start_time` | `datetime` | yes |  |
| `end_time` | `datetime` | yes |  |
| `request_count` | `int` | yes |  |
| `tokens` | `TokenUsage \| None` | yes |  |
| `cost` | `CostBreakdown \| None` | yes |  |
| `reported_cost` | `float \| None` | yes |  |
| `cost_state` | `CostState` | yes |  |
| `cost_states` | `list[CostState]` | yes |  |
| `is_sidechain` | `bool` | yes |  |
| `has_sidechain` | `bool` | yes |  |
| `currency` | `str` | yes |  |
| `project` | `str \| None` | yes |  |
| `working_directory` | `str \| None` | yes |  |
| `repository` | `str \| None` | yes |  |
| `branch` | `str \| None` | yes |  |
| `machine` | `str` | yes |  |
| `raw_source` | `list[str]` | yes |  |
| `outcome` | `OutcomeLabel` | yes |  |
| `traced` | `bool` | yes |  |
| `error_count` | `int` | yes |  |
| `title` | `str \| None` | yes |  |

### Source

Defined at [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:18`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `str` | yes |  |
| `label` | `str` | yes |  |
| `clients` | `dict[str, str]` | yes |  |
| `default_roots` | `Callable[[], list[Path]]` | yes |  |
| `files` | `Callable[[Path], list[Path]]` | yes |  |
| `parse` | `Callable[[Path, list[str]], Iterator[UsageEvent]]` | yes |  |
| `token_data` | `TokenData` | yes |  |
| `display_path` | `str` | yes |  |
| `spans` | `Callable[[Path, list[str]], Iterator[Span]] \| None` | yes |  |
| `capabilities` | `Capabilities` | yes |  |
| `experimental` | `bool` | yes |  |
| `parse_resume` | `Callable[[Path, list[str], int, str \| None], Iterator[UsageEvent]] \| None` | yes |  |

### SourceInfo

Defined at [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:31`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `str` | yes |  |
| `label` | `str` | yes |  |
| `clients` | `list[str]` | yes |  |
| `token_data` | `TokenData` | yes |  |
| `path` | `str` | yes |  |
| `root_hint` | `str` | yes |  |
| `detected` | `bool` | yes |  |
| `files` | `int` | yes |  |
| `capabilities` | `Capabilities` | yes |  |
| `experimental` | `bool` | yes |  |

### Span

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:55`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `model_config` | `ConfigDict` | yes |  |
| `span_id` | `str` | yes |  |
| `parent_id` | `str \| None` | yes |  |
| `record_parent` | `str \| None` | yes |  |
| `source` | `str` | yes |  |
| `session_id` | `str` | yes |  |
| `turn_id` | `str \| None` | yes |  |
| `agent_id` | `str \| None` | yes |  |
| `is_sidechain` | `bool` | yes |  |
| `seq` | `int` | yes |  |
| `kind` | `SpanKind` | yes |  |
| `name` | `str \| None` | yes |  |
| `model` | `str \| None` | yes |  |
| `status` | `SpanStatus` | yes |  |
| `started_at` | `datetime` | yes |  |
| `ended_at` | `datetime \| None` | yes |  |
| `duration_ms` | `int \| None` | yes |  |
| `duration_provenance` | `Provenance` | yes |  |
| `ttft_ms` | `int \| None` | yes |  |
| `tokens` | `TokenUsage \| None` | yes |  |
| `tokens_provenance` | `Provenance` | yes |  |
| `context_capacity` | `int \| None` | yes |  |
| `capacity_provenance` | `Provenance` | yes |  |
| `retry_attempt` | `int \| None` | yes |  |
| `error` | `str \| None` | yes |  |
| `source_file` | `str` | yes |  |
| `record_offset` | `int` | yes |  |
| `record_length` | `int` | yes |  |
| `content_path` | `str \| None` | yes |  |
| `detail` | `dict[str, RawScalar]` | yes |  |

### SpanContent

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:201`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `span_id` | `str` | yes |  |
| `content` | `str` | yes |  |
| `truncated` | `bool` | yes |  |
| `redactions` | `int` | yes |  |

### Spec

Defined at [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:82`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `source_id` | `str` | yes |  |
| `client` | `str` | yes |  |
| `ext_id` | `str` | yes |  |
| `tokens_in_inclusive` | `bool` | yes |  |
| `sdk` | `bool` | yes |  |

### TokenUsage

Defined at [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:12`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `uncached_input` | `int` | yes |  |
| `cache_read` | `int` | yes |  |
| `cache_write_5m` | `int` | yes |  |
| `cache_write_1h` | `int` | yes |  |
| `output` | `int` | yes |  |
| `reasoning_output` | `int` | yes |  |

### Totals

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:26`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `tokens` | `TokenUsage` | yes |  |
| `cost` | `CostBreakdown` | yes |  |
| `reported_cost` | `float \| None` | yes |  |
| `events` | `int` | yes |  |
| `priced_events` | `int` | yes |  |
| `sessions` | `int` | yes |  |
| `first_event` | `datetime \| None` | yes |  |
| `last_event` | `datetime \| None` | yes |  |

### Trace

Defined at [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:192`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `source` | `str` | yes |  |
| `session_id` | `str` | yes |  |
| `capabilities` | `Capabilities` | yes |  |
| `spans` | `list[Span]` | yes |  |
| `outcome` | `Outcome \| None` | yes |  |
| `insights` | `list[Insight]` | yes |  |

### UnknownModel

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:77`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `model` | `str` | yes |  |
| `tokens` | `int` | yes |  |
| `events` | `int` | yes |  |

### UnpricedModel

Defined at [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:232`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `match` | `str` | yes |  |
| `note` | `str` | yes |  |
| `status` | `Literal['watchlist', 'no_list_price'] \| None` | yes |  |

### UsageEvent

Defined at [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:49`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `source` | `str` | yes |  |
| `client` | `str` | yes |  |
| `provider` | `str \| None` | yes |  |
| `model` | `str \| None` | yes |  |
| `timestamp` | `datetime` | yes |  |
| `session_id` | `str` | yes |  |
| `request_id` | `str \| None` | yes |  |
| `tokens` | `TokenUsage \| None` | yes |  |
| `is_sidechain` | `bool` | yes |  |
| `tier` | `str` | yes |  |
| `project` | `str \| None` | yes |  |
| `working_directory` | `str \| None` | yes |  |
| `repository` | `str \| None` | yes |  |
| `branch` | `str \| None` | yes |  |
| `title` | `str \| None` | yes |  |
| `title_source` | `Literal['tool', 'summary', 'prompt', 'folder']` | yes |  |
| `machine` | `str` | yes |  |
| `source_file` | `str` | yes |  |
| `record_offset` | `int \| None` | yes |  |
| `raw` | `dict[str, RawScalar]` | yes |  |
| `reported_cost` | `float \| None` | yes |  |

### WarningGroup

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:115`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `kind` | `str` | yes |  |
| `label` | `str` | yes |  |
| `count` | `int` | yes |  |
| `summary` | `str` | yes |  |
| `severity` | `WarningSeverity` | yes |  |
| `total_delta_tokens` | `int` | yes |  |
| `total_delta_cost` | `float` | yes |  |
| `worst_example` | `WarningInstance \| None` | yes |  |
| `affected_sessions` | `int` | yes |  |
| `instances` | `list[WarningInstance]` | yes |  |
| `warnings` | `list[str]` | yes |  |

### WarningInstance

Defined at [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:100`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `kind` | `str` | yes |  |
| `message` | `str` | yes |  |
| `source` | `str` | yes |  |
| `file` | `str \| None` | yes |  |
| `session_id` | `str \| None` | yes |  |
| `severity` | `WarningSeverity` | yes |  |
| `delta_tokens` | `int \| None` | yes |  |
| `delta_cost` | `float \| None` | yes |  |
| `likely_cause` | `str \| None` | yes |  |
| `auto_corrected` | `bool` | yes |  |

### WarningSummary

Defined at [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:91`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `critical` | `int` | yes |  |
| `caution` | `int` | yes |  |
| `info` | `int` | yes |  |
| `total_delta_cost` | `float` | yes |  |

### apps

Defined at [[src/ai_usage_cost/demo.py]] `src/ai_usage_cost/demo.py:52`; table `apps`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `INTEGER` | no | PK |
| `name` | `TEXT` | yes |  |
| `path` | `TEXT` | yes |  |
| `created_at` | `INTEGER` | yes |  |
| `updated_at` | `INTEGER` | yes |  |
| `github_org` | `TEXT` | yes |  |
| `github_repo` | `TEXT` | yes |  |
| `chat_context` | `TEXT` | yes |  |
| `github_branch` | `TEXT` | yes |  |
| `vercel_project_id` | `TEXT` | yes |  |
| `vercel_project_name` | `TEXT` | yes |  |
| `vercel_team_id` | `TEXT` | yes |  |
| `vercel_deployment_url` | `TEXT` | yes |  |
| `neon_project_id` | `TEXT` | yes |  |
| `neon_development_branch_id` | `TEXT` | yes |  |
| `neon_preview_branch_id` | `TEXT` | yes |  |

### apps

Defined at [[tests/fixtures/dyad/basic.sql]] `tests/fixtures/dyad/basic.sql:1`; table `apps`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `INTEGER` | no | PK |
| `name` | `TEXT` | yes |  |
| `path` | `TEXT` | yes |  |
| `created_at` | `INTEGER` | yes |  |
| `updated_at` | `INTEGER` | yes |  |
| `github_org` | `TEXT` | yes |  |
| `github_repo` | `TEXT` | yes |  |
| `chat_context` | `TEXT` | yes |  |
| `github_branch` | `TEXT` | yes |  |
| `vercel_project_id` | `TEXT` | yes |  |
| `vercel_project_name` | `TEXT` | yes |  |
| `vercel_team_id` | `TEXT` | yes |  |
| `vercel_deployment_url` | `TEXT` | yes |  |
| `neon_project_id` | `TEXT` | yes |  |
| `neon_development_branch_id` | `TEXT` | yes |  |
| `neon_preview_branch_id` | `TEXT` | yes |  |

### apps

Defined at [[tests/fixtures/dyad/null_title.sql]] `tests/fixtures/dyad/null_title.sql:1`; table `apps`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `INTEGER` | no | PK |
| `name` | `TEXT` | yes |  |
| `path` | `TEXT` | yes |  |
| `created_at` | `INTEGER` | yes |  |
| `updated_at` | `INTEGER` | yes |  |
| `github_org` | `TEXT` | yes |  |
| `github_repo` | `TEXT` | yes |  |
| `chat_context` | `TEXT` | yes |  |
| `github_branch` | `TEXT` | yes |  |
| `vercel_project_id` | `TEXT` | yes |  |
| `vercel_project_name` | `TEXT` | yes |  |
| `vercel_team_id` | `TEXT` | yes |  |
| `vercel_deployment_url` | `TEXT` | yes |  |
| `neon_project_id` | `TEXT` | yes |  |
| `neon_development_branch_id` | `TEXT` | yes |  |
| `neon_preview_branch_id` | `TEXT` | yes |  |

### chats

Defined at [[src/ai_usage_cost/demo.py]] `src/ai_usage_cost/demo.py:71`; table `chats`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `INTEGER` | no | PK |
| `app_id` | `INTEGER` | yes |  |
| `title` | `TEXT` | yes |  |
| `created_at` | `INTEGER` | yes |  |
| `initial_commit_hash` | `TEXT` | yes |  |

### chats

Defined at [[tests/fixtures/dyad/basic.sql]] `tests/fixtures/dyad/basic.sql:20`; table `chats`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `INTEGER` | no | PK |
| `app_id` | `INTEGER` | yes |  |
| `title` | `TEXT` | yes |  |
| `created_at` | `INTEGER` | yes |  |
| `initial_commit_hash` | `TEXT` | yes |  |

### chats

Defined at [[tests/fixtures/dyad/null_title.sql]] `tests/fixtures/dyad/null_title.sql:20`; table `chats`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `INTEGER` | no | PK |
| `app_id` | `INTEGER` | yes |  |
| `title` | `TEXT` | yes |  |
| `created_at` | `INTEGER` | yes |  |
| `initial_commit_hash` | `TEXT` | yes |  |

### cursorDiskKV

Defined at [[tests/test_cursor.py]] `tests/test_cursor.py:62`; table `cursorDiskKV`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `value` | `BLOB` | yes |  |

### cursorDiskKV

Defined at [[tests/fixtures/cursor/basic.sql]] `tests/fixtures/cursor/basic.sql:1`; table `cursorDiskKV`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `value` | `BLOB` | yes |  |

### cursorDiskKV

Defined at [[tests/fixtures/cursor/empty.sql]] `tests/fixtures/cursor/empty.sql:1`; table `cursorDiskKV`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `value` | `BLOB` | yes |  |

### files

Defined at [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:36`; table `files`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `path` | `TEXT` | no | PK |
| `source` | `TEXT` | no |  |
| `mtime` | `REAL` | no |  |
| `size` | `INTEGER` | no |  |
| `ingested_at` | `TEXT` | no |  |
| `warnings` | `TEXT` | no |  |
| `parser_version` | `INTEGER` | no |  |
| `ingested_offset` | `INTEGER` | no |  |
| `boundary_hash` | `TEXT` | yes |  |
| `title_seed` | `TEXT` | yes |  |

### message

Defined at [[tests/test_opencode.py]] `tests/test_opencode.py:20`; table `message`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `TEXT` | no | PK |
| `session_id` | `TEXT` | yes |  |
| `time_created` | `INTEGER` | yes |  |
| `time_updated` | `INTEGER` | yes |  |
| `data` | `TEXT` | yes |  |

### message

Defined at [[tests/test_opencode.py]] `tests/test_opencode.py:318`; table `message`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `TEXT` | no | PK |
| `session_id` | `TEXT` | yes |  |
| `data` | `TEXT` | yes |  |

### messages

Defined at [[src/ai_usage_cost/demo.py]] `src/ai_usage_cost/demo.py:79`; table `messages`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `INTEGER` | no | PK |
| `chat_id` | `INTEGER` | yes |  |
| `role` | `TEXT` | yes |  |
| `content` | `TEXT` | yes |  |
| `created_at` | `INTEGER` | yes |  |
| `approval_state` | `TEXT` | yes |  |
| `commit_hash` | `TEXT` | yes |  |

### messages

Defined at [[tests/fixtures/dyad/basic.sql]] `tests/fixtures/dyad/basic.sql:28`; table `messages`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `INTEGER` | no | PK |
| `chat_id` | `INTEGER` | yes |  |
| `role` | `TEXT` | yes |  |
| `content` | `TEXT` | yes |  |
| `created_at` | `INTEGER` | yes |  |
| `approval_state` | `TEXT` | yes |  |
| `commit_hash` | `TEXT` | yes |  |

### messages

Defined at [[tests/fixtures/dyad/null_title.sql]] `tests/fixtures/dyad/null_title.sql:28`; table `messages`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `INTEGER` | no | PK |
| `chat_id` | `INTEGER` | yes |  |
| `role` | `TEXT` | yes |  |
| `content` | `TEXT` | yes |  |
| `created_at` | `INTEGER` | yes |  |
| `approval_state` | `TEXT` | yes |  |
| `commit_hash` | `TEXT` | yes |  |

### messages

Defined at [[tests/fixtures/ollama_app/basic.sql]] `tests/fixtures/ollama_app/basic.sql:1`; table `messages`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `INTEGER` | no | PK |
| `chat_id` | `TEXT` | yes |  |
| `role` | `TEXT` | yes |  |
| `content` | `TEXT` | yes |  |
| `thinking` | `TEXT` | yes |  |
| `stream` | `INTEGER` | yes |  |
| `model_name` | `TEXT` | yes |  |
| `model_cloud` | `INTEGER` | yes |  |
| `model_ollama_host` | `TEXT` | yes |  |
| `created_at` | `TEXT` | yes |  |
| `updated_at` | `TEXT` | yes |  |
| `thinking_time_start` | `TEXT` | yes |  |
| `thinking_time_end` | `TEXT` | yes |  |
| `tool_result` | `TEXT` | yes |  |

### outcomes

Defined at [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:63`; table `outcomes`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `source` | `TEXT` | no | PK |
| `session_id` | `TEXT` | no | PK |
| `outcome` | `TEXT` | no |  |
| `notes` | `TEXT` | no |  |
| `tags` | `TEXT` | no |  |
| `updated_at` | `TEXT` | no |  |

### part

Defined at [[tests/test_opencode.py]] `tests/test_opencode.py:22`; table `part`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `TEXT` | no | PK |
| `message_id` | `TEXT` | yes |  |
| `session_id` | `TEXT` | yes |  |
| `time_created` | `INTEGER` | yes |  |
| `time_updated` | `INTEGER` | yes |  |
| `data` | `TEXT` | yes |  |

### part

Defined at [[tests/test_opencode.py]] `tests/test_opencode.py:319`; table `part`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `TEXT` | no | PK |
| `message_id` | `TEXT` | yes |  |
| `data` | `TEXT` | yes |  |

### requests

Defined at [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:23`; table `requests`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `fingerprint` | `TEXT` | no | PK |
| `source` | `TEXT` | no |  |
| `client` | `TEXT` | no |  |
| `provider` | `TEXT` | yes |  |
| `model` | `TEXT` | yes |  |
| `session_id` | `TEXT` | no |  |
| `timestamp` | `TEXT` | no |  |
| `request_id` | `TEXT` | yes |  |
| `uncached_input` | `INTEGER` | yes |  |
| `cache_read` | `INTEGER` | yes |  |
| `cache_write_5m` | `INTEGER` | yes |  |
| `cache_write_1h` | `INTEGER` | yes |  |
| `output` | `INTEGER` | yes |  |
| `reasoning_output` | `INTEGER` | yes |  |
| `is_sidechain` | `INTEGER` | no |  |
| `tier` | `TEXT` | no |  |
| `project` | `TEXT` | yes |  |
| `working_directory` | `TEXT` | yes |  |
| `repository` | `TEXT` | yes |  |
| `branch` | `TEXT` | yes |  |
| `machine` | `TEXT` | no |  |
| `source_file` | `TEXT` | no |  |
| `raw` | `TEXT` | no |  |
| `title` | `TEXT` | yes |  |
| `title_source` | `TEXT` | no |  |
| `reported_cost` | `REAL` | yes |  |

### samples

Defined at [[src/ai_usage_cost/collect.py]] `src/ai_usage_cost/collect.py:19`; table `samples`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `machine` | `TEXT` | no |  |
| `sampled_at` | `TEXT` | no |  |
| `gpu_util` | `REAL` | yes |  |
| `vram_used` | `INTEGER` | yes |  |
| `vram_total` | `INTEGER` | yes |  |
| `power_w` | `REAL` | yes |  |
| `source` | `TEXT` | no |  |

### session

Defined at [[tests/test_opencode.py]] `tests/test_opencode.py:15`; table `session`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `TEXT` | no | PK |
| `project_id` | `TEXT` | yes |  |
| `parent_id` | `TEXT` | yes |  |
| `slug` | `TEXT` | yes |  |
| `directory` | `TEXT` | yes |  |
| `title` | `TEXT` | yes |  |
| `version` | `TEXT` | yes |  |
| `cost` | `REAL` | yes |  |
| `tokens_input` | `INTEGER` | yes |  |
| `tokens_output` | `INTEGER` | yes |  |
| `tokens_reasoning` | `INTEGER` | yes |  |
| `tokens_cache_read` | `INTEGER` | yes |  |
| `tokens_cache_write` | `INTEGER` | yes |  |
| `time_created` | `INTEGER` | yes |  |
| `time_updated` | `INTEGER` | yes |  |

### session

Defined at [[tests/test_opencode.py]] `tests/test_opencode.py:317`; table `session`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `TEXT` | no | PK |

### session_exclusions

Defined at [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:69`; table `session_exclusions`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `source` | `TEXT` | no | PK |
| `session_id` | `TEXT` | no | PK |
| `excluded_at` | `TEXT` | no |  |

### sessions

Defined at [[tests/fixtures/copilot_chat/basic.sql]] `tests/fixtures/copilot_chat/basic.sql:1`; table `sessions`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `TEXT` | no | PK |
| `cwd` | `TEXT` | yes |  |
| `repository` | `TEXT` | yes |  |
| `host_type` | `TEXT` | yes |  |
| `branch` | `TEXT` | yes |  |
| `summary` | `TEXT` | yes |  |
| `agent_name` | `TEXT` | yes |  |
| `agent_description` | `TEXT` | yes |  |
| `created_at` | `TEXT` | yes |  |
| `updated_at` | `TEXT` | yes |  |

### sessions

Defined at [[tests/fixtures/copilot_chat/empty.sql]] `tests/fixtures/copilot_chat/empty.sql:1`; table `sessions`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `TEXT` | no | PK |
| `cwd` | `TEXT` | yes |  |
| `repository` | `TEXT` | yes |  |
| `host_type` | `TEXT` | yes |  |
| `branch` | `TEXT` | yes |  |
| `summary` | `TEXT` | yes |  |
| `agent_name` | `TEXT` | yes |  |
| `agent_description` | `TEXT` | yes |  |
| `created_at` | `TEXT` | yes |  |
| `updated_at` | `TEXT` | yes |  |

### trace_events

Defined at [[src/ai_usage_cost/store.py]] `src/ai_usage_cost/store.py:43`; table `trace_events`. Relations: -.

| Column | Type | Null | Key |
|---|---|---|---|
| `span_id` | `TEXT` | no | PK |
| `parent_id` | `TEXT` | yes |  |
| `record_parent` | `TEXT` | yes |  |
| `source` | `TEXT` | no |  |
| `session_id` | `TEXT` | no |  |
| `turn_id` | `TEXT` | yes |  |
| `agent_id` | `TEXT` | yes |  |
| `is_sidechain` | `INTEGER` | no |  |
| `seq` | `INTEGER` | no |  |
| `kind` | `TEXT` | no |  |
| `name` | `TEXT` | yes |  |
| `model` | `TEXT` | yes |  |
| `status` | `TEXT` | no |  |
| `started_at` | `TEXT` | no |  |
| `ended_at` | `TEXT` | yes |  |
| `duration_ms` | `INTEGER` | yes |  |
| `duration_provenance` | `TEXT` | no |  |
| `ttft_ms` | `INTEGER` | yes |  |
| `uncached_input` | `INTEGER` | yes |  |
| `cache_read` | `INTEGER` | yes |  |
| `cache_write_5m` | `INTEGER` | yes |  |
| `cache_write_1h` | `INTEGER` | yes |  |
| `output` | `INTEGER` | yes |  |
| `reasoning_output` | `INTEGER` | yes |  |
| `tokens_provenance` | `TEXT` | no |  |
| `context_capacity` | `INTEGER` | yes |  |
| `capacity_provenance` | `TEXT` | no |  |
| `retry_attempt` | `INTEGER` | yes |  |
| `error` | `TEXT` | yes |  |
| `source_file` | `TEXT` | no |  |
| `record_offset` | `INTEGER` | no |  |
| `record_length` | `INTEGER` | no |  |
| `content_path` | `TEXT` | yes |  |
| `detail` | `TEXT` | no |  |

### turns

Defined at [[tests/fixtures/copilot_chat/basic.sql]] `tests/fixtures/copilot_chat/basic.sql:14`; table `turns`. Relations: many-to-one `sessions`.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `INTEGER` | no | PK |
| `session_id` | `TEXT` | yes |  |
| `turn_index` | `INTEGER` | yes |  |
| `user_message` | `TEXT` | yes |  |
| `assistant_response` | `TEXT` | yes |  |
| `timestamp` | `TEXT` | yes |  |

### turns

Defined at [[tests/fixtures/copilot_chat/empty.sql]] `tests/fixtures/copilot_chat/empty.sql:14`; table `turns`. Relations: many-to-one `sessions`.

| Column | Type | Null | Key |
|---|---|---|---|
| `id` | `INTEGER` | no | PK |
| `session_id` | `TEXT` | yes |  |
| `turn_index` | `INTEGER` | yes |  |
| `user_message` | `TEXT` | yes |  |
| `assistant_response` | `TEXT` | yes |  |
| `timestamp` | `TEXT` | yes |  |
%% generated:schema end %%
