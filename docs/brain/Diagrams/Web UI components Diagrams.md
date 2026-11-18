---
title: Web UI components Diagrams
aliases: []
tags: [c4, diagram, mermaid]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/components/*]
verified-against: 4a002de17be5
sources: [docs/brain/architecture/diagrams/module-ch-localtokenomics-web-src-components.mmd]
chunk: ch-localtokenomics-web-src-components
node_citations:
  module-ch-localtokenomics-web-src-components:
    web/src/components: ['web/src/components/status.tsx:1-454', 'web/src/components/trace.tsx:1-435']
    web/src: ['web/src/components/status.tsx:3-6']
    web/src/components/ui: ['web/src/components/columns.tsx:4-12']
approved-by: human
approved-at: '2026-11-18T19:03:01+00:00'
---

# Web UI components Diagrams

This view shows how the shared dashboard building blocks sit between the main web application and the lower-level interface primitives. It helps a reader see which direction dependencies run before changing a shared card, badge or chart.

## What the diagram shows

- The centre box is the set of shared dashboard components: stat cards, badges, charts, filters and session views `web/src/components/status.tsx:1-454`.
- An arrow from the components to the main web application exists because the badges import the data types, the design helper and the pricing notes from it `web/src/components/status.tsx:3-6`.
- An arrow from the components to the primitives box exists because the column chooser builds on the shared button and dropdown menu `web/src/components/columns.tsx:4-12`.
- An arrow from the main web application back to the components exists because the app screens import filters, stat cards and states from them `web/src/App.tsx:15-17`.
- An arrow from the primitives to the main web application exists because the button primitive uses the shared class name helper `web/src/components/ui/button.tsx:3`.

## Capability and related functionality

The diagram realises the shared display layer of the dashboard. The written explanation is in [[Web UI components Overview]], and the tests that guard it are in [[Web UI components Tests]]. The neighbouring modules are Web Overview and Web ui UI components Overview.

> [!example]- Code references
> | Code | Role |
> |---|---|
> | `web/src/components/status.tsx:3-6` | Imports from the main web application |
> | `web/src/components/columns.tsx:4-12` | Imports from the primitives |
> | `web/src/App.tsx:15-17` | Application imports of the components |
> | `web/src/components/ui/button.tsx:3` | Primitive importing the shared helper |

## Components around Web UI components

%% generated:diagram-module-ch-localtokenomics-web-src-components start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    subgraph g_web["web"]
        localtokenomics_web_src_components["web/src/components<br/>18 files, 3024 lines<br/>typescript"]:::system
        localtokenomics_web_src["web/src<br/>20 files, 7127 lines<br/>typescript"]:::system
        localtokenomics_web_src_components_ui["web/src/components/ui<br/>25 files, 2083 lines<br/>typescript"]:::system
    end
    localtokenomics_web_src_components --> localtokenomics_web_src
    localtokenomics_web_src_components --> localtokenomics_web_src_components_ui
    localtokenomics_web_src --> localtokenomics_web_src_components
    localtokenomics_web_src --> localtokenomics_web_src_components_ui
    localtokenomics_web_src_components_ui --> localtokenomics_web_src
    subgraph Legend
        direction LR
        zlegend_a["Component: part of this system"]:::system
        zlegend_b["Solid arrow: imports or calls"]:::system
        zlegend_a ~~~ zlegend_b
    end
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-module-ch-localtokenomics-web-src-components end %%
