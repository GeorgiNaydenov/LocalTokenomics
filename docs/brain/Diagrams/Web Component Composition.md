---
title: Web Component Composition
aliases: []
tags: [diagram, mermaid, component-tree]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
sources: [docs/brain/architecture/diagrams/web-ui-composition.mmd]
chunk: ch-localtokenomics-web-src
authored: true
node_citations:
  web-ui-composition:
    'main': ['web/src/main.tsx:7-12']
    'App': ['web/src/App.tsx:129-129']
    'Header': ['web/src/App.tsx:292-304']
    'FilterRail': ['web/src/App.tsx:307-318']
    'FilterChips': ['web/src/App.tsx:327-327']
    'OfflineCard': ['web/src/App.tsx:255-259']
    'Overview': ['web/src/App.tsx:331-331']
    'Sessions': ['web/src/App.tsx:334-334']
    'Sources': ['web/src/App.tsx:336-336']
    'Pricing': ['web/src/App.tsx:338-338']
    'SessionWorkspace': ['web/src/App.tsx:343-352']
    'Sheet': ['web/src/FilterRail.tsx:486-486', 'web/src/SessionWorkspace.tsx:620-620']
    'Tabs': ['web/src/SessionWorkspace.tsx:536-551']
    'OutcomeControl': ['web/src/SessionWorkspace.tsx:533-533']
    'SummaryTab': ['web/src/SessionWorkspace.tsx:555-555']
    'LoadableTab': ['web/src/SessionWorkspace.tsx:379-379']
    'TraceTab': ['web/src/SessionWorkspace.tsx:564-564']
    'EconomicsTab': ['web/src/SessionWorkspace.tsx:575-580']
    'ContextTab': ['web/src/SessionWorkspace.tsx:591-591']
    'EmptyState': ['web/src/Sessions.tsx:299-299', 'web/src/TraceTab.tsx:980-980', 'web/src/ContextTab.tsx:166-166']
---

# Web Component Composition

This picture shows which part of the dashboard draws which other part. It helps a developer find where a piece of the screen lives before changing it. Shared parts are drawn once, so a reader sees how far a change to one of them reaches.

## What the diagram shows

- The entry file mounts the App component inside a tooltip provider `web/src/main.tsx:7-12`.
- App renders the header, the filter rail, the filter chips, the offline and error cards, one of four views and the workspace `web/src/App.tsx:255-255` `web/src/App.tsx:274-274` `web/src/App.tsx:292-304` `web/src/App.tsx:307-318` `web/src/App.tsx:327-327` `web/src/App.tsx:330-340` `web/src/App.tsx:343-352`.
- The filter rail renders its content twice, as a docked aside and inside a sheet `web/src/FilterRail.tsx:477-503`.
- The workspace renders the outcome control, the tab list and a loading wrapper around the trace, economics and context tabs `web/src/SessionWorkspace.tsx:533-533` `web/src/SessionWorkspace.tsx:536-596`.
- Sessions, Trace and Context render the shared empty state `web/src/Sessions.tsx:299-299` `web/src/TraceTab.tsx:980-980` `web/src/ContextTab.tsx:166-166`.

## Capability and related functionality

The composition sits under [[App Screen]] and the screen notes such as [[Session Workspace Screen]]. The C4 view of the same code is [[Web Dashboard Components]] and the folders are in [[Web Package Tree]].

## Web Component Composition

%% generated:diagram-web-ui-composition start (do not edit; run brain docs generate) %%
```mermaid
flowchart TD
    main(["main.tsx entry"]):::entry --> App
    App["App"]:::page
    App --> Header["Header"]:::shared
    App --> FilterRail["FilterRail"]:::shared
    App --> FilterChips["FilterChips"]:::lib
    App --> OfflineCard["OfflineCard, ErrorState"]:::lib
    App --> Overview["Overview"]:::page
    App --> Sessions["Sessions"]:::page
    App --> Sources["Sources"]:::page
    App --> Pricing["Pricing"]:::page
    App --> SessionWorkspace["SessionWorkspace"]:::page
    FilterRail --> Sheet["Sheet"]:::third
    SessionWorkspace --> Sheet
    SessionWorkspace --> Tabs["Tabs"]:::third
    SessionWorkspace --> OutcomeControl["OutcomeControl"]:::shared
    SessionWorkspace --> SummaryTab["SummaryTab"]:::shared
    SessionWorkspace --> LoadableTab["LoadableTab"]:::shared
    LoadableTab --> TraceTab["TraceTab"]:::shared
    LoadableTab --> EconomicsTab["EconomicsTab"]:::shared
    LoadableTab --> ContextTab["ContextTab"]:::shared
    Sessions --> EmptyState["EmptyState"]:::lib
    TraceTab --> EmptyState
    ContextTab --> EmptyState
    subgraph Legend
        direction LR
        zl1["Page: thick border"]:::page
        zl2["Component of this chunk"]:::shared
        zl3["Shared component from web/src/components"]:::lib
        zl4["Third party primitive, dashed"]:::third
        zl5(["Entry point"]):::entry
        zl6["Arrow reads: renders"]:::lib
    end
    classDef page fill:#dae8fc,stroke:#222222,stroke-width:3px,color:#142233
    classDef shared fill:#dae8fc,stroke:#222222,color:#142233
    classDef lib fill:#ffffff,stroke:#222222,color:#222222
    classDef third fill:#eeeeee,stroke:#666666,stroke-dasharray:4 3,color:#222222
    classDef entry fill:#fff2cc,stroke:#222222,color:#222222
```
%% generated:diagram-web-ui-composition end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/main.tsx:7-12` | The entry file mounts the App component inside a tooltip provider |
> | `web/src/App.tsx:255-255` | App renders the header, the filter rail, the filter chips, the offline and error cards, one of four views and the workspace |
> | `web/src/App.tsx:274-274` | App renders the header, the filter rail, the filter chips, the offline and error cards, one of four views and the workspace |
> | `web/src/App.tsx:292-304` | App renders the header, the filter rail, the filter chips, the offline and error cards, one of four views and the workspace |
> | `web/src/App.tsx:307-318` | App renders the header, the filter rail, the filter chips, the offline and error cards, one of four views and the workspace |
> | `web/src/App.tsx:327-327` | App renders the header, the filter rail, the filter chips, the offline and error cards, one of four views and the workspace |
> | `web/src/App.tsx:330-340` | App renders the header, the filter rail, the filter chips, the offline and error cards, one of four views and the workspace |
> | `web/src/App.tsx:343-352` | App renders the header, the filter rail, the filter chips, the offline and error cards, one of four views and the workspace |
> | `web/src/FilterRail.tsx:477-503` | The filter rail renders its content twice, as a docked aside and inside a sheet |
> | `web/src/SessionWorkspace.tsx:533-533` | The workspace renders the outcome control, the tab list and a loading wrapper around the trace, economics and context tabs |
> | `web/src/SessionWorkspace.tsx:536-596` | The workspace renders the outcome control, the tab list and a loading wrapper around the trace, economics and context tabs |
> | `web/src/Sessions.tsx:299-299` | Sessions, Trace and Context render the shared empty state |
> | `web/src/TraceTab.tsx:980-980` | Sessions, Trace and Context render the shared empty state |
> | `web/src/ContextTab.tsx:166-166` | Sessions, Trace and Context render the shared empty state |
