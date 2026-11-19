---
title: Usage cost types
aliases: []
tags: [class, diagram, mermaid]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/*]
verified-against: 1445ea834ab7
sources: [docs/brain/architecture/diagrams/usage-cost-types.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost
authored: true
approved-by: human
approved-at: '2026-11-19T06:39:06+00:00'
---

# Usage cost types

This view shows the record types the tool passes around in memory, as opposed to the tables it stores. It explains how one logged request gains a price, how priced requests are summed into a report and how a session rating is shaped. A developer can see at a glance which types to change when a new figure must reach the report.

## What the diagram shows

- A usage event is one logged request with its client, model, time, session, service tier and the cost the tool itself logged, if any. `src/ai_usage_cost/models.py:49-72`
- Its token counts are optional, and the totals are computed from the six counted fields. `src/ai_usage_cost/models.py:12-33` `src/ai_usage_cost/models.py:57`
- A priced event wraps one usage event with an optional cost breakdown and a cost state. `src/ai_usage_cost/models.py:117-120`
- A cost breakdown holds the price of each token kind, a no cache baseline and the estimated flag, and its total is the sum of the four prices. `src/ai_usage_cost/models.py:75-98`
- A bucket sums tokens, cost, requests and sessions under one key. `src/ai_usage_cost/models.py:123-130`
- The analysis holds every priced event, the rate table, the file count, the warnings and the store path. `src/ai_usage_cost/pipeline.py:44-55`
- A rate table holds its as of date, currency and model rows, and each row names the model prefix it matches, its provider and display name. `src/ai_usage_cost/pricing.py:252-260` `src/ai_usage_cost/pricing.py:126-129`
- A report carries totals, buckets by client, provider, model, project and day, session rows and the warnings. `src/ai_usage_cost/aggregate.py:462-482` `src/ai_usage_cost/aggregate.py:26-34`
- A session row carries the worst cost state of its requests and the session rating. `src/ai_usage_cost/aggregate.py:48-75`
- A span is one step of a session trace with its kind, status and the provenance of its token counts. `src/ai_usage_cost/trace.py:55-86`
- An outcome extends the rating update with the source and session it belongs to. `src/ai_usage_cost/trace.py:141-151`

## Capability and related functionality

- The stored form of these types is the entity diagram in [[Ai usage cost Data Model]]; the business view is [[Usage cost conceptual model]].
- The cost state field is drawn as a lifecycle in [[Cost state of a request]].
- The report type is what the routes in [[Usage cost HTTP routes]] return.

## Usage cost types

%% generated:diagram-usage-cost-types start (do not edit; run brain docs generate) %%
```mermaid
classDiagram
    direction LR
    class UsageEvent {
        +str source
        +str client
        +str model
        +datetime timestamp
        +str session_id
        +str tier
        +bool is_sidechain
        +float reported_cost
    }
    class TokenUsage {
        +int uncached_input
        +int cache_read
        +int cache_write_5m
        +int cache_write_1h
        +int output
        +int reasoning_output
        +total() int
    }
    class PricedEvent {
        +CostState state
    }
    class CostBreakdown {
        +float uncached_input
        +float cache_read
        +float cache_write
        +float output
        +float no_cache_equivalent
        +bool estimated
        +total() float
    }
    class Bucket {
        +str key
        +int events
        +int sessions
    }
    class Report {
        +datetime generated_at
        +str rates_as_of
        +list warnings
    }
    class Totals {
        +int events
        +int sessions
    }
    class SessionRow {
        +str session_id
        +CostState cost_state
        +OutcomeLabel outcome
    }
    class Analysis {
        +int files
        +list warnings
        +Path db_path
    }
    class RateTable {
        +str as_of
        +str currency
    }
    class ModelRate {
        +str match
        +str provider
        +str display
    }
    class Span {
        +str span_id
        +SpanKind kind
        +SpanStatus status
        +Provenance tokens_provenance
    }
    class OutcomeUpdate {
        +OutcomeLabel outcome
        +str notes
        +list tags
    }
    class Outcome {
        +str source
        +str session_id
    }
    UsageEvent "1" *-- "0..1" TokenUsage : tokens
    PricedEvent "1" *-- "1" UsageEvent : event
    PricedEvent "1" *-- "0..1" CostBreakdown : cost
    Analysis "1" o-- "*" PricedEvent : events
    Analysis "1" --> "1" RateTable : table
    RateTable "1" *-- "*" ModelRate : models
    Report "1" *-- "1" Totals : totals
    Report "1" *-- "*" Bucket : by_client, by_model, by_day
    Report "1" *-- "*" SessionRow : sessions
    Bucket "1" *-- "1" CostBreakdown : cost
    Span "1" *-- "0..1" TokenUsage : tokens
    OutcomeUpdate <|-- Outcome
    class Legend {
        <<legend>>
        +field type
    }
    note for Legend "Legend: a box is a type with the fields that carry meaning. A line with a filled diamond is composition, an open diamond is aggregation, an open triangle is inheritance, a plain arrow is a reference. Numbers at each end are multiplicities: 1 one, 0..1 optional, * many."
```
%% generated:diagram-usage-cost-types end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `src/ai_usage_cost/models.py:12-134` | Token, event, cost, priced event and bucket types |
> | `src/ai_usage_cost/pipeline.py:44-63` | The analysis type |
> | `src/ai_usage_cost/pricing.py:126-145` | A rate row |
> | `src/ai_usage_cost/aggregate.py:26-75` | Totals and session row |
> | `src/ai_usage_cost/aggregate.py:462-482` | The report type |
> | `src/ai_usage_cost/trace.py:55-151` | Span and outcome types |
