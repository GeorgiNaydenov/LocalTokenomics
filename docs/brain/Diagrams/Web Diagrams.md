---
title: Web Diagrams
aliases: []
tags: [c4, diagram, mermaid]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
sources: [docs/brain/architecture/diagrams/module-ch-localtokenomics-web-src.mmd]
chunk: ch-localtokenomics-web-src
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Web Diagrams

Generated views of the Web chunk; hand-laid views are added next to them.

## Components around Web

%% generated:diagram-module-ch-localtokenomics-web-src start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    subgraph g_web["web"]
        localtokenomics_web_src["web/src<br/>20 files, 7127 lines<br/>typescript"]:::system
        localtokenomics_web_src_components["web/src/components<br/>18 files, 3024 lines<br/>typescript"]:::system
        localtokenomics_web_src_components_ui["web/src/components/ui<br/>25 files, 2083 lines<br/>typescript"]:::system
    end
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
%% generated:diagram-module-ch-localtokenomics-web-src end %%

## Hand-laid views

Screens, each with a numbered screen map and a callout table: [[App Screen]], [[Overview Screen]], [[Sessions Screen]], [[Sources Screen]], [[Pricing Screen]], [[Session Workspace Screen]], [[Trace Tab Screen]], [[Context Tab Screen]] and [[Economics Tab Screen]].

Structure and navigation: [[Web Dashboard Components]], [[Web Component Composition]], [[Web Package Tree]], [[Web Sitemap]], [[Web Screen Flow]], [[Web User Journey]], [[Web Concept Map]] and [[Web Glossary Map]].

Forms, tables and dialogs: [[Web Outcome Form Wireframe]], [[Web Filter Rail Wireframe]], [[Web Sessions Table Wireframe]], [[Web Rate Table Wireframe]] and [[Web Workspace Panel Wireframe]].

States and failures: [[Web App Load State Chart]], [[Web Workspace State Chart]], [[Web Outcome Save State Chart]], [[Web Trace State Chart]], [[Web Sessions Table State Chart]] and [[Web Error Flow]].
