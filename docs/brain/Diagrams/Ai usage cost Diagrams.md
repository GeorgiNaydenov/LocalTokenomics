---
title: Ai usage cost Diagrams
aliases: []
tags: [c4, diagram, erd, mermaid]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/*]
verified-against: 1445ea834ab7
sources: [docs/brain/architecture/diagrams/module-ch-localtokenomics-src-ai-usage-cost.mmd,
  docs/brain/architecture/diagrams/er-ch-localtokenomics-src-ai-usage-cost.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost
actors: [Person using the tool]
use-cases: [UC-05]
models: [PricedEvent, CostBreakdown, Report]
approved-by: human
approved-at: '2026-11-19T06:39:06+00:00'
---

# Ai usage cost Diagrams

Generated views of the Ai usage cost chunk; hand-laid views are added next to them.

## Hand-laid views

| Kind | Diagram | Question it answers |
|---|---|---|
| Conceptual model | [[Usage cost conceptual model]] | What are the things the tool talks about? |
| State | [[Cost state of a request]] | Which cost state can a request end in? |
| Sequence | [[Scan pipeline from logs to report]] | In what order do the parts work during a scan? |
| Decision flowchart | [[How one request is priced]] | What settles the price of one request? |
| Data flow | [[Usage data flow]] | Where does the data come from, rest and go? |
| BPMN | [[Scan and report process]] | What is the scan as a process between a person and the tool? |
| Mind map | [[Usage cost concepts]] | What is the core made of, in one picture? |
| API map | [[Usage cost HTTP routes]] | Which addresses does the dashboard call, and which ones change data? |
| Use case diagram | [[Usage cost goals]] | What can a person get done, and who else takes part? |
| Class diagram | [[Usage cost types]] | Which in memory types carry a request from log to report? |
| Data lineage | [[Where usage cost data comes from]] | Where does each stored table get its data, and who reads it? |
| Activity | [[Spend alert run]] | What happens in one run of the spend alert? |
| Timeline | [[Store schema versions]] | In what order did the store gain its tables and columns? |
| Gantt | [[Alert comparison windows]] | Which days does the alert compare? |
| Error flow | [[Usage cost refusals]] | How does the core refuse, and what does it absorb quietly? |
| Glossary map | [[Usage cost terms]] | How do the domain words relate? |
| Package tree | [[Usage cost folders]] | How is the package laid out on disk? |

The conceptual model also serves as the conceptual data model (kind erd-conceptual).

The container view below is the C4 view and the entity view is the physical model of the store.

## Components around Ai usage cost

%% generated:diagram-module-ch-localtokenomics-src-ai-usage-cost start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    subgraph g_src["src"]
        localtokenomics_src_ai_usage_cost["src/ai_usage_cost<br/>13 files, 5069 lines<br/>python"]:::system
        localtokenomics_src_ai_usage_cost_render["src/ai_usage_cost/render<br/>3 files, 187 lines<br/>python"]:::system
        localtokenomics_src_ai_usage_cost_sources["src/ai_usage_cost/sources<br/>22 files, 4722 lines<br/>python"]:::system
    end
    localtokenomics_src_ai_usage_cost --> localtokenomics_src_ai_usage_cost_sources
    localtokenomics_src_ai_usage_cost --> localtokenomics_src_ai_usage_cost_render
    localtokenomics_src_ai_usage_cost_render --> localtokenomics_src_ai_usage_cost
    localtokenomics_src_ai_usage_cost_sources --> localtokenomics_src_ai_usage_cost
    subgraph Legend
        direction LR
        zlegend_a["Component: part of this system"]:::system
        zlegend_b["Solid arrow: imports or calls"]:::system
        zlegend_a ~~~ zlegend_b
    end
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-module-ch-localtokenomics-src-ai-usage-cost end %%

## Entity relationship view of Ai usage cost

%% generated:diagram-er-ch-localtokenomics-src-ai-usage-cost start (do not edit; run brain docs generate) %%
```mermaid
erDiagram
    samples {
        TEXT machine
        TEXT sampled_at
        REAL gpu_util
        INTEGER vram_used
        INTEGER vram_total
        REAL power_w
        TEXT source
    }
    requests {
        TEXT fingerprint PK
        TEXT source
        TEXT client
        TEXT provider
        TEXT model
        TEXT session_id
        TEXT timestamp
        TEXT request_id
        INTEGER uncached_input
        INTEGER cache_read
        INTEGER cache_write_5m
        INTEGER cache_write_1h
        INTEGER output
        INTEGER reasoning_output
        INTEGER is_sidechain
        TEXT tier
        TEXT project
        TEXT working_directory
        TEXT repository
        TEXT branch
        TEXT machine
        TEXT source_file
        TEXT raw
        TEXT title
        TEXT title_source
        REAL reported_cost
    }
    files {
        TEXT path PK
        TEXT source
        REAL mtime
        INTEGER size
        TEXT ingested_at
        TEXT warnings
        INTEGER parser_version
        INTEGER ingested_offset
        TEXT boundary_hash
        TEXT title_seed
    }
    trace_events {
        TEXT span_id PK
        TEXT parent_id
        TEXT record_parent
        TEXT source
        TEXT session_id
        TEXT turn_id
        TEXT agent_id
        INTEGER is_sidechain
        INTEGER seq
        TEXT kind
        TEXT name
        TEXT model
        TEXT status
        TEXT started_at
        TEXT ended_at
        INTEGER duration_ms
        TEXT duration_provenance
        INTEGER ttft_ms
        INTEGER uncached_input
        INTEGER cache_read
        INTEGER cache_write_5m
        INTEGER cache_write_1h
        INTEGER output
        INTEGER reasoning_output
        TEXT tokens_provenance
        INTEGER context_capacity
        TEXT capacity_provenance
        INTEGER retry_attempt
        TEXT error
        TEXT source_file
        INTEGER record_offset
        INTEGER record_length
        TEXT content_path
        TEXT detail
    }
    outcomes {
        TEXT source PK
        TEXT session_id PK
        TEXT outcome
        TEXT notes
        TEXT tags
        TEXT updated_at
    }
    session_exclusions {
        TEXT source PK
        TEXT session_id PK
        TEXT excluded_at
    }
```
%% generated:diagram-er-ch-localtokenomics-src-ai-usage-cost end %%
