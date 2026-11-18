---
title: Ai usage cost sources Diagrams
aliases: []
tags: [c4, diagram, mermaid]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/sources/**]
verified-against: 8a1d896ab1c8
sources: [docs/brain/architecture/diagrams/module-ch-localtokenomics-src-ai-usage-cost-sources.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost-sources
approved-by: human
approved-at: '2026-11-18T19:05:23+00:00'
---

# Ai usage cost sources Diagrams

Generated views of the Ai usage cost sources chunk; hand-laid views are added next to them.

## Components around Ai usage cost sources

%% generated:diagram-module-ch-localtokenomics-src-ai-usage-cost-sources start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    subgraph g_src["src"]
        localtokenomics_src_ai_usage_cost_sources["src/ai_usage_cost/sources<br/>22 files, 4722 lines<br/>python"]:::system
        localtokenomics_src_ai_usage_cost["src/ai_usage_cost<br/>13 files, 5069 lines<br/>python"]:::system
    end
    localtokenomics_src_ai_usage_cost_sources --> localtokenomics_src_ai_usage_cost
    localtokenomics_src_ai_usage_cost --> localtokenomics_src_ai_usage_cost_sources
    subgraph Legend
        direction LR
        zlegend_a["Component: part of this system"]:::system
        zlegend_b["Solid arrow: imports or calls"]:::system
        zlegend_a ~~~ zlegend_b
    end
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-module-ch-localtokenomics-src-ai-usage-cost-sources end %%
