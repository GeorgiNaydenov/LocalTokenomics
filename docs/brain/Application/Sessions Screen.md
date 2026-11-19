---
title: Sessions Screen
aliases: []
tags: [ui, reference, screen-map]
area: application
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 5796e68c0471
chunk: ch-localtokenomics-web-src
---

# Sessions Screen

The Sessions view (web/src/Sessions.tsx): a sortable table of the sessions in the slice, cards on a phone. Its map is [[Sessions Screen Map]]; each numbered badge in the image is one row below.

## Screen map

| # | Element | What it does | Handler or target | State it depends on | Citation |
|---|---|---|---|---|---|
| 1 | `<SortSelect` sort | Select that sets the sort key and direction. | `onSortSelect` | - | [[web/src/Sessions.tsx]] `web/src/Sessions.tsx:286-289` |
| 2 | `<ColumnChooser` columns | Hides or shows table columns, remembered in the browser. | `toggleColumn` | desktop only, and only with rows | [[web/src/Sessions.tsx]] `web/src/Sessions.tsx:292-292` |
| 3 | `sorted.length === 0` empty section | Shows an empty state when the slice holds no session. | - | empty: `sorted.length === 0` | [[web/src/Sessions.tsx]] `web/src/Sessions.tsx:298-298` |
| 4 | `<SessionCard` phone cards | One card per session on a phone. | `onOpenSession` | phone width | [[web/src/Sessions.tsx]] `web/src/Sessions.tsx:306-323` |
| 5 | `<Table` sessions | Table of the shown sessions with the visible columns. | `shownColumns` | - | [[web/src/Sessions.tsx]] `web/src/Sessions.tsx:329-332` |
| 6 | `<SortButton` column header | Header button that sorts by its column or flips the direction. | `onHeaderSort` | - | [[web/src/Sessions.tsx]] `web/src/Sessions.tsx:338-343` |
| 7 | `<TableRow` session row | Clicking a row opens the session workspace. | `onOpenSession` | - | [[web/src/Sessions.tsx]] `web/src/Sessions.tsx:352-354` |
| 8 | `<PanelNote` row limit note | Says how many sessions are shown out of how many. | - | - | [[web/src/Sessions.tsx]] `web/src/Sessions.tsx:374-374` |

### Conditional sections

- empty: `sorted.length === 0`, callout 3, [[web/src/Sessions.tsx]] `web/src/Sessions.tsx:298-298`

## Diagnosis

The reader sorts, hides columns and opens a session. Sorting is local to the loaded report `web/src/Sessions.tsx:244-251`.

What can go wrong:

- Rows and cards are keyed and opened by session id only, so two sources with the same session id collide as React keys and open the same session `web/src/Sessions.tsx:307` `web/src/Sessions.tsx:323` `web/src/Sessions.tsx:353-354`.
- A table row opens the session on click only; it has no tab stop and no key handler, unlike the turn rows of the trace tab `web/src/Sessions.tsx:352-357` `web/src/TraceTab.tsx:683-694`.
- Beyond the row limit the remaining sessions cannot be reached except by narrowing the filters `web/src/Sessions.tsx:253` `web/src/Sessions.tsx:375-376`.

States not handled: there is no loading state of its own; a refetch keeps the old rows, and only the shell dims the count line `web/src/App.tsx:203` `web/src/App.tsx:322`.
