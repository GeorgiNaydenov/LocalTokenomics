---
title: Domain Models
aliases: []
tags: [data, generated, models, spec]
area: data
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [src/ai_usage_cost/aggregate.py, src/ai_usage_cost/models.py, src/ai_usage_cost/pricing.py,
  src/ai_usage_cost/privacy.py, src/ai_usage_cost/trace.py]
generated: true
anchors: true
---

# Domain Models

> [!info] What this is
> The entities the application works with, their attributes and where each is declared in the code.

## AlertDecision

The entity AlertDecision, declared in src/ai_usage_cost/cli.py lines 252-254. It has 2 fields and 0 relations.

- `fire`: `bool`
- `message`: `str`

No lifecycle field was found in the code.

Source:
- `AlertDecision`: `class AlertDecision:`

## Analysis

The entity Analysis, declared in src/ai_usage_cost/pipeline.py lines 45-63. It has 9 fields and 0 relations.

- `events`: `list[PricedEvent]`
- `table`: `RateTable`
- `files`: `int`
- `warnings`: `list[str]`
- `scan_warnings`: `list[str]`
- `sources`: `list[SourceInfo]`
- `session_flags`: `dict[tuple[str, str], tuple[bool, int, str]]`
- `db_path`: `Path | None`
- `today`: `date | None`

No lifecycle field was found in the code.

Source:
- `Analysis`: `class Analysis:`

## apps

The table apps apps, declared in src/ai_usage_cost/demo.py lines 52-69. It has 16 fields and 0 relations.

- `id`: `INTEGER (PK, required)`
- `name`: `TEXT`
- `path`: `TEXT`
- `created_at`: `INTEGER`
- `updated_at`: `INTEGER`
- `github_org`: `TEXT`
- `github_repo`: `TEXT`
- `chat_context`: `TEXT`
- `github_branch`: `TEXT`
- `vercel_project_id`: `TEXT`
- `vercel_project_name`: `TEXT`
- `vercel_team_id`: `TEXT`
- `vercel_deployment_url`: `TEXT`
- `neon_project_id`: `TEXT`
- `neon_development_branch_id`: `TEXT`
- `neon_preview_branch_id`: `TEXT`

No lifecycle field was found in the code.

Source:
- `apps`: `CREATE TABLE apps (`

## Bucket

A group of priced events under one key such as a client, provider, model, project or day, with summed tokens and cost. [[src/ai_usage_cost/models.py|src/ai_usage_cost/models.py:123]]

- key, label, tokens, cost, events, sessions, reported_cost

No lifecycle field was found in the code.

Source:
- `Bucket`: `class Bucket(BaseModel):`

## Capabilities

The entity Capabilities, declared in src/ai_usage_cost/trace.py lines 104-109. It has 5 fields and 0 relations.

- `trace`: `Provenance`
- `tokens`: `Provenance`
- `cost`: `Provenance`
- `context`: `Provenance`
- `latency`: `Provenance`

No lifecycle field was found in the code.

Source:
- `Capabilities`: `class Capabilities(BaseModel):`

## chats

The table chats chats, declared in src/ai_usage_cost/demo.py lines 71-77. It has 5 fields and 0 relations.

- `id`: `INTEGER (PK, required)`
- `app_id`: `INTEGER`
- `title`: `TEXT`
- `created_at`: `INTEGER`
- `initial_commit_hash`: `TEXT`

No lifecycle field was found in the code.

Source:
- `chats`: `CREATE TABLE chats (`

## ClientInfo

The entity ClientInfo, declared in src/ai_usage_cost/api.py lines 86-88. It has 2 fields and 0 relations.

- `id`: `str`
- `label`: `str`

No lifecycle field was found in the code.

Source:
- `ClientInfo`: `class ClientInfo(BaseModel):`

## Config

The privacy settings read from config.json in the store folder. [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:52]]

- `metadata_only`: `default true`
- exclude_projects, max_content_bytes
- `metadata_retention_days, content_retention_days`: `default None`

No lifecycle field was found in the code.

Source:
- `Config`: `class Config(BaseModel):`

## ContextSnapshot

The entity ContextSnapshot, declared in src/ai_usage_cost/trace.py lines 112-131. It has 14 fields and 0 relations.

- `span_id`: `str`
- `model`: `str | None`
- `started_at`: `datetime`
- `input_total`: `int | None`
- `tokens_provenance`: `Provenance`
- `capacity`: `int | None`
- `capacity_provenance`: `Provenance`
- `occupancy`: `float | None`
- `occupancy_provenance`: `Provenance`
- `delta_input`: `int | None`
- `added_span_ids`: `list[str]`
- `compacted_before`: `bool`
- `composition`: `dict[str, float]`
- `model_config`: `ConfigDict`

No lifecycle field was found in the code.

Source:
- `ContextSnapshot`: `class ContextSnapshot(BaseModel):`

## CostBreakdown

The computed cost of a request or of a group of requests, split into uncached input, cache read, cache write and output, with the no cache baseline. [[src/ai_usage_cost/models.py|src/ai_usage_cost/models.py:75]]

- `uncached_input, cache_read, cache_write, output, no_cache_equivalent`: `dollars`
- `estimated`: `true when any part was priced from a shorter id prefix`
- `total, cache_savings`: `derived`

No lifecycle field was found in the code.

Source:
- `CostBreakdown`: `class CostBreakdown(BaseModel):`

## Economics

The entity Economics, declared in src/ai_usage_cost/trace.py lines 177-181. It has 4 fields and 0 relations.

- `totals`: `EconRow`
- `by_turn`: `list[EconRow]`
- `by_model`: `list[EconRow]`
- `by_tool`: `list[EconRow]`

No lifecycle field was found in the code.

Source:
- `Economics`: `class Economics(BaseModel):`

## EconRow

The entity EconRow, declared in src/ai_usage_cost/trace.py lines 154-174. It has 19 fields and 0 relations.

- `key`: `str`
- `label`: `str | None`
- `ordinal`: `int | None`
- `started_at`: `datetime | None`
- `is_sidechain`: `bool`
- `model_calls`: `int`
- `tool_calls`: `int`
- `tokens`: `TokenUsage | None`
- `tokens_provenance`: `Provenance`
- `cost`: `CostBreakdown | None`
- `cost_state`: `CostState`
- `duration_ms`: `int | None`
- `duration_provenance`: `Provenance`
- `errors`: `int`
- `retries`: `int | None`
- `amplification`: `float | None`
- `cache_hit_ratio`: `float | None`
- `tokens_per_second`: `float | None`
- `model_config`: `ConfigDict`

Lifecycle is described by [[State Machines#CostState lifecycle|CostState lifecycle]].

Source:
- `EconRow`: `class EconRow(BaseModel):`

## Facets

The entity Facets, declared in src/ai_usage_cost/aggregate.py lines 454-459. It has 5 fields and 0 relations.

- `states`: `dict[str, int]`
- `clients`: `dict[str, int]`
- `models`: `dict[str, int]`
- `projects`: `dict[str, int]`
- `outcomes`: `dict[str, int]`

No lifecycle field was found in the code.

Source:
- `Facets`: `class Facets(BaseModel):`

## files

The table files files, declared in src/ai_usage_cost/store.py lines 36-82. It has 10 fields and 0 relations.

- `path`: `TEXT (PK, required)`
- `source`: `TEXT (required)`
- `mtime`: `REAL (required)`
- `size`: `INTEGER (required)`
- `ingested_at`: `TEXT (required)`
- `warnings`: `TEXT (required)`
- `parser_version`: `INTEGER (required), default 0`
- `ingested_offset`: `INTEGER (required), default 0`
- `boundary_hash`: `TEXT`
- `title_seed`: `TEXT`

No lifecycle field was found in the code.

Source:
- `files`: `CREATE TABLE files (`

## IngestSummary

The entity IngestSummary, declared in src/ai_usage_cost/store.py lines 134-137. It has 3 fields and 0 relations.

- `files_parsed`: `int`
- `files_skipped`: `int`
- `warnings`: `list[str]`

No lifecycle field was found in the code.

Source:
- `IngestSummary`: `class IngestSummary:`

## Insight

The entity Insight, declared in src/ai_usage_cost/trace.py lines 184-189. It has 5 fields and 0 relations.

- `kind`: `str`
- `severity`: `Literal['info', 'warning', 'critical']`
- `span_id`: `str`
- `message`: `str`
- `count`: `int`

No lifecycle field was found in the code.

Source:
- `Insight`: `class Insight(BaseModel):`

## messages

The table messages messages, declared in src/ai_usage_cost/demo.py lines 79-87. It has 7 fields and 0 relations.

- `id`: `INTEGER (PK, required)`
- `chat_id`: `INTEGER`
- `role`: `TEXT`
- `content`: `TEXT`
- `created_at`: `INTEGER`
- `approval_state`: `TEXT`
- `commit_hash`: `TEXT`

No lifecycle field was found in the code.

Source:
- `messages`: `CREATE TABLE messages (`

## Meta

The entity Meta, declared in src/ai_usage_cost/api.py lines 105-128. It has 18 fields and 0 relations.

- `clients`: `list[ClientInfo]`
- `providers`: `list[str]`
- `models`: `list[str]`
- `projects`: `list[str]`
- `first_day`: `date | None`
- `last_day`: `date | None`
- `rates_as_of`: `str`
- `rates_age_days`: `int | None`
- `currency`: `str`
- `files_scanned`: `int`
- `events`: `int`
- `warnings`: `list[str]`
- `warning_summary`: `WarningSummary`
- `session_warnings`: `dict[str, list[str]]`
- `sources`: `list[SourceInfo]`
- `client_last_seen`: `dict[str, str]`
- `model_last_seen`: `dict[str, str]`
- `project_last_seen`: `dict[str, str]`

No lifecycle field was found in the code.

Source:
- `Meta`: `class Meta(BaseModel):`

## ModelMatch

The entity ModelMatch, declared in src/ai_usage_cost/pricing.py lines 224-229. It has 2 fields and 0 relations.

- `match`: `str | None`
- `kind`: `Literal['exact', 'suffix', 'estimated', 'none']`

No lifecycle field was found in the code.

Source:
- `ModelMatch`: `class ModelMatch(BaseModel):`

## ModelRate

One row of the rate table: prices per million tokens for a model id prefix, with variants, bands, a peak window and dated periods. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:126]]

- `match, provider, display`: `required`
- `input, output, cache_read, cache_write_5m, cache_write_1h`: `dollars per million tokens`
- variants, bands, peak, periods, cache_rules, context_window, status

Source:
- `ModelRate`: `class ModelRate(PriceSet):`

## Outcome

The rating a person gives to a session, with notes and tags, plus signals computed from its spans. [[src/ai_usage_cost/trace.py|src/ai_usage_cost/trace.py:147]]

- `source, session_id`: `identity`
- `outcome`: `successful, partial, failed, abandoned or unrated`
- notes, tags, updated_at, signals

Source:
- `Outcome`: `class Outcome(OutcomeUpdate):`

## outcomes

The table outcomes outcomes, declared in src/ai_usage_cost/store.py lines 63-68. It has 6 fields and 0 relations.

- `source`: `TEXT (PK, required)`
- `session_id`: `TEXT (PK, required)`
- `outcome`: `TEXT (required)`
- `notes`: `TEXT (required)`
- `tags`: `TEXT (required)`
- `updated_at`: `TEXT (required)`

No lifecycle field was found in the code.

Source:
- `outcomes`: `CREATE TABLE outcomes (`

## OutcomeSignals

The entity OutcomeSignals, declared in src/ai_usage_cost/trace.py lines 134-138. It has 4 fields and 0 relations.

- `aborted_turns`: `int`
- `interrupted_tools`: `int`
- `errors`: `int`
- `last_turn_status`: `SpanStatus`

Lifecycle is described by [[State Machines#SpanStatus lifecycle|SpanStatus lifecycle]].

Source:
- `OutcomeSignals`: `class OutcomeSignals(BaseModel):`

## OutcomeUpdate

The entity OutcomeUpdate, declared in src/ai_usage_cost/trace.py lines 141-144. It has 3 fields and 0 relations.

- `outcome`: `OutcomeLabel`
- `notes`: `str`
- `tags`: `list[str]`

No lifecycle field was found in the code.

Source:
- `OutcomeUpdate`: `class OutcomeUpdate(BaseModel):`

## PartialRules

The entity PartialRules, declared in src/ai_usage_cost/pricing.py lines 109-117. It has 5 fields and 0 relations.

- `cache_read`: `float | None`
- `cache_write_5m`: `float | None`
- `cache_write_1h`: `float | None`
- `batch`: `float | None`
- `free`: `bool | None`

No lifecycle field was found in the code.

Source:
- `PartialRules`: `class PartialRules(BaseModel):`

## Period

The entity Period, declared in src/ai_usage_cost/pricing.py lines 68-98. It has 11 fields and 0 relations.

- `model_config`: `ConfigDict`
- `from_`: `date | None`
- `until`: `date | None`
- `input`: `float | None`
- `output`: `float | None`
- `cache_read`: `float | None`
- `cache_write_5m`: `float | None`
- `cache_write_1h`: `float | None`
- `variants`: `dict[str, PriceSet] | None`
- `bands`: `list[Band] | None`
- `peak`: `Peak | None`

No lifecycle field was found in the code.

Source:
- `Period`: `class Period(BaseModel):`

## Prefix

The entity Prefix, declared in src/ai_usage_cost/pricing.py lines 169-171. It has 2 fields and 0 relations.

- `prefix`: `str`
- `provider`: `str | None`

No lifecycle field was found in the code.

Source:
- `Prefix`: `class Prefix(BaseModel):`

## PricedEvent

A usage event with its cost breakdown (absent when not priced) and its cost state. [[src/ai_usage_cost/models.py|src/ai_usage_cost/models.py:117]]

- `event`: `the usage event`
- `cost`: `breakdown or None`
- `state`: `priced, free, unpriced or unavailable`

Lifecycle is described by [[State Machines#CostState lifecycle|CostState lifecycle]].

Source:
- `PricedEvent`: `class PricedEvent(BaseModel):`

## PriceSet

The entity PriceSet, declared in src/ai_usage_cost/pricing.py lines 29-37. It has 5 fields and 0 relations.

- `input`: `float`
- `output`: `float`
- `cache_read`: `float | None`
- `cache_write_5m`: `float | None`
- `cache_write_1h`: `float | None`

No lifecycle field was found in the code.

Source:
- `PriceSet`: `class PriceSet(BaseModel):`

## ProviderRules

The entity ProviderRules, declared in src/ai_usage_cost/pricing.py lines 101-106. It has 5 fields and 0 relations.

- `cache_read`: `float`
- `cache_write_5m`: `float`
- `cache_write_1h`: `float`
- `batch`: `float`
- `free`: `bool`

No lifecycle field was found in the code.

Source:
- `ProviderRules`: `class ProviderRules(BaseModel):`

## RateTable

The loaded rates.json: model rows, provider cache rules, gateway prefixes and models known to have no price. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:252]]

- as_of, currency, units, notes
- `models`: `rows keyed by a match prefix`
- `providers`: `cache and batch rules per provider`
- prefixes, unpriced_models

No lifecycle field was found in the code.

Source:
- `RateTable`: `class RateTable(BaseModel):`

## Report

The answer to one query: totals, buckets by client, provider, model, project and day, session rows, warnings and facets. [[src/ai_usage_cost/aggregate.py|src/ai_usage_cost/aggregate.py:462]]

- totals, by_client, by_provider, by_model, by_project, by_day, series, sessions
- unknown_models, warnings, scan_warnings, warning_groups, facets, model_matches
- rates_as_of, rates_age_days, currency, files_scanned, files_in_slice

No lifecycle field was found in the code.

Source:
- `Report`: `class Report(BaseModel):`

## requests

The table requests requests, declared in src/ai_usage_cost/store.py lines 23-85. It has 26 fields and 0 relations.

- `fingerprint`: `TEXT (PK, required)`
- `source`: `TEXT (required)`
- `client`: `TEXT (required)`
- `provider`: `TEXT`
- `model`: `TEXT`
- `session_id`: `TEXT (required)`
- `timestamp`: `TEXT (required)`
- `request_id`: `TEXT`
- `uncached_input`: `INTEGER`
- `cache_read`: `INTEGER`
- `cache_write_5m`: `INTEGER`
- `cache_write_1h`: `INTEGER`
- `output`: `INTEGER`
- `reasoning_output`: `INTEGER`
- `is_sidechain`: `INTEGER (required)`
- `tier`: `TEXT (required)`
- `project`: `TEXT`
- `working_directory`: `TEXT`
- `repository`: `TEXT`
- `branch`: `TEXT`
- `machine`: `TEXT (required)`
- `source_file`: `TEXT (required)`
- `raw`: `TEXT (required)`
- `title`: `TEXT`
- `title_source`: `TEXT (required), default 'folder'`
- `reported_cost`: `REAL`

No lifecycle field was found in the code.

Source:
- `requests`: `CREATE TABLE requests (`

## Sample

The entity Sample, declared in src/ai_usage_cost/collect.py lines 49-56. It has 7 fields and 0 relations.

- `machine`: `str`
- `sampled_at`: `datetime`
- `gpu_util`: `float | None`
- `vram_used`: `int | None`
- `vram_total`: `int | None`
- `power_w`: `float | None`
- `source`: `str`

No lifecycle field was found in the code.

Source:
- `Sample`: `class Sample(BaseModel):`

## samples

The table samples samples, declared in src/ai_usage_cost/collect.py lines 19-23. It has 7 fields and 0 relations.

- `machine`: `TEXT (required)`
- `sampled_at`: `TEXT (required)`
- `gpu_util`: `REAL`
- `vram_used`: `INTEGER`
- `vram_total`: `INTEGER`
- `power_w`: `REAL`
- `source`: `TEXT (required)`

No lifecycle field was found in the code.

Source:
- `samples`: `CREATE TABLE IF NOT EXISTS samples (`

## SeriesPoint

The entity SeriesPoint, declared in src/ai_usage_cost/aggregate.py lines 37-45. It has 8 fields and 0 relations.

- `day`: `date`
- `client`: `str`
- `provider`: `str`
- `model`: `str`
- `source`: `str`
- `cost`: `float`
- `tokens`: `int`
- `events`: `int`

No lifecycle field was found in the code.

Source:
- `SeriesPoint`: `class SeriesPoint(BaseModel):`

## session_exclusions

The table session_exclusions session_exclusions, declared in src/ai_usage_cost/store.py lines 69-72. It has 3 fields and 0 relations.

- `source`: `TEXT (PK, required)`
- `session_id`: `TEXT (PK, required)`
- `excluded_at`: `TEXT (required)`

No lifecycle field was found in the code.

Source:
- `session_exclusions`: `CREATE TABLE session_exclusions (`

## SessionRow

One session in a report: its time span, models, summed tokens and cost, worst cost state and rating. [[src/ai_usage_cost/aggregate.py|src/ai_usage_cost/aggregate.py:48]]

- `session_id, source, client, provider`: `identity`
- start_time, end_time, request_count, tokens, cost, reported_cost
- `cost_state`: `worst of its requests; outcome, traced, error_count, title`

Lifecycle is described by [[State Machines#CostState lifecycle|CostState lifecycle]].

Source:
- `SessionRow`: `class SessionRow(BaseModel):`

## Source

The frozen description of one reader: id, label, client names, default roots, file lister, parse function, token data flag, display path, optional spans, capabilities, experimental flag and resume hook.

- `id`: `str`
- `label`: `str`
- `clients`: `dict[str, str]`
- `default_roots`: `Callable[[], list[Path]]`
- `files`: `Callable[[Path], list[Path]]`
- `parse`: `Callable[[Path, list[str]], Iterator[UsageEvent]]`
- `token_data`: `TokenData`
- `display_path`: `str`
- `spans`: `Callable[[Path, list[str]], Iterator[Span]] | None`
- `capabilities`: `Capabilities`
- `experimental`: `bool`
- `parse_resume`: `Callable[[Path, list[str], int, str | None], Iterator[UsageEvent]] | None`

No lifecycle field was found in the code.

Source:
- [[src/ai_usage_cost/sources/base.py|src/ai_usage_cost/sources/base.py]]: `class Source:`

## SourceInfo

The entity SourceInfo, declared in src/ai_usage_cost/pipeline.py lines 31-41. It has 10 fields and 0 relations.

- `id`: `str`
- `label`: `str`
- `clients`: `list[str]`
- `token_data`: `TokenData`
- `path`: `str`
- `root_hint`: `str`
- `detected`: `bool`
- `files`: `int`
- `capabilities`: `Capabilities`
- `experimental`: `bool`

No lifecycle field was found in the code.

Source:
- `SourceInfo`: `class SourceInfo(BaseModel):`

## Span

One step of a session trace: a turn, a message, a model call, a tool call or an error, with timing, tokens and where its record sits in the log. [[src/ai_usage_cost/trace.py|src/ai_usage_cost/trace.py:55]]

- span_id, parent_id, session_id, turn_id, agent_id, kind, status
- started_at, ended_at, duration_ms, tokens, context_capacity, each with a provenance
- source_file, record_offset, record_length, content_path

Lifecycle is described by [[State Machines#SpanKind lifecycle|SpanKind lifecycle]]. Lifecycle is described by [[State Machines#SpanStatus lifecycle|SpanStatus lifecycle]].

Source:
- `Span`: `class Span(BaseModel):`

## SpanContent

The entity SpanContent, declared in src/ai_usage_cost/trace.py lines 201-205. It has 4 fields and 0 relations.

- `span_id`: `str`
- `content`: `str`
- `truncated`: `bool`
- `redactions`: `int`

No lifecycle field was found in the code.

Source:
- `SpanContent`: `class SpanContent(BaseModel):`

## Spec

Per tool settings shared by the Cline family readers: source id, client name, extension id, whether input tokens include cache buckets, and whether the SDK store is read.

- `source_id`: `str`
- `client`: `str`
- `ext_id`: `str`
- `tokens_in_inclusive`: `bool`
- `sdk`: `bool`

No lifecycle field was found in the code.

Source:
- [[src/ai_usage_cost/sources/cline.py|src/ai_usage_cost/sources/cline.py]]: `class Spec:`

## TokenUsage

The token counts of one request, split into uncached input, cache read, two cache write buckets, output and reasoning output. [[src/ai_usage_cost/models.py|src/ai_usage_cost/models.py:12]]

- `uncached_input, cache_read, cache_write_5m, cache_write_1h, output, reasoning_output`: `whole numbers, default 0`
- `cache_write, input_total, total`: `derived, never stored`

No lifecycle field was found in the code.

Source:
- `TokenUsage`: `class TokenUsage(BaseModel):`

## Totals

The entity Totals, declared in src/ai_usage_cost/aggregate.py lines 26-34. It has 8 fields and 0 relations.

- `tokens`: `TokenUsage`
- `cost`: `CostBreakdown`
- `reported_cost`: `float | None`
- `events`: `int`
- `priced_events`: `int`
- `sessions`: `int`
- `first_event`: `datetime | None`
- `last_event`: `datetime | None`

No lifecycle field was found in the code.

Source:
- `Totals`: `class Totals(BaseModel):`

## Trace

The entity Trace, declared in src/ai_usage_cost/trace.py lines 192-198. It has 6 fields and 0 relations.

- `source`: `str`
- `session_id`: `str`
- `capabilities`: `Capabilities`
- `spans`: `list[Span]`
- `outcome`: `Outcome | None`
- `insights`: `list[Insight]`

No lifecycle field was found in the code.

Source:
- `Trace`: `class Trace(BaseModel):`

## trace_events

The table trace_events trace_events, declared in src/ai_usage_cost/store.py lines 43-60. It has 34 fields and 0 relations.

- `span_id`: `TEXT (PK, required)`
- `parent_id`: `TEXT`
- `record_parent`: `TEXT`
- `source`: `TEXT (required)`
- `session_id`: `TEXT (required)`
- `turn_id`: `TEXT`
- `agent_id`: `TEXT`
- `is_sidechain`: `INTEGER (required)`
- `seq`: `INTEGER (required)`
- `kind`: `TEXT (required)`
- `name`: `TEXT`
- `model`: `TEXT`
- `status`: `TEXT (required)`
- `started_at`: `TEXT (required)`
- `ended_at`: `TEXT`
- `duration_ms`: `INTEGER`
- `duration_provenance`: `TEXT (required)`
- `ttft_ms`: `INTEGER`
- `uncached_input`: `INTEGER`
- `cache_read`: `INTEGER`
- `cache_write_5m`: `INTEGER`
- `cache_write_1h`: `INTEGER`
- `output`: `INTEGER`
- `reasoning_output`: `INTEGER`
- `tokens_provenance`: `TEXT (required)`
- `context_capacity`: `INTEGER`
- `capacity_provenance`: `TEXT (required)`
- `retry_attempt`: `INTEGER`
- `error`: `TEXT`
- `source_file`: `TEXT (required)`
- `record_offset`: `INTEGER (required)`
- `record_length`: `INTEGER (required)`
- `content_path`: `TEXT`
- `detail`: `TEXT (required)`

No lifecycle field was found in the code.

Source:
- `trace_events`: `CREATE TABLE trace_events (`

## UnknownModel

The entity UnknownModel, declared in src/ai_usage_cost/aggregate.py lines 77-80. It has 3 fields and 0 relations.

- `model`: `str`
- `tokens`: `int`
- `events`: `int`

No lifecycle field was found in the code.

Source:
- `UnknownModel`: `class UnknownModel(BaseModel):`

## UnpricedModel

The entity UnpricedModel, declared in src/ai_usage_cost/pricing.py lines 232-242. It has 3 fields and 0 relations.

- `match`: `str`
- `note`: `str`
- `status`: `Literal['watchlist', 'no_list_price'] | None`

No lifecycle field was found in the code.

Source:
- `UnpricedModel`: `class UnpricedModel(BaseModel):`

## UsageEvent

One request read from a log: who made it, when, with which model and how many tokens, plus project and title context. [[src/ai_usage_cost/models.py|src/ai_usage_cost/models.py:49]]

- `source, client, session_id, timestamp`: `required`
- `provider, model, request_id, tokens`: `optional; tokens is None when the log has no counts`
- `tier`: `service tier, default standard`
- `reported_cost`: `the cost the tool itself logged, kept beside the computed one`

No lifecycle field was found in the code.

Source:
- `UsageEvent`: `class UsageEvent(BaseModel):`

## WarningGroup

The entity WarningGroup, declared in src/ai_usage_cost/aggregate.py lines 115-127. It has 11 fields and 0 relations.

- `kind`: `str`
- `label`: `str`
- `count`: `int`
- `summary`: `str`
- `severity`: `WarningSeverity`
- `total_delta_tokens`: `int`
- `total_delta_cost`: `float`
- `worst_example`: `WarningInstance | None`
- `affected_sessions`: `int`
- `instances`: `list[WarningInstance]`
- `warnings`: `list[str]`

No lifecycle field was found in the code.

Source:
- `WarningGroup`: `class WarningGroup(BaseModel):`

## WarningInstance

The entity WarningInstance, declared in src/ai_usage_cost/aggregate.py lines 100-111. It has 10 fields and 0 relations.

- `kind`: `str`
- `message`: `str`
- `source`: `str`
- `file`: `str | None`
- `session_id`: `str | None`
- `severity`: `WarningSeverity`
- `delta_tokens`: `int | None`
- `delta_cost`: `float | None`
- `likely_cause`: `str | None`
- `auto_corrected`: `bool`

No lifecycle field was found in the code.

Source:
- `WarningInstance`: `class WarningInstance(BaseModel):`

## WarningSummary

The entity WarningSummary, declared in src/ai_usage_cost/api.py lines 91-102. It has 4 fields and 0 relations.

- `critical`: `int`
- `caution`: `int`
- `info`: `int`
- `total_delta_cost`: `float`

No lifecycle field was found in the code.

Source:
- `WarningSummary`: `class WarningSummary(BaseModel):`
