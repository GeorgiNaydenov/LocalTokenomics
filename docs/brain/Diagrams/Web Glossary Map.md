---
title: Web Glossary Map
aliases: []
tags: [diagram, mermaid, glossary-map]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
sources: [docs/brain/architecture/diagrams/web-terms.mmd]
chunk: ch-localtokenomics-web-src
authored: true
node_citations:
  web-terms:
    report: ['web/src/api.ts:264-287']
    session: ['web/src/api.ts:215-240']
    state: ['web/src/api.ts:61-61']
    outcome: ['web/src/api.ts:82-82']
    trace: ['web/src/api.ts:195-202']
    span: ['web/src/api.ts:84-114']
    turn: ['web/src/TraceTab.tsx:566-566']
    unatt: ['web/src/EconomicsTab.tsx:8-8']
    snap: ['web/src/api.ts:124-137']
    prov: ['web/src/api.ts:63-63']
    priced: ['web/src/api.ts:61-61']
    rate: ['web/src/api.ts:471-480']
    est: ['web/src/Pricing.tsx:62-68']
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Web Glossary Map

This map shows the words the dashboard uses and how they relate. It helps a reader understand that a session has a cost state, an outcome and a trace made of spans grouped into turns. The same words appear on every screen.

## What the diagram shows

- The report carries the sessions of the slice, each with a cost state, its other states and an outcome `web/src/api.ts:215-240`.
- A cost state is one of priced, free, unpriced or unavailable `web/src/api.ts:61-61`.
- A provenance word says where a figure came from `web/src/api.ts:63-63`.
- A trace holds spans, and spans are grouped by turn, with spans outside any turn in their own row `web/src/api.ts:195-202` `web/src/TraceTab.tsx:566-566`.
- A context snapshot is one model call with its occupancy and provenance `web/src/api.ts:124-137`.
- An estimated rate prices a model from a sibling row `web/src/Pricing.tsx:62-68`.

## Capability and related functionality

The glossary entries Cost state, Provenance, Estimated rate, Session outcome and Unattributed turn are in [[Web Specification]]. The concepts are grouped by concern in [[Web Concept Map]], and the data shapes are in [[Web Data Model]].

## Web Glossary Map

%% generated:diagram-web-terms start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    report("Report"):::term -->|has many| session("Session"):::term
    session -->|has| state("Cost state"):::term
    session -->|has| outcome("Session outcome"):::term
    session -->|has| trace("Trace"):::term
    trace -->|has many| span("Span"):::term
    span -->|belongs to| turn("Turn"):::term
    turn -.->|is a, when no turn id| unatt("Unattributed turn"):::term
    session -->|has many| snap("Context snapshot"):::term
    snap -->|has| prov("Provenance"):::term
    span -->|has| prov
    state -->|is a| priced("priced, free, unpriced, unavailable"):::term
    rate("Rate table"):::term -->|prices| session
    rate -->|is a, from a sibling row| est("Estimated rate"):::term
    subgraph Legend
        direction LR
        zl1("Rounded box: a term as the code names it"):::term
        zl2["Solid arrow: has, belongs to, prices or is a"]:::term
        zl3["Dashed arrow: a special case"]:::term
    end
    classDef term fill:#dae8fc,stroke:#222222,color:#142233
```
%% generated:diagram-web-terms end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/api.ts:215-240` | The report carries the sessions of the slice, each with a cost state, its other states and an outcome |
> | `web/src/api.ts:61-61` | A cost state is one of priced, free, unpriced or unavailable |
> | `web/src/api.ts:63-63` | A provenance word says where a figure came from |
> | `web/src/api.ts:195-202` | A trace holds spans, and spans are grouped by turn, with spans outside any turn in their own row |
> | `web/src/TraceTab.tsx:566-566` | A trace holds spans, and spans are grouped by turn, with spans outside any turn in their own row |
> | `web/src/api.ts:124-137` | A context snapshot is one model call with its occupancy and provenance |
> | `web/src/Pricing.tsx:62-68` | An estimated rate prices a model from a sibling row |
