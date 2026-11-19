---
title: Module Map Diagrams
aliases: []
tags: [c4, diagram, mermaid]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: []
sources: [docs/brain/architecture/diagrams/module-map.mmd]
node_citations:
  module-map:
    (root): ['web/eslint.config.js:1-25', 'web/vite.config.ts:1-31']
    src/ai_usage_cost: ['src/ai_usage_cost/__init__.py:1', 'src/ai_usage_cost/aggregate.py:1-723',
      'src/ai_usage_cost/api.py:1-404']
    src/ai_usage_cost/render: ['src/ai_usage_cost/render/__init__.py:1', 'src/ai_usage_cost/render/png.py:1-101',
      'src/ai_usage_cost/render/terminal.py:1-86']
    src/ai_usage_cost/sources: ['src/ai_usage_cost/sources/__init__.py:1-27', 'src/ai_usage_cost/sources/antigravity.py:1-314',
      'src/ai_usage_cost/sources/base.py:1-176']
    web/src: ['web/src/App.tsx:1-357', 'web/src/ContextTab.tsx:1-227', 'web/src/EconomicsTab.tsx:1-770']
    web/src/components: ['web/src/components/chart-hover.tsx:1-121', 'web/src/components/chart-time.tsx:1-184',
      'web/src/components/columns.tsx:1-95']
    web/src/components/ui: ['web/src/components/ui/accordion.tsx:1-65', 'web/src/components/ui/alert.tsx:1-65',
      'web/src/components/ui/badge.tsx:1-47']
    web/src/prototype: ['web/src/prototype/Gallery.tsx:1-659', 'web/src/prototype/OverviewScreen.tsx:1-386',
      'web/src/prototype/PricingScreen.tsx:1-218']
---

# Module Map Diagrams

Components and their dependencies, extracted from imports.

## Module dependency map

%% generated:diagram-module-map start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    subgraph g_root["root"]
        localtokenomics_root["(root)<br/>2 files, 1668 lines<br/>python"]:::system
        localtokenomics_root["(root)<br/>2 files, 56 lines<br/>typescript"]:::system
    end
    subgraph g_src["src"]
        localtokenomics_src_ai_usage_cost["src/ai_usage_cost<br/>13 files, 5069 lines<br/>python"]:::system
        localtokenomics_src_ai_usage_cost_render["src/ai_usage_cost/render<br/>3 files, 187 lines<br/>python"]:::system
        localtokenomics_src_ai_usage_cost_sources["src/ai_usage_cost/sources<br/>22 files, 4722 lines<br/>python"]:::system
    end
    subgraph g_web["web"]
        localtokenomics_web_src["web/src<br/>20 files, 7127 lines<br/>typescript"]:::system
        localtokenomics_web_src_components["web/src/components<br/>18 files, 3024 lines<br/>typescript"]:::system
        localtokenomics_web_src_components_ui["web/src/components/ui<br/>25 files, 2083 lines<br/>typescript"]:::system
        localtokenomics_web_src_prototype["web/src/prototype<br/>10 files, 3215 lines<br/>typescript"]:::system
    end
    localtokenomics_root --> localtokenomics_src_ai_usage_cost
    localtokenomics_src_ai_usage_cost --> localtokenomics_src_ai_usage_cost_sources
    localtokenomics_src_ai_usage_cost --> localtokenomics_src_ai_usage_cost_render
    localtokenomics_src_ai_usage_cost_render --> localtokenomics_src_ai_usage_cost
    localtokenomics_src_ai_usage_cost_sources --> localtokenomics_src_ai_usage_cost
    localtokenomics_web_src --> localtokenomics_web_src_components
    localtokenomics_web_src --> localtokenomics_web_src_components_ui
    localtokenomics_web_src_components --> localtokenomics_web_src
    localtokenomics_web_src_components --> localtokenomics_web_src_components_ui
    localtokenomics_web_src_components_ui --> localtokenomics_web_src
    localtokenomics_web_src_prototype --> localtokenomics_web_src_components
    localtokenomics_web_src_prototype --> localtokenomics_web_src_components_ui
    localtokenomics_web_src_prototype --> localtokenomics_web_src
    subgraph Legend
        direction LR
        zlegend_a["Component: part of this system"]:::system
        zlegend_b["Solid arrow: imports or calls"]:::system
        zlegend_a ~~~ zlegend_b
    end
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-module-map end %%

%% generated:node-citations-module-map start (do not edit; run brain docs generate) %%
### Node citations

- (root): `web/eslint.config.js:1-25`, `web/vite.config.ts:1-31`
- src/ai_usage_cost: `src/ai_usage_cost/__init__.py:1`, `src/ai_usage_cost/aggregate.py:1-723`, `src/ai_usage_cost/api.py:1-404`
- src/ai_usage_cost/render: `src/ai_usage_cost/render/__init__.py:1`, `src/ai_usage_cost/render/png.py:1-101`, `src/ai_usage_cost/render/terminal.py:1-86`
- src/ai_usage_cost/sources: `src/ai_usage_cost/sources/__init__.py:1-27`, `src/ai_usage_cost/sources/antigravity.py:1-314`, `src/ai_usage_cost/sources/base.py:1-176`
- web/src: `web/src/App.tsx:1-357`, `web/src/ContextTab.tsx:1-227`, `web/src/EconomicsTab.tsx:1-770`
- web/src/components: `web/src/components/chart-hover.tsx:1-121`, `web/src/components/chart-time.tsx:1-184`, `web/src/components/columns.tsx:1-95`
- web/src/components/ui: `web/src/components/ui/accordion.tsx:1-65`, `web/src/components/ui/alert.tsx:1-65`, `web/src/components/ui/badge.tsx:1-47`
- web/src/prototype: `web/src/prototype/Gallery.tsx:1-659`, `web/src/prototype/OverviewScreen.tsx:1-386`, `web/src/prototype/PricingScreen.tsx:1-218`
%% generated:node-citations-module-map end %%
