---
title: Trace Tab Screen
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

# Trace Tab Screen

The Trace tab of the session workspace (web/src/TraceTab.tsx): timeline, agent tree and by turn modes, filters, insights and the span rows. Its map is [[Trace Tab Screen Map]]; each numbered badge in the image is one row below.

## Screen map

| # | Element | What it does | Handler or target | State it depends on | Citation |
|---|---|---|---|---|---|
| 1 | `<ToggleGroup` Timeline, Agent tree, By turn | Chooses the trace mode. | `setMode` | - | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:908-913` |
| 2 | `<ProvenanceBadge` capabilities | Badges saying what this reader reports for each capability. | - | - | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:924-924` |
| 3 | `<ToggleGroup` span kinds | Multi select of span kinds with counts. | `onKindsChange` | - | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:933-939` |
| 4 | `<Toggle` Errors only | Keeps only error spans. | `setErrorsOnly` | - | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:951-956` |
| 5 | `insights.length === 0` empty section | Hides the insights panel when there are none. | - | empty: `insights.length === 0` | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:266-266` |
| 6 | `<InsightList` insights | Findings that jump to their worst span. | `onSelectSpan` | - | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:278-290` |
| 7 | `turnRollups.length === 0` empty section | Empty state in By turn mode when no span has a turn. | - | empty: `turnRollups.length === 0` | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:978-978` |
| 8 | `<SortSelect` turn sort | Sorts the turn table. | `onSortChange` | - | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:665-665` |
| 9 | `<TableRow` turn row | Jumps to the turn in the timeline, by click or Enter. | `onJump` | - | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:683-689` |
| 10 | `<Button` Show all turns | Shows every turn. | `onShowAll` | - | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:742-742` |
| 11 | `shown.length === 0` empty section | Empty state when no span matches the filters. | - | empty: `shown.length === 0` | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:998-998` |
| 12 | `<SpanTimeline` span rows | Span rows with tokens, duration and status. | `selectSpan` | - | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:1007-1011` |
| 13 | `if (span.error) {` error section | A span with an error shows its error text. | - | error: `if (span.error) {` | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:829-829` |
| 14 | `<Button` Text, Hide | Loads and shows the text of a span. | `toggleContent` | - | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:876-881` |
| 15 | `<Button` Show more spans | Reveals the next batch of rows. | `setRevealed` | shown only while rows are hidden | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:1017-1017` |

### Conditional sections

- empty: `insights.length === 0`, callout 5, [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:266-266`
- empty: `turnRollups.length === 0`, callout 7, [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:978-978`
- empty: `shown.length === 0`, callout 11, [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:998-998`
- error: `if (span.error) {`, callout 13, [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:829-829`

## Diagnosis

The reader filters spans, focuses one from an insight or from the context tab, and opens span text. Focusing a span past the shown rows widens the row budget so it is drawn `web/src/TraceTab.tsx:768-771` `web/src/TraceTab.tsx:801-805`.

What can go wrong:

- A span text request that failed is stored as an error, and pressing Text again does not fetch it again because a stored state already exists `web/src/TraceTab.tsx:791` `web/src/TraceTab.tsx:795-797`.
- A 404 is detected by looking for the text 404 in the error message, which depends on the wording of the API helper `web/src/TraceTab.tsx:59-61` `web/src/api.ts:497`.
- A span focused from the context tab that the kind filter or errors only hides is not found in the rows, and nothing tells the reader why no row is highlighted `web/src/TraceTab.tsx:765-768`.

States not handled: there is no loading indicator per span text request beyond the stored loading state inside the content block `web/src/TraceTab.tsx:792` `web/src/TraceTab.tsx:836-838`.
