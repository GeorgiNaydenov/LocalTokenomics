---
title: Web Dashboard Components
aliases: []
tags: [c4, diagram, mermaid]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*]
verified-against: 02d21a1926f6
sources: [docs/brain/architecture/diagrams/web-src-dashboard-c4.mmd]
chunk: ch-localtokenomics-web-src
authored: true
node_citations:
  web-src-dashboard-c4:
    '["Person': ['web/src/main.tsx:7-13']
    ai-usage-cost server: ['web/src/api.ts:489-500']
    App: ['web/src/App.tsx:129-145']
    api.ts: ['web/src/api.ts:489-512']
    Overview, Sessions, Sources, Pricing: ['web/src/App.tsx:330-339']
    SessionWorkspace: ['web/src/SessionWorkspace.tsx:433-474']
    format, pricing-notes, pricing-format, turn-insights: ['web/src/format.ts:19-27',
      'web/src/pricing-notes.ts:27-34', 'web/src/pricing-format.ts:83-90', 'web/src/turn-insights.ts:73-82']
    theme.ts: ['web/src/theme.ts:56-69']
    Browser local storage: ['web/src/theme.ts:12-33']
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Web Dashboard Components

This view shows how the local dashboard is put together, from the person reading it to the server that holds the numbers. It lets a new team member see which part loads data, which part shows it and which part only formats it. It also makes clear that the page itself calculates nothing and only asks the server.

## What the diagram shows

- The person opens the page, which mounts one top level component inside a tooltip provider `web/src/main.tsx:7-13`.
- That component loads the metadata, the rate table and the report, and holds the query, the view and the open session `web/src/App.tsx:132-145` `web/src/App.tsx:166-201`.
- All network calls go through one module of typed helpers that talk to the local server over relative paths `web/src/api.ts:489-512`.
- The component shows one of four views, overview, sessions, sources or pricing, once their data has arrived `web/src/App.tsx:330-339`.
- Opening a session shows the workspace with four tabs, and each tab fetches its own data from the same helper module when first requested `web/src/SessionWorkspace.tsx:72-77` `web/src/SessionWorkspace.tsx:457-474`.
- The views and the workspace use small pure modules for money, token and date formatting, price notes, price text and per turn insights `web/src/format.ts:19-27` `web/src/pricing-notes.ts:27-34` `web/src/pricing-format.ts:83-90` `web/src/turn-insights.ts:73-82`.
- The theme module reads the saved choice from browser local storage and writes it back when the mode changes `web/src/theme.ts:12-33` `web/src/theme.ts:42-47`.

## Capability and related functionality

The diagram realises the usage and cost dashboard. It sits above [[Web Overview]], which lists every file and explains the data flow in prose, and next to the generated module view in [[Web Diagrams]]. The tests behind the pure modules are listed in [[Web Tests]].

## Diagram

%% generated:diagram-web-src-dashboard-c4 start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    person(["Person<br/>reads usage and cost"]):::person
    server["ai-usage-cost server<br/>external, not in this chunk<br/>JSON over HTTP"]:::external
    subgraph dash["Web dashboard (web/src, React and TypeScript)"]
        app["App<br/>component<br/>state, loading, refresh"]:::system
        api["api.ts<br/>module<br/>typed fetch helpers"]:::system
        views["Overview, Sessions, Sources, Pricing<br/>components<br/>four views"]:::system
        ws["SessionWorkspace<br/>component<br/>Summary, Trace, Economics, Context"]:::system
        helpers["format, pricing-notes, pricing-format, turn-insights<br/>modules<br/>pure display rules"]:::system
        theme["theme.ts<br/>module<br/>light or dark mode"]:::system
    end
    store[("Browser local storage<br/>theme choice")]:::data
    person --> app
    app --> api
    app --> views
    app --> ws
    views --> helpers
    ws --> api
    ws --> helpers
    app --> theme
    api -.-> server
    theme -.-> store
    subgraph Legend
        direction LR
        zlegend_a(["Stadium: a person"]):::person
        zlegend_b["Rounded box: part of this system"]:::system
        zlegend_c["Dashed grey box: external system"]:::external
        zlegend_d[("Cylinder: data store")]:::data
        zlegend_e["Solid arrow: call or use. Dashed arrow: network or storage access"]:::system
        zlegend_a ~~~ zlegend_b
        zlegend_b ~~~ zlegend_c
        zlegend_c ~~~ zlegend_d
        zlegend_d ~~~ zlegend_e
    end
    classDef system fill:#dae8fc,stroke:#222222,color:#142233
    classDef person fill:#fff2cc,stroke:#222222,color:#222222
    classDef external fill:#eeeeee,stroke:#222222,stroke-dasharray:5 3,color:#222222
    classDef data fill:#d5e8d4,stroke:#222222,color:#142233
```
%% generated:diagram-web-src-dashboard-c4 end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/main.tsx:7-13` | The entry point mounts the app |
> | `web/src/App.tsx:166-201` | Metadata, rates and report loading |
> | `web/src/api.ts:489-512` | The single fetch helper and the metadata and rate endpoints |
> | `web/src/App.tsx:330-339` | The four views |
> | `web/src/SessionWorkspace.tsx:457-474` | Lazy loading of the workspace tabs |
> | `web/src/theme.ts:12-33` | Theme choice kept in local storage |
