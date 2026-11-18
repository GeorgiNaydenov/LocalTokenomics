---
title: Web prototype Diagrams
aliases: []
tags: [c4, diagram, mermaid]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/prototype/**]
verified-against: b3afa144f2c4
sources: [docs/brain/architecture/diagrams/module-ch-localtokenomics-web-src-prototype.mmd]
chunk: ch-localtokenomics-web-src-prototype
approved-by: human
approved-at: '2026-11-18T18:48:18+00:00'
---

# Web prototype Diagrams

Generated views of the Web prototype chunk; hand-laid views are added next to them.

## Components around Web prototype

%% generated:diagram-module-ch-localtokenomics-web-src-prototype start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    subgraph g_web["web"]
        localtokenomics_web_src_prototype["web/src/prototype<br/>10 files, 3215 lines<br/>typescript"]:::system
        localtokenomics_web_src["web/src<br/>20 files, 7127 lines<br/>typescript"]:::system
        localtokenomics_web_src_components["web/src/components<br/>18 files, 3024 lines<br/>typescript"]:::system
        localtokenomics_web_src_components_ui["web/src/components/ui<br/>25 files, 2083 lines<br/>typescript"]:::system
    end
    localtokenomics_web_src_prototype --> localtokenomics_web_src_components
    localtokenomics_web_src_prototype --> localtokenomics_web_src_components_ui
    localtokenomics_web_src_prototype --> localtokenomics_web_src
    localtokenomics_web_src --> localtokenomics_web_src_components
    localtokenomics_web_src --> localtokenomics_web_src_components_ui
    localtokenomics_web_src_components --> localtokenomics_web_src
    localtokenomics_web_src_components --> localtokenomics_web_src_components_ui
    localtokenomics_web_src_components_ui --> localtokenomics_web_src
    subgraph Legend
        direction LR
        zlegend_a["Component: part of this system"]:::system
        zlegend_b["Solid arrow: imports or calls"]:::system
        zlegend_a ~~~ zlegend_b
    end
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-module-ch-localtokenomics-web-src-prototype end %%
