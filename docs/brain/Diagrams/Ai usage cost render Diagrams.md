---
title: Ai usage cost render Diagrams
aliases: []
tags: [c4, diagram, mermaid]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/render/**]
verified-against: 15259010c74a
sources: [docs/brain/architecture/diagrams/module-ch-localtokenomics-src-ai-usage-cost-render.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost-render
approved-by: human
approved-at: '2026-11-19T06:47:07+00:00'
---

# Ai usage cost render Diagrams

Generated views of the Ai usage cost render chunk; hand-laid views are added next to them.

## Components around Ai usage cost render

%% generated:diagram-module-ch-localtokenomics-src-ai-usage-cost-render start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    subgraph g_src["src"]
        localtokenomics_src_ai_usage_cost_render["src/ai_usage_cost/render<br/>3 files, 187 lines<br/>python"]:::system
        localtokenomics_src_ai_usage_cost["src/ai_usage_cost<br/>13 files, 5069 lines<br/>python"]:::system
    end
    localtokenomics_src_ai_usage_cost_render --> localtokenomics_src_ai_usage_cost
    localtokenomics_src_ai_usage_cost --> localtokenomics_src_ai_usage_cost_render
    subgraph Legend
        direction LR
        zlegend_a["Component: part of this system"]:::system
        zlegend_b["Solid arrow: imports or calls"]:::system
        zlegend_a ~~~ zlegend_b
    end
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-module-ch-localtokenomics-src-ai-usage-cost-render end %%
