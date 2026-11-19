---
title: Web Sessions Table State Chart
aliases: []
tags: [diagram, mermaid, state-chart]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
sources: [docs/brain/architecture/diagrams/web-sessions-view.mmd]
chunk: ch-localtokenomics-web-src
authored: true
node_citations:
  web-sessions-view:
    Empty: ['web/src/Sessions.tsx:298-298']
    Cards: ['web/src/Sessions.tsx:306-306']
    Table: ['web/src/Sessions.tsx:329-329']
    Capped: ['web/src/Sessions.tsx:253-253']
    WorkspaceOpen: ['web/src/Sessions.tsx:354-354']
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Web Sessions Table State Chart

This chart shows the shapes the session list can take. It helps a reader understand why they may see cards, a table or a message, and why some sessions are not listed. It also shows that opening any row leads to the session workspace.

## What the diagram shows

- An empty slice shows an empty state, a phone shows cards, and a wider screen shows the table `web/src/Sessions.tsx:298-327`.
- A header press sorts by its column or flips the direction `web/src/Sessions.tsx:259-262`.
- Only the first rows up to the limit are drawn, and the note says how many are hidden `web/src/Sessions.tsx:48-48` `web/src/Sessions.tsx:375-377`.
- A row or a card opens the workspace `web/src/Sessions.tsx:323-323` `web/src/Sessions.tsx:354-354`.

## Capability and related functionality

The chart belongs to [[Sessions Screen]] and its table is drawn in [[Web Sessions Table Wireframe]]. Opening a row leads to [[Session Workspace Screen]].

## Web Sessions Table State Chart

%% generated:diagram-web-sessions-view start (do not edit; run brain docs generate) %%
```mermaid
stateDiagram-v2
    direction LR
    [*] --> Empty: no session in the slice
    [*] --> Cards: sessions, phone width
    [*] --> Table: sessions, wider screen
    Table --> Table: header pressed, sort or flip direction
    Table --> Capped: more than the row limit
    Cards --> Capped: more than the row limit
    Table --> WorkspaceOpen: row clicked
    Cards --> WorkspaceOpen: card opened
    Capped --> WorkspaceOpen: row clicked
    note right of Capped
        Not handled: rows past the limit are reachable only by narrowing the filters.
    end note
    note left of Empty
        Legend: the filled dot starts, a rounded box is a state of the sessions list, an arrow is labelled with the condition or event in the code, a note marks a gap.
    end note
```
%% generated:diagram-web-sessions-view end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/Sessions.tsx:298-327` | An empty slice shows an empty state, a phone shows cards, and a wider screen shows the table |
> | `web/src/Sessions.tsx:259-262` | A header press sorts by its column or flips the direction |
> | `web/src/Sessions.tsx:48-48` | Only the first rows up to the limit are drawn, and the note says how many are hidden |
> | `web/src/Sessions.tsx:375-377` | Only the first rows up to the limit are drawn, and the note says how many are hidden |
> | `web/src/Sessions.tsx:323-323` | A row or a card opens the workspace |
> | `web/src/Sessions.tsx:354-354` | A row or a card opens the workspace |
