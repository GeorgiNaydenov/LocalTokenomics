---
title: Dashboard component composition
aliases: []
tags: [component-tree, diagram, mermaid]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/components/*]
sources: [docs/brain/architecture/diagrams/dashboard-component-composition.mmd]
chunk: ch-localtokenomics-web-src-components
authored: true
node_citations:
  dashboard-component-composition:
    pages: ['web/src/Overview.tsx:20-20', 'web/src/Sessions.tsx:17-17', 'web/src/Sources.tsx:7-7', 'web/src/App.tsx:17-17', 'web/src/ContextTab.tsx:9-9']
    stat: ['web/src/components/stat.tsx:61-155']
    source: ['web/src/components/source-card.tsx:33-64']
    session: ['web/src/components/session.tsx:117-205']
    timechart: ['web/src/components/chart-time.tsx:23-184']
    warnings: ['web/src/components/states.tsx:247-278']
    offline: ['web/src/components/states.tsx:280-328']
    errorstate: ['web/src/components/states.tsx:98-121']
    occupancy: ['web/src/components/trace.tsx:45-212']
    info: ['web/src/components/metric-info.tsx:46-191']
    ticker: ['web/src/components/stat.tsx:14-47']
    spark: ['web/src/components/sparkline.tsx:89-145']
    hover: ['web/src/components/chart-hover.tsx:18-121']
    outcome: ['web/src/components/status.tsx:220-236']
    keylist: ['web/src/components/status.tsx:324-344']
    row: ['web/src/components/states.tsx:202-245']
    code: ['web/src/components/detail.tsx:54-65']
    panel: ['web/src/components/panel.tsx:5-13']
    chartbox: ['web/src/components/chart-time.tsx:99-99']
    popover: ['web/src/components/metric-info.tsx:114-114']
---

# Dashboard component composition

This tree shows which shared component draws which other component. It helps a developer see that one hover frame and one info box serve many parts, so a fix there reaches every screen. It also marks where the tree ends at the basic interface parts.

## What the diagram shows

The dashboard pages place the shared components: the overview page uses the stat card, the source card and the time chart, the sessions page uses the session card, the sources page uses the warnings list, the context tab uses the occupancy bars and the app shell uses the offline and error cards. `web/src/Overview.tsx:20-20` `web/src/Sessions.tsx:17-17` `web/src/Sources.tsx:7-7` `web/src/App.tsx:17-17` `web/src/ContextTab.tsx:9-9`

A stat card renders the info box next to its label and a number ticker for a numeric value. `web/src/components/stat.tsx:101-101` `web/src/components/stat.tsx:114-114`

A source card renders a sparkline, and both the sparkline and the context occupancy bars render the hover frame, so pointer and keyboard inspection is written once. `web/src/components/source-card.tsx:49-49` `web/src/components/sparkline.tsx:132-132` `web/src/components/trace.tsx:75-75`

A session card renders the outcome badge, and every signal badge that has a hint is wrapped by the info box. `web/src/components/session.tsx:161-161` `web/src/components/status.tsx:139-139`

The time chart renders the chart container and the key list of series. `web/src/components/chart-time.tsx:174-174` `web/src/components/chart-time.tsx:99-99`

The warnings list renders one row per group, and each row puts the info box on its severity dot. `web/src/components/states.tsx:273-273` `web/src/components/states.tsx:211-211`

The offline card renders a code block with the start command inside a panel, and the error card renders a panel with a title, a message and an optional retry button. `web/src/components/states.tsx:317-317` `web/src/components/states.tsx:305-305` `web/src/components/states.tsx:110-110`

The info box opens its content in a popover from the UI primitives. `web/src/components/metric-info.tsx:114-114`

## Capability and related functionality

The tree realises how the shared display layer composes cards, charts and badges. Imports between files are in [[Shared components imports]], the grouping is in [[Shared components C4]], and the vocabulary is in [[Shared components concepts]]. The primitives are described in [[Web ui UI components Overview]] and the tests in [[Web UI components Tests]].


## Dashboard component composition

%% generated:diagram-dashboard-component-composition start (do not edit; run brain docs generate) %%
```mermaid
flowchart TD
    pages["Dashboard pages"]:::page
    stat["Stat"]:::shared
    source["SourceCard"]:::shared
    session["SessionCard"]:::shared
    timechart["TimeChart"]:::shared
    warnings["WarningsList"]:::shared
    offline["OfflineCard"]:::shared
    errorstate["ErrorState"]:::shared
    occupancy["ContextOccupancy"]:::shared
    info["MetricInfo"]:::shared
    ticker["NumberTicker"]:::shared
    spark["Sparkline"]:::shared
    hover["HoverFrame"]:::shared
    outcome["OutcomeBadge"]:::shared
    keylist["Legend list"]:::shared
    row["WarningGroupRow"]:::shared
    code["CodeBlock"]:::shared
    panel["Panel"]:::shared
    chartbox["ChartContainer"]:::third
    popover["Popover"]:::third

    pages --> stat
    pages --> source
    pages --> session
    pages --> timechart
    pages --> warnings
    pages --> offline
    pages --> errorstate
    pages --> occupancy
    stat --> info
    stat --> ticker
    source --> spark
    spark --> hover
    occupancy --> hover
    session --> outcome
    outcome --> info
    timechart --> keylist
    timechart --> chartbox
    warnings --> row
    row --> info
    offline --> code
    offline --> panel
    errorstate --> panel
    info --> popover

    subgraph Legend
        direction LR
        zlegend_a["Page: thick border"]:::page
        zlegend_b["Shared component"]:::shared
        zlegend_c["Primitive from components/ui"]:::third
    end

    classDef page fill:#dae8fc,stroke:#222222,color:#222222,stroke-width:4px
    classDef shared fill:#dae8fc,stroke:#222222,color:#222222
    classDef third fill:#f5f5f5,stroke:#666666,color:#222222,stroke-dasharray:5 3
```
%% generated:diagram-dashboard-component-composition end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/Overview.tsx:20-20` | Overview page imports |
> | `web/src/App.tsx:17-17` | App shell imports of the offline and error cards |
> | `web/src/components/stat.tsx:61-155` | Stat card |
> | `web/src/components/sparkline.tsx:132-132` | Sparkline using the hover frame |
> | `web/src/components/status.tsx:139-139` | Signal badge wrapped by the info box |
> | `web/src/components/chart-time.tsx:99-99` | Chart container in the time chart |
> | `web/src/components/states.tsx:202-245` | Warning group row |
> | `web/src/components/states.tsx:317-317` | Offline card code block |
