---
title: Shared components imports
aliases: []
tags: [diagram, mermaid, module-dependency]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/components/*]
sources: [docs/brain/architecture/diagrams/shared-components-imports.mmd]
chunk: ch-localtokenomics-web-src-components
authored: true
node_citations:
  shared-components-imports:
    session: ['web/src/components/session.tsx:117-205']
    source: ['web/src/components/source-card.tsx:33-64']
    trace: ['web/src/components/trace.tsx:227-315']
    chartTime: ['web/src/components/chart-time.tsx:23-184']
    states: ['web/src/components/states.tsx:68-96']
    filters: ['web/src/components/filters.tsx:18-54']
    columns: ['web/src/components/columns.tsx:62-95']
    detail: ['web/src/components/detail.tsx:6-26']
    status: ['web/src/components/status.tsx:149-165']
    sparkline: ['web/src/components/sparkline.tsx:89-145']
    panel: ['web/src/components/panel.tsx:5-13']
    stat: ['web/src/components/stat.tsx:61-155']
    hover: ['web/src/components/chart-hover.tsx:18-121']
    series: ['web/src/components/series.ts:3-5']
    info: ['web/src/components/metric-info.tsx:46-191']
    alone: ['web/src/components/rank.ts:13-15', 'web/src/components/use-media-query.ts:3-18', 'web/src/components/workspace-panel.ts:49-73']
    ui: ['web/src/components/columns.tsx:4-4', 'web/src/components/metric-info.tsx:8-8', 'web/src/components/chart-time.tsx:9-9']
    srcmods: ['web/src/components/status.tsx:3-6', 'web/src/components/session.tsx:2-2', 'web/src/components/states.tsx:17-17']
---

# Shared components imports

This graph shows which shared component files import which. It lets a developer see how far a change to a base file reaches before editing it. The graph also confirms that dependencies run one way, from big widgets down to small parts.

## What the diagram shows

The base layer holds the metric info box, the stat card, the hover frame and the series colours, and the stat card imports the info box. `web/src/components/stat.tsx:4-4` `web/src/components/sparkline.tsx:1-1`

The status badges and the page states also import the info box. `web/src/components/status.tsx:4-4` `web/src/components/states.tsx:15-15`

The detail helpers import the stat label, and so do the filters. `web/src/components/detail.tsx:4-4` `web/src/components/filters.tsx:15-15`

The page states import the code block, the panel parts and the info box. `web/src/components/states.tsx:13-14`

The source card imports the sparkline, the badges and the stat label, and the sparkline imports the hover frame. `web/src/components/source-card.tsx:4-6` `web/src/components/sparkline.tsx:1-1`

The session card imports the badge metadata, and the trace widgets import the hover frame, the badges and the stat label. `web/src/components/session.tsx:5-5` `web/src/components/trace.tsx:5-9`

The time chart imports the series colours and the key list from the badges. `web/src/components/chart-time.tsx:10-11`

The column chooser, the info box and the time chart import primitives from the UI folder. `web/src/components/columns.tsx:4-4` `web/src/components/metric-info.tsx:8-8` `web/src/components/chart-time.tsx:9-9`

The badges, the session card and the page states import the class helper, data types, formatters and pricing notes of the main web folder. `web/src/components/status.tsx:3-6` `web/src/components/session.tsx:2-2` `web/src/components/states.tsx:17-17`

The rank, media query and workspace panel files import nothing from their siblings, only from React and the data types. `web/src/components/rank.ts:1-1` `web/src/components/use-media-query.ts:1-1` `web/src/components/workspace-panel.ts:1-1`

No import cycle exists between the files of this folder: every arrow points from a higher layer to a lower one.

## Capability and related functionality

The graph realises the file level view of the shared display layer. The folder level view is [[Web UI components Diagrams]], the grouped view is [[Shared components C4]], and the render tree is [[Dashboard component composition]]. The primitives folder is described in [[Web ui UI components Overview]].


## Shared components imports

%% generated:diagram-shared-components-imports start (do not edit; run brain docs generate) %%
```mermaid
flowchart TD
    subgraph Top["Top layer: widgets that combine others"]
        session["session.tsx"]:::module
        source["source-card.tsx"]:::module
        trace["trace.tsx"]:::module
        chartTime["chart-time.tsx"]:::module
        states["states.tsx"]:::module
        filters["filters.tsx"]:::module
        columns["columns.tsx"]:::module
    end
    subgraph Mid["Middle layer"]
        detail["detail.tsx"]:::module
        status["status.tsx"]:::module
        sparkline["sparkline.tsx"]:::module
        panel["panel.tsx"]:::module
    end
    subgraph Base["Base layer"]
        stat["stat.tsx"]:::module
        hover["chart-hover.tsx"]:::module
        series["series.ts"]:::module
        info["metric-info.tsx"]:::module
    end
    alone["rank.ts, use-media-query.ts, workspace-panel.ts"]:::module
    ui["components/ui"]:::external
    srcmods["design-system, api, format, pricing-notes"]:::external

    status --> info
    stat --> info
    states --> info
    states --> detail
    states --> panel
    detail --> stat
    filters --> stat
    source --> sparkline
    source --> status
    source --> stat
    sparkline --> hover
    session --> status
    trace --> hover
    trace --> status
    trace --> stat
    chartTime --> series
    chartTime --> status
    Top --> ui
    Base --> ui
    Top --> srcmods
    Mid --> srcmods
    Base --> srcmods
    alone --> srcmods

    subgraph Legend
        direction LR
        zlegend_a["Module: one file"]:::module
        zlegend_b["Outside this chunk"]:::external
        zlegend_c["Red arrow: import cycle, none found here"]:::cycle
        zlegend_a ~~~ zlegend_b ~~~ zlegend_c
    end

    classDef module fill:#dae8fc,stroke:#222222,color:#222222
    classDef external fill:#f5f5f5,stroke:#666666,color:#222222,stroke-dasharray:5 3
    classDef cycle fill:#f8cecc,stroke:#b85450,color:#222222
```
%% generated:diagram-shared-components-imports end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/components/stat.tsx:4-4` | Stat card imports the info box |
> | `web/src/components/states.tsx:13-14` | Page states imports |
> | `web/src/components/source-card.tsx:4-6` | Source card imports |
> | `web/src/components/trace.tsx:5-9` | Trace imports |
> | `web/src/components/chart-time.tsx:10-11` | Time chart imports |
> | `web/src/components/chart-time.tsx:9-9` | Chart primitives import |
> | `web/src/components/rank.ts:1-1` | Rank imports |
