---
title: Web prototype screen flow
aliases: []
tags: [diagram, mermaid, screen-flow]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/prototype/**]
verified-against: f7104a42d355
sources: [docs/brain/architecture/diagrams/prototype-navigation.mmd]
chunk: ch-localtokenomics-web-src-prototype
authored: true
node_citations:
  prototype-navigation:
    start: ['web/prototype.html:25-25']
    overview: ['web/src/prototype/Prototype.tsx:22-22']
    sessions: ['web/src/prototype/Prototype.tsx:16-16']
    sources: ['web/src/prototype/Screens.tsx:361-361']
    pricing: ['web/src/prototype/Screens.tsx:43-48']
    gallery: ['web/src/prototype/Prototype.tsx:98-107']
    drawer: ['web/src/prototype/Screens.tsx:84-264']
    railsheet: ['web/src/prototype/Rail.tsx:264-273']
    rescan: ['web/src/prototype/Prototype.tsx:26-29']
    theme: ['web/src/prototype/Prototype.tsx:87-94']
approved-by: human
approved-at: '2026-11-19T06:43:08+00:00'
---

# Web prototype screen flow

This diagram shows how a person moves between the screens of the prototype. Every screen is one click from every other, and the only deeper steps are the session drawer and the filters sheet. A designer can hold it next to the real dashboard and compare the paths.

## What the diagram shows

The page opens on the overview tab `web/src/prototype/Prototype.tsx:22-22`.

Each header tab calls the tab setter, so any tab reaches any other, including the design system page `web/src/prototype/Prototype.tsx:49-67` `web/src/prototype/Prototype.tsx:16-16`.

A row button on the overview moves the user to the sources tab `web/src/prototype/OverviewScreen.tsx:76-82`. The screens component supplies that move `web/src/prototype/Screens.tsx:361-361`.

A click on a session row opens the drawer `web/src/prototype/SessionsScreen.tsx:168-172`, and the chosen session is kept as the active one `web/src/prototype/Screens.tsx:363-363`. Closing the sheet clears it `web/src/prototype/Screens.tsx:94-94` `web/src/prototype/Screens.tsx:375-375`.

The Filters button appears on every tab but the gallery and is hidden on wide windows `web/src/prototype/Prototype.tsx:70-79`. It opens a left sheet that holds the filter content `web/src/prototype/Rail.tsx:264-273`.

Rescan logs disables its button for 900 milliseconds and reads nothing `web/src/prototype/Prototype.tsx:26-29` `web/src/prototype/Prototype.tsx:83-86`. The theme button flips between light and dark `web/src/prototype/Prototype.tsx:87-94`.

## Capability and related functionality

The capability is navigation between the four reference screens and the design system page. The structure of the pages is in [[Web prototype sitemap]], the states behind the moves are in [[Web prototype shell UI states]], and the journey of a developer is in [[Web prototype user journey]].

## Web prototype screen flow

%% generated:diagram-prototype-navigation start (do not edit; run brain docs generate) %%
```mermaid
flowchart TD
    start(["Developer opens prototype.html"]):::person
    overview["Overview tab: default screen"]:::screen
    sessions["Sessions tab"]:::screen
    sources["Sources tab"]:::screen
    pricing["Models and pricing tab"]:::screen
    gallery["Design system tab: Gallery"]:::screen
    drawer["Session drawer: sheet over Sessions"]:::overlay
    railsheet["Filters sheet: narrow windows, any dashboard screen"]:::overlay
    rescan["Rescan logs: any screen, button disabled for 900 ms"]:::action
    theme["Theme toggle: any screen, light or dark"]:::action

    start --> overview
    overview -->|"header tab click"| sessions
    overview -->|"header tab click"| sources
    overview -->|"header tab click"| pricing
    overview -->|"header tab click"| gallery
    sessions -->|"header tab click"| overview
    sources -->|"header tab click"| overview
    pricing -->|"header tab click"| overview
    gallery -->|"header tab click"| overview
    overview -.->|"more readers button"| sources
    sessions -->|"row or card click"| drawer
    drawer -->|"close"| sessions
    overview -->|"Filters button below lg"| railsheet
    railsheet -->|"close"| overview
    overview -->|"Rescan logs"| rescan
    rescan -->|"after 900 ms"| overview
    overview -->|"theme button"| theme
    theme -->|"mode switches"| overview

    subgraph Legend
        direction LR
        zl1(["Yellow pill: the person who starts"]):::person
        zl2["Blue box: a screen reached from the header tabs"]:::screen
        zl3["Purple box: an overlay that opens above a screen"]:::overlay
        zl4["Orange box: a header action that stays on the same screen"]:::action
        zl5["Solid arrow: user action. Dashed arrow: a shortcut inside a screen"]:::screen
        zl1 ~~~ zl2
        zl2 ~~~ zl3
        zl3 ~~~ zl4
        zl4 ~~~ zl5
    end

    classDef person fill:#fff2cc,stroke:#222222,color:#111111
    classDef screen fill:#dae8fc,stroke:#222222,color:#111111
    classDef overlay fill:#e1d5e7,stroke:#222222,color:#111111
    classDef action fill:#ffe6cc,stroke:#222222,color:#111111
```
%% generated:diagram-prototype-navigation end %%

%% generated:node-citations-prototype-navigation start (do not edit; run brain docs generate) %%
### Node citations

- start: `web/prototype.html:25-25`
- overview: `web/src/prototype/Prototype.tsx:22-22`
- sessions: `web/src/prototype/Prototype.tsx:16-16`
- sources: `web/src/prototype/Screens.tsx:361-361`
- pricing: `web/src/prototype/Screens.tsx:43-48`
- gallery: `web/src/prototype/Prototype.tsx:98-107`
- drawer: `web/src/prototype/Screens.tsx:84-264`
- railsheet: `web/src/prototype/Rail.tsx:264-273`
- rescan: `web/src/prototype/Prototype.tsx:26-29`
- theme: `web/src/prototype/Prototype.tsx:87-94`
%% generated:node-citations-prototype-navigation end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/prototype/Prototype.tsx:49-67` | Header tabs |
> | `web/src/prototype/OverviewScreen.tsx:76-82` | Shortcut to Sources |
> | `web/src/prototype/SessionsScreen.tsx:168-172` | Row click opens the drawer |
> | `web/src/prototype/Screens.tsx:361-375` | Shortcut wiring and drawer close |
> | `web/src/prototype/Rail.tsx:264-273` | Filters sheet |
> | `web/src/prototype/Prototype.tsx:26-29` | Staged rescan |
