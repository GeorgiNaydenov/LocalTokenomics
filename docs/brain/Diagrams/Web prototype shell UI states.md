---
title: Web prototype shell UI states
aliases: []
tags: [diagram, mermaid, state-chart]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/prototype/**]
verified-against: f7104a42d355
sources: [docs/brain/architecture/diagrams/shell-ui-states.mmd]
chunk: ch-localtokenomics-web-src-prototype
authored: true
approved-by: human
approved-at: '2026-11-19T06:43:08+00:00'
---

# Web prototype shell UI states

This chart shows the modes the prototype header can be in: which screen is active and what happens when the design system tab is chosen. It points out that filters are lost on a visit to the design system and that no loading or error state exists. Both matter to anyone copying this behaviour.

## What the diagram shows

The shell starts on the overview tab `web/src/prototype/Prototype.tsx:22-22`.

A tab click sets the tab, and any tab can follow any other `web/src/prototype/Prototype.tsx:49-67`. The overview also moves to sources through its row button `web/src/prototype/Screens.tsx:361-361`.

The gallery tab swaps the screens component for the gallery `web/src/prototype/Prototype.tsx:98-107`. The screens component owns the filter state and the active session `web/src/prototype/Screens.tsx:277-278`, so leaving it for the gallery drops both, and returning starts from the initial filters.

The Filters button is drawn only when the tab is not the gallery `web/src/prototype/Prototype.tsx:70-79`.

No state waits for data: totals are literal and sessions are built when the module loads `web/src/prototype/data.ts:617-632` `web/src/prototype/data.ts:698-742`. The shell has no loading, empty or error state.

## Capability and related functionality

The capability is the behaviour of the five tab shell. The routes between states are drawn as a flow in [[Web prototype screen flow]], and the drawer has its own chart in [[Web prototype session drawer states]].

## Web prototype shell UI states

%% generated:diagram-shell-ui-states start (do not edit; run brain docs generate) %%
```mermaid
stateDiagram-v2
    direction LR
    [*] --> Overview: first render, tab starts as overview
    Overview --> Sessions: tab click
    Overview --> Sources: tab click or readers button
    Overview --> Pricing: tab click
    Sessions --> Overview: tab click
    Sessions --> Sources: tab click
    Sessions --> Pricing: tab click
    Sources --> Overview: tab click
    Sources --> Sessions: tab click
    Sources --> Pricing: tab click
    Pricing --> Overview: tab click
    Pricing --> Sessions: tab click
    Pricing --> Sources: tab click
    Overview --> Gallery: Design system tab
    Sessions --> Gallery: Design system tab
    Sources --> Gallery: Design system tab
    Pricing --> Gallery: Design system tab
    Gallery --> Overview: screen tab
    Gallery --> Sessions: screen tab
    Gallery --> Sources: screen tab
    Gallery --> Pricing: screen tab
    Gallery --> [*]
    note right of Gallery
        Screens is unmounted here, so filter state and any open drawer are lost. The Filters button is hidden.
    end note
    note right of Overview
        The four screens share one mounted Screens component, so filters stay while the tab changes. No loading, empty or error state exists because all data is literal.
    end note
    note left of Overview
        Legend, a rounded box is the active tab, an arrow label is the trigger, the filled dot is the start and the ringed dot is the end, a note records a rule that holds in that state.
    end note
```
%% generated:diagram-shell-ui-states end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/prototype/Prototype.tsx:20-29` | Tab, rail and scanning state |
> | `web/src/prototype/Prototype.tsx:98-107` | Gallery or screens |
> | `web/src/prototype/Screens.tsx:277-281` | Filter and drawer state kept in Screens |
> | `web/src/prototype/data.ts:698-742` | Sessions built at load |
