---
title: Web prototype module dependencies
aliases: []
tags: [diagram, mermaid, module-dependency]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/prototype/**]
verified-against: f7104a42d355
sources: [docs/brain/architecture/diagrams/prototype-imports.mmd]
chunk: ch-localtokenomics-web-src-prototype
authored: true
node_citations:
  prototype-imports:
    main: ['web/src/prototype/main.tsx:1-11']
    proto: ['web/src/prototype/Prototype.tsx:10-12']
    screens: ['web/src/prototype/Screens.tsx:25-39']
    rail: ['web/src/prototype/Rail.tsx:12-24']
    ov: ['web/src/prototype/OverviewScreen.tsx:25-35']
    se: ['web/src/prototype/SessionsScreen.tsx:20-20']
    so: ['web/src/prototype/SourcesScreen.tsx:6-6']
    pr: ['web/src/prototype/PricingScreen.tsx:18-18']
    ga: ['web/src/prototype/Gallery.tsx:82-90']
    data: ['web/src/prototype/data.ts:1-1']
    ext: ['web/src/prototype/Prototype.tsx:4-9']
approved-by: human
approved-at: '2026-11-19T06:43:08+00:00'
---

# Web prototype module dependencies

This view shows which files of the prototype import which, as layers from the entry script down to the sample data. Imports run in one direction and no cycle exists inside the folder. A developer can change a screen without worrying about hidden loops.

## What the diagram shows

The entry script imports the shell `web/src/prototype/main.tsx:5-5`. The shell imports the gallery, the screens component and the sample data `web/src/prototype/Prototype.tsx:10-12`.

The screens component imports the four screens, the filter rail and the sample data `web/src/prototype/Screens.tsx:25-39`.

Each screen imports only the sample data from its own folder `web/src/prototype/OverviewScreen.tsx:25-35` `web/src/prototype/SessionsScreen.tsx:20-20` `web/src/prototype/SourcesScreen.tsx:6-6` `web/src/prototype/PricingScreen.tsx:18-18`. The rail and the gallery do the same `web/src/prototype/Rail.tsx:12-24` `web/src/prototype/Gallery.tsx:82-90`.

The sample data file imports only type names from the shared API module `web/src/prototype/data.ts:1-1`.

Everything else comes from outside the folder: shared components, UI primitives, formatting, the theme and the design system `web/src/prototype/Prototype.tsx:4-9` `web/src/prototype/Screens.tsx:3-24`. The diagram groups them in one box. The folder level graph is in [[Web prototype Diagrams]].

## Capability and related functionality

The capability is a clear boundary: the prototype depends on the shared code, and [[Web prototype Overview]] states that no other chunk depends on it. The component view is [[Web prototype component tree]].

## Web prototype module dependencies

%% generated:diagram-prototype-imports start (do not edit; run brain docs generate) %%
```mermaid
flowchart TD
    subgraph entry["Entry"]
        main["main.tsx"]:::mod
    end
    subgraph shell["Shell"]
        proto["Prototype.tsx"]:::mod
        screens["Screens.tsx"]:::mod
        rail["Rail.tsx"]:::mod
    end
    subgraph pages["Pages"]
        ov["OverviewScreen.tsx"]:::mod
        se["SessionsScreen.tsx"]:::mod
        so["SourcesScreen.tsx"]:::mod
        pr["PricingScreen.tsx"]:::mod
        ga["Gallery.tsx"]:::mod
    end
    subgraph dataLayer["Data"]
        data["data.ts"]:::mod
    end
    ext["Outside the folder: components, ui, format, api, theme, design-system"]:::external

    main --> proto
    proto --> screens
    proto --> ga
    proto --> data
    screens --> ov
    screens --> se
    screens --> so
    screens --> pr
    screens --> rail
    screens --> data
    rail --> data
    ov --> data
    se --> data
    so --> data
    pr --> data
    ga --> data
    proto --> ext
    screens --> ext
    rail --> ext
    ov --> ext
    se --> ext
    so --> ext
    pr --> ext
    ga --> ext
    data --> ext

    subgraph Legend
        direction LR
        zl1["Box: a module, an arrow from A to B means A imports B"]:::mod
        zl2["Subgraph: a layer, imports point down the layers"]:::mod
        zl3["Grey dashed box: modules outside this folder, grouped in one box"]:::external
        zl4["Red arrow: a cycle. None exists inside this folder"]:::mod
        zl1 ~~~ zl2
        zl2 ~~~ zl3
        zl3 ~~~ zl4
    end

    classDef mod fill:#dae8fc,stroke:#222222,color:#111111
    classDef external fill:#e6e6e6,stroke:#222222,stroke-dasharray:5 3,color:#111111
```
%% generated:diagram-prototype-imports end %%

%% generated:node-citations-prototype-imports start (do not edit; run brain docs generate) %%
### Node citations

- main: `web/src/prototype/main.tsx:1-11`
- proto: `web/src/prototype/Prototype.tsx:10-12`
- screens: `web/src/prototype/Screens.tsx:25-39`
- rail: `web/src/prototype/Rail.tsx:12-24`
- ov: `web/src/prototype/OverviewScreen.tsx:25-35`
- se: `web/src/prototype/SessionsScreen.tsx:20-20`
- so: `web/src/prototype/SourcesScreen.tsx:6-6`
- pr: `web/src/prototype/PricingScreen.tsx:18-18`
- ga: `web/src/prototype/Gallery.tsx:82-90`
- data: `web/src/prototype/data.ts:1-1`
- ext: `web/src/prototype/Prototype.tsx:4-9`
%% generated:node-citations-prototype-imports end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/prototype/main.tsx:4-5` | Entry imports |
> | `web/src/prototype/Prototype.tsx:4-12` | Shell imports |
> | `web/src/prototype/Screens.tsx:25-39` | Screens imports |
> | `web/src/prototype/data.ts:1-1` | Type only import |
