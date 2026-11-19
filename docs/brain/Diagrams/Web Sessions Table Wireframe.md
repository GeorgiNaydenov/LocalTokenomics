---
title: Web Sessions Table Wireframe
aliases: []
tags: [diagram, drawio, wireframe]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
sources: [docs/brain/architecture/drawio/drawio-web-sessions-table.drawio]
chunk: ch-localtokenomics-web-src
authored: true
node_citations:
  drawio-web-sessions-table:
    panel: ['web/src/Sessions.tsx:235-239']
    s-title: ['web/src/Sessions.tsx:235-239']
    s-sort: ['web/src/Sessions.tsx:235-239']
    s-cols: ['web/src/Sessions.tsx:235-239']
    s-table: ['web/src/Sessions.tsx:235-239']
    h1: ['web/src/Sessions.tsx:235-239']
    h2: ['web/src/Sessions.tsx:235-239']
    h3: ['web/src/Sessions.tsx:235-239']
    h4: ['web/src/Sessions.tsx:235-239']
    h5: ['web/src/Sessions.tsx:235-239']
    h6: ['web/src/Sessions.tsx:235-239']
    h7: ['web/src/Sessions.tsx:235-239']
    h8: ['web/src/Sessions.tsx:235-239']
    h9: ['web/src/Sessions.tsx:235-239']
    h10: ['web/src/Sessions.tsx:235-239']
    h11: ['web/src/Sessions.tsx:235-239']
    s-row1: ['web/src/Sessions.tsx:235-239']
    s-row2: ['web/src/Sessions.tsx:235-239']
    s-note: ['web/src/Sessions.tsx:235-239']
    s-empty: ['web/src/Sessions.tsx:235-239']
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Web Sessions Table Wireframe

This wireframe shows the table a reader uses to find one session. It names every column and shows that each header sorts and each row opens the session. It also shows the line that warns when not all sessions are listed.

## What the diagram shows

- The header holds the title, the sort select and the column chooser `web/src/Sessions.tsx:281-290`.
- The columns are state, outcome, session, client, model, project, started, requests, errors, tokens and cost `web/src/Sessions.tsx:124-124` `web/src/Sessions.tsx:212-212`.
- Each header is a sort button and each row opens the workspace `web/src/Sessions.tsx:338-345` `web/src/Sessions.tsx:354-354`.
- A note under the table says how many rows are shown `web/src/Sessions.tsx:374-378`.
- An empty slice shows an empty state instead of the table `web/src/Sessions.tsx:298-302`.

## Capability and related functionality

The table's states are in [[Web Sessions Table State Chart]], and it sits on [[Sessions Screen]]. The row limit is a rule in [[Web Specification]].

## Web Sessions Table Wireframe

![[docs/brain/architecture/rendered/drawio-web-sessions-table.svg]]

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/Sessions.tsx:281-290` | The header holds the title, the sort select and the column chooser |
> | `web/src/Sessions.tsx:124-124` | The columns are state, outcome, session, client, model, project, started, requests, errors, tokens and cost |
> | `web/src/Sessions.tsx:212-212` | The columns are state, outcome, session, client, model, project, started, requests, errors, tokens and cost |
> | `web/src/Sessions.tsx:338-345` | Each header is a sort button and each row opens the workspace |
> | `web/src/Sessions.tsx:354-354` | Each header is a sort button and each row opens the workspace |
> | `web/src/Sessions.tsx:374-378` | A note under the table says how many rows are shown |
> | `web/src/Sessions.tsx:298-302` | An empty slice shows an empty state instead of the table |
