---
title: Reader types
aliases: []
tags: [class, diagram, mermaid]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/sources/**]
verified-against: 4d81cedd5403
sources: [docs/brain/architecture/diagrams/src-types.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost-sources
authored: true
use-cases: [UC-13]
approved-by: human
approved-at: '2026-11-19T00:12:14+00:00'
---

# Reader types

This diagram shows the few data types that every reader is built from and what each one holds. A reader describes itself with one record, produces usage records, and may add step by step spans. Knowing these shapes is enough to read any reader module or to write a new one.

## What the diagram shows

- Source is a frozen dataclass with an id, a label, a client map, a default roots function, a files function, a parse function, a token data flag and a display path. `src/ai_usage_cost/sources/base.py:18` `src/ai_usage_cost/sources/base.py:24` `src/ai_usage_cost/sources/base.py:26`
- Its optional parts are a spans function, a capabilities value, an experimental flag and a resume function. `src/ai_usage_cost/sources/base.py:27` `src/ai_usage_cost/sources/base.py:28` `src/ai_usage_cost/sources/base.py:40`
- Token data is a two value type, full or session. `src/ai_usage_cost/sources/base.py:14`
- Capabilities holds five labels, one each for trace, tokens, cost, context and latency, and every label defaults to unavailable. `src/ai_usage_cost/trace.py:104` `src/ai_usage_cost/trace.py:109`
- Provenance has five values: measured, derived, estimated, inferred and unavailable. `src/ai_usage_cost/models.py:9`
- A usage event names its source, client, model, timestamp, session and request, and may carry token usage, a title with its source and the cost the tool logged itself. `src/ai_usage_cost/models.py:49` `src/ai_usage_cost/models.py:57` `src/ai_usage_cost/models.py:72`
- Token usage splits counts into uncached input, cache read, two cache write buckets, output and reasoning output. `src/ai_usage_cost/models.py:12` `src/ai_usage_cost/models.py:16`
- A span has an id, a kind, a status, a start time and the file, offset and length of the record it came from. `src/ai_usage_cost/trace.py:55` `src/ai_usage_cost/trace.py:84`
- Spec is a frozen dataclass with a source id, a client name, an extension id, a flag for whether input tokens include cache, and an sdk flag. The Cline builder turns a Spec into a Source. `src/ai_usage_cost/sources/cline.py:82` `src/ai_usage_cost/sources/cline.py:86` `src/ai_usage_cost/sources/cline.py:410`

## Capability and related functionality

- The diagram realises the reader contract capability: the typed boundary between a tool's files and the rest of the application. [[Ai usage cost sources Overview]] explains the readers in prose, and [[Ai usage cost sources Workflows]] walks through a scan. The sibling views are [[Readers concepts]], [[Reader types]], [[Reader data lineage]], [[Reader module imports]], [[Reader glossary map]], [[Readers component view]] and [[Readers data flow]].
- The models behind the diagram live outside this chunk. The usage event and token usage are described with the other chunks of the package, and the contract itself is in [[Ai usage cost sources Data Model]].

## The diagram

%% generated:diagram-src-types start (do not edit; run brain docs generate) %%
```mermaid
classDiagram
    direction LR
    class Source {
        <<frozen dataclass>>
        +str id
        +str label
        +dict clients
        +default_roots() list~Path~
        +files(Path) list~Path~
        +parse(Path, warnings) Iterator~UsageEvent~
        +TokenData token_data
        +str display_path
        +spans(Path, warnings) Iterator~Span~
        +bool experimental
        +parse_resume(Path, warnings, offset, state) Iterator~UsageEvent~
        +root_hint str
    }
    class Spec {
        <<frozen dataclass>>
        +str source_id
        +str client
        +str ext_id
        +bool tokens_in_inclusive
        +bool sdk
    }
    class Capabilities {
        +Provenance trace
        +Provenance tokens
        +Provenance cost
        +Provenance context
        +Provenance latency
    }
    class UsageEvent {
        +str source
        +str client
        +str model
        +datetime timestamp
        +str session_id
        +str request_id
        +str project
        +str title
        +str title_source
        +int record_offset
        +float reported_cost
    }
    class TokenUsage {
        +int uncached_input
        +int cache_read
        +int cache_write_5m
        +int cache_write_1h
        +int output
        +int reasoning_output
    }
    class Span {
        +str span_id
        +SpanKind kind
        +SpanStatus status
        +datetime started_at
        +str source_file
        +int record_offset
        +int record_length
    }
    class TokenData {
        <<enumeration>>
        full
        session
    }
    class Provenance {
        <<enumeration>>
        measured
        derived
        estimated
        inferred
        unavailable
    }
    Source *-- "1" Capabilities : declares
    Source --> "1" TokenData : token_data
    Source ..> UsageEvent : parse yields
    Source ..> Span : spans yields, optional
    UsageEvent o-- "0..1" TokenUsage : tokens
    Span o-- "0..1" TokenUsage : tokens
    Capabilities --> Provenance : each field
    Spec ..> Source : make_source builds
    class Legend {
        <<legend>>
        Box is a type with its fields
        Diamond line is composition
        Open diamond line is a part that may be absent
        Dashed arrow is a use, not ownership
        0..1 means the value may be missing
    }
```
%% generated:diagram-src-types end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `src/ai_usage_cost/sources/base.py:18` | Reader record |
> | `src/ai_usage_cost/sources/cline.py:82` | Specification used by the Cline family builder |
> | `src/ai_usage_cost/trace.py:104` | Per reader capability labels |
> | `src/ai_usage_cost/models.py:49` | Usage record produced by parse |
> | `src/ai_usage_cost/models.py:12` | Token buckets |
> | `src/ai_usage_cost/trace.py:55` | Step record produced by spans |
