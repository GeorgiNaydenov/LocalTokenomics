---
title: Ai usage cost Diagrams
aliases: []
tags: [c4, diagram, erd, mermaid]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [src/ai_usage_cost/*]
sources: [docs/brain/architecture/diagrams/module-ch-localtokenomics-src-ai-usage-cost.mmd,
  docs/brain/architecture/diagrams/er-ch-localtokenomics-src-ai-usage-cost.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost
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
