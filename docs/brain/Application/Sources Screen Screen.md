---
title: Sources Screen Screen
aliases: []
tags: [ui, reference, screen-map]
area: application
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/prototype/**]
verified-against: 5796e68c0471
chunk: ch-localtokenomics-web-src-prototype
---

# Sources Screen Screen

The Sources screen (`web/src/prototype/SourcesScreen.tsx:8-95`). The map is [[Sources Screen Screen Map]]; each numbered badge in the image is one row below.

## Screen map

| # | Element | What it does | Handler or target | State it depends on | Citation |
|---|---|---|---|---|---|
| 1 | `<PanelHeader` readers with data | Title that counts readers with logs and how many of them have token counts. | - | `detected`, `withTokens` | [[web/src/prototype/SourcesScreen.tsx]] `web/src/prototype/SourcesScreen.tsx:16-19` |
| 2 | `<SourceDetail` one block per detected reader | Detail block with path, clients, headline, trend and four stats: files, sessions, requests and last event. | - | `detected` | [[web/src/prototype/SourcesScreen.tsx]] `web/src/prototype/SourcesScreen.tsx:22-46` |
| 3 | `undetected.length > 0` conditional section | Collapsible block, drawn only when some readers found nothing on this machine. | - | conditional: `undetected.length > 0` | [[web/src/prototype/SourcesScreen.tsx]] `web/src/prototype/SourcesScreen.tsx:51-80` |
| 4 | `<DisclosurePanel` available, not detected here | Disclosure that opens the list of readers that found nothing. | - | `undetected` | [[web/src/prototype/SourcesScreen.tsx]] `web/src/prototype/SourcesScreen.tsx:52-57` |
| 5 | `<div` one row per missing reader | Row with the reader label, its log path and its root hint. | - | `undetected` | [[web/src/prototype/SourcesScreen.tsx]] `web/src/prototype/SourcesScreen.tsx:60-72` |
| 6 | `SCAN_WARNINGS.length > 0` conditional section | Scan warnings panel, drawn only when the last scan left warnings. | - | conditional: `SCAN_WARNINGS.length > 0` | [[web/src/prototype/SourcesScreen.tsx]] `web/src/prototype/SourcesScreen.tsx:82-92` |
| 7 | `<PanelHeader` scan warnings | Title that counts the file and parse warnings. | - | `SCAN_WARNINGS` | [[web/src/prototype/SourcesScreen.tsx]] `web/src/prototype/SourcesScreen.tsx:84-87` |
| 8 | `<WarningsList` warnings | List of the warnings, passed as one hand built group of kind other. | - | `SCAN_WARNINGS` | [[web/src/prototype/SourcesScreen.tsx]] `web/src/prototype/SourcesScreen.tsx:89` |

### Conditional sections

- conditional: `undetected.length > 0`, callout 3, [[web/src/prototype/SourcesScreen.tsx]] `web/src/prototype/SourcesScreen.tsx:51-80`
- conditional: `SCAN_WARNINGS.length > 0`, callout 6, [[web/src/prototype/SourcesScreen.tsx]] `web/src/prototype/SourcesScreen.tsx:82-92`

## Diagnosis

**What the user can do.** Read one detail block per reader that found logs, with path, clients, headline and four counts `web/src/prototype/SourcesScreen.tsx:15-49`. Open a folded block to see the readers that found nothing and where each one looks `web/src/prototype/SourcesScreen.tsx:51-80`. Read the warnings of the last scan `web/src/prototype/SourcesScreen.tsx:82-92`. The screen has no controls that change data.

**What can go wrong.**

- A reader without token counts shows its request count as the headline instead of a cost `web/src/prototype/SourcesScreen.tsx:31-33`. The copy says elsewhere that cost is never invented, so this is deliberate, but the headline then mixes two units on one list.
- The warnings panel builds one fixed group of kind other for all warnings `web/src/prototype/SourcesScreen.tsx:89-89`. The real scan groups warnings by kind with a severity and a worst example, so this prototype does not show how grouping looks.
- The detail block gets an empty footer text `web/src/prototype/SourcesScreen.tsx:34-34`, so the layout of a footer is not demonstrated.
- The disclosure promises that an undetected reader appears everywhere on the next scan `web/src/prototype/SourcesScreen.tsx:73-76`. The Rescan logs button of the shell reads no logs, so the promise cannot be tried in the prototype `web/src/prototype/Prototype.tsx:26-29`.

**States the code does not handle.**

- No loading state while a scan runs, and no error state when a scan fails; the page changes nothing during the staged rescan `web/src/prototype/Prototype.tsx:26-29`.
- No empty state for zero detected readers: the first panel would show a title that counts zero and an empty list `web/src/prototype/SourcesScreen.tsx:15-49`.
