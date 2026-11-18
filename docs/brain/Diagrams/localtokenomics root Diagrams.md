---
title: localtokenomics root Diagrams
aliases: []
tags: [c4, diagram, mermaid]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/*]
verified-against: 696b7c3b3902
sources: [docs/brain/architecture/diagrams/module-ch-localtokenomics-root.mmd]
chunk: ch-localtokenomics-root
approved-by: human
approved-at: '2026-11-18T19:00:53+00:00'
---

# localtokenomics root Diagrams

Generated views of the localtokenomics root chunk; hand-laid views are added next to them.

## Components around localtokenomics root

%% generated:diagram-module-ch-localtokenomics-root start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    subgraph g_root["root"]
        localtokenomics_root["(root)<br/>2 files, 1668 lines<br/>python"]:::system
    end
    subgraph g_src["src"]
        localtokenomics_src_ai_usage_cost["src/ai_usage_cost<br/>13 files, 5069 lines<br/>python"]:::system
    end
    localtokenomics_root --> localtokenomics_src_ai_usage_cost
    subgraph Legend
        direction LR
        zlegend_a["Component: part of this system"]:::system
        zlegend_b["Solid arrow: imports or calls"]:::system
        zlegend_a ~~~ zlegend_b
    end
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-module-ch-localtokenomics-root end %%
