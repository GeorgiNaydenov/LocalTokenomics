---
title: Sessions Screen Map
aliases: []
tags: [diagram, drawio, screen-map]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
sources: [docs/brain/architecture/drawio/drawio-screen-sessions.drawio]
chunk: ch-localtokenomics-web-src
authored: true
screen-note: Sessions Screen
node_citations:
  drawio-screen-sessions:
    el-1: ['web/src/Sessions.tsx:286-289']
    el-2: ['web/src/Sessions.tsx:292-292']
    el-3: ['web/src/Sessions.tsx:298-298']
    el-4: ['web/src/Sessions.tsx:306-323']
    el-5: ['web/src/Sessions.tsx:329-332']
    el-6: ['web/src/Sessions.tsx:338-343']
    el-7: ['web/src/Sessions.tsx:352-354']
    el-8: ['web/src/Sessions.tsx:374-374']
    badge-1: ['web/src/Sessions.tsx:286-289']
    badge-2: ['web/src/Sessions.tsx:292-292']
    badge-3: ['web/src/Sessions.tsx:298-298']
    badge-4: ['web/src/Sessions.tsx:306-323']
    badge-5: ['web/src/Sessions.tsx:329-332']
    badge-6: ['web/src/Sessions.tsx:338-343']
    badge-7: ['web/src/Sessions.tsx:352-354']
    badge-8: ['web/src/Sessions.tsx:374-374']
    region-1: ['web/src/Sessions.tsx:286-289', 'web/src/Sessions.tsx:292-292']
    region-2: ['web/src/Sessions.tsx:298-298', 'web/src/Sessions.tsx:306-323', 'web/src/Sessions.tsx:329-332']
    region-3: ['web/src/Sessions.tsx:338-343', 'web/src/Sessions.tsx:352-354']
    region-4: ['web/src/Sessions.tsx:374-374']
---

# Sessions Screen Map

This map shows the list a reader uses to find one session and open it. It lets them sort, hide columns and see which sessions cost the most or failed. It also shows the cap on how many rows are drawn.

## What the diagram shows

- The header carries the sort select and, on wider screens with rows, the column chooser `web/src/Sessions.tsx:281-296`.
- The body is an empty state, phone cards or a table, in that order of checks `web/src/Sessions.tsx:298-371`.
- Each header cell is a sort button and each row opens the session `web/src/Sessions.tsx:338-345` `web/src/Sessions.tsx:352-356`.
- At most a fixed number of rows is drawn and the note says so `web/src/Sessions.tsx:48` `web/src/Sessions.tsx:373-379`.

## Capability and related functionality

Opening a row shows [[Session Workspace Screen]]. The row limit is the rule recorded in [[Web Specification]], and the view is reached from [[App Screen]]. The journey through it is drawn in [[Web User Journey]].

## Sessions Screen screen map

![[docs/brain/architecture/rendered/drawio-screen-sessions.svg]]

> [!example]- Code references
> | Badge | Element | Code |
> |---|---|---|
> | 1 | `<SortSelect` sort | `web/src/Sessions.tsx:286-289` |
> | 2 | `<ColumnChooser` columns | `web/src/Sessions.tsx:292-292` |
> | 3 | `sorted.length === 0` empty section | `web/src/Sessions.tsx:298-298` |
> | 4 | `<SessionCard` phone cards | `web/src/Sessions.tsx:306-323` |
> | 5 | `<Table` sessions | `web/src/Sessions.tsx:329-332` |
> | 6 | `<SortButton` column header | `web/src/Sessions.tsx:338-343` |
> | 7 | `<TableRow` session row | `web/src/Sessions.tsx:352-354` |
> | 8 | `<PanelNote` row limit note | `web/src/Sessions.tsx:374-374` |
