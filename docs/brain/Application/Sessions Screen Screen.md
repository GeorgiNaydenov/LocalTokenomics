---
title: Sessions Screen Screen
aliases: []
tags: [ui, reference, screen-map]
area: application
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/prototype/**]
verified-against: f7104a42d355
chunk: ch-localtokenomics-web-src-prototype
approved-by: human
approved-at: '2026-11-19T06:43:08+00:00'
---

# Sessions Screen Screen

The Sessions screen (`web/src/prototype/SessionsScreen.tsx:82-249`) and the session drawer it opens (`web/src/prototype/Screens.tsx:84-264`). The map is [[Sessions Screen Screen Map]]; each numbered badge in the image is one row below. Rows 1 to 12 belong to the screen, rows 13 to 26 to the drawer. The numbering follows the markup of each file, so it is not strictly the order on screen.

## Screen map

| # | Element | What it does | Handler or target | State it depends on | Citation |
|---|---|---|---|---|---|
| 1 | `<SortSelect` sort menu | Drop down that picks a sort key and direction from the shared option list; it works on both the table and the phone cards. | `onChange` (inline): splits the value into key and direction | `sortKey`, `sortDir`, `SORT_OPTIONS` | [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:115-123` |
| 2 | `isPhone` phone layout section | Switch between the phone card list and the desktop table at 639 px. | - | phone layout: `isPhone` | [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:127-147` |
| 3 | `<SessionCard` one card per session | Card for one session on narrow screens. It carries state, model, client, project, start, requests, tokens and cost, but not the outcome or error count. | `onOpen(session)` | `shown` | [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:130-145` |
| 4 | `<Table` sessions table | Desktop table with ten columns declared once in the column list. | - | - | [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:150` |
| 5 | `<SortButton` column header | Header button that sorts by its column; a second press on the same column flips the direction. | `onHeaderSort` | `sortKey`, `sortDir` | [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:155-161` |
| 6 | `<TableRow` session row | The whole row is clickable and opens the session drawer. The row has no keyboard handler and no tab stop. | `onOpen(session)` | `shown` | [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:168-172` |
| 7 | `<CostStateBadge` cost state | Badge that names how the cost was derived: priced, free, unpriced or unavailable. | - | `session.state` | [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:175` |
| 8 | `<OutcomeBadge` outcome | Badge with how the session ended. | - | `session.outcome` | [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:179` |
| 9 | `session.errorCount > 0` error section | Red count with an exclamation mark, drawn only for sessions that logged errors. | - | error: `session.errorCount > 0` | [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:180-196` |
| 10 | `<Tooltip` error count tooltip | Tooltip on the error count, reachable by hover or by keyboard focus on the count itself. | - | `session.errorCount` | [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:181-195` |
| 11 | `<TokenCell` token total and bar | Token total plus a bar scaled to the largest session on screen, coloured by cost state. | - | `tokenTotal(session)`, `maxTokens` | [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:220-224` |
| 12 | `<PanelNote` footer note | Note that says how many rows are shown and, when the list is cut, tells the user to narrow the filters. | - | `shown`, `sorted` | [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:242-246` |
| 13 | `<Sheet` session drawer | Side sheet that opens when a session is chosen and closes through its own close control. | `onClose` through `onOpenChange` | `session` (the active session) | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:94` |
| 14 | `<CostStateBadge` cost state in the drawer | Same cost state badge as the table, next to the big cost figure. | - | `session.state` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:114` |
| 15 | `<OutcomeBadge` outcome in the drawer | Outcome badge beside the cost state. | - | `session.outcome` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:115` |
| 16 | `session.tokens ?` conditional section | Token buckets section, drawn only when the client logged token counts. | - | conditional: `session.tokens ?` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:125-163` |
| 17 | `<BucketBar` token bucket bar | Stacked bar of the four token buckets. | - | `TOKEN_BUCKETS` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:127-135` |
| 18 | `<EmptyState` empty section | Empty state that explains why a client without token counts shows no tokens and no cost. | - | empty: `<EmptyState` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:165-168` |
| 19 | `session.traced ?` conditional section | Context window, trace, insights and capability blocks, drawn only for traced sessions; other sessions get a short explanation instead. | - | conditional: `session.traced ?` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:171-215` |
| 20 | `<ContextOccupancy` context window bars | One bar per model call, amber above 85 percent of the window. | - | `CONTEXT_SNAPSHOTS` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:181-186` |
| 21 | `<SpanTimeline` trace timeline | Indented list of the spans of a turn. | - | `TRACE_SPANS` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:195-205` |
| 22 | `<InsightList` insights | Three sample insights about context pressure, a retry and cache use. | - | `TRACE_INSIGHTS` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:209` |
| 23 | `<CapabilityGrid` what can be known here | Grid of what the source can tell: trace, tokens, cost, context and latency, each with its provenance. | - | `CAPABILITIES` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:213` |
| 24 | `<MetaGrid` where it came from | Thirteen facts about the session: client, provider, models, project, directory, repository, branch and more. | - | `session` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:227-246` |
| 25 | `<PathList` raw log files | Paths of the log files the session was read from. | - | `session.rawSource` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:250` |
| 26 | `<CodeBlock` reprice this model | A rate override line with zero prices, built from the first model name of the session. | - | `session.models` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:254-256` |

### Conditional sections

- phone layout: `isPhone`, callout 2, [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:127-147`
- error: `session.errorCount > 0`, callout 9, [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:180-196`
- conditional: `session.tokens ?`, callout 16, [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:125-163`
- empty: `<EmptyState`, callout 18, [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:165-168`
- conditional: `session.traced ?`, callout 19, [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:171-215`

## Diagnosis

**What the user can do.** Sort the list from the menu or, on a wide window, from any column header; the first press on a header sorts high to low and a second press on the same header flips the direction `web/src/prototype/SessionsScreen.tsx:99-105`. On a phone width the table is replaced by cards `web/src/prototype/SessionsScreen.tsx:127-147`. A click on a row or a card opens the drawer `web/src/prototype/SessionsScreen.tsx:168-172`, where the user reads the cost, the token buckets, the context window, the trace and the raw log paths `web/src/prototype/Screens.tsx:110-257`.

**What can go wrong.**

- The footer note tells the user to narrow the filters when the list is cut `web/src/prototype/SessionsScreen.tsx:243-244`, but the screen takes no filter value; its only prop is `onOpen` `web/src/prototype/SessionsScreen.tsx:82-82`, and the parent renders it without any filter `web/src/prototype/Screens.tsx:363-363`. The advice cannot be followed in the prototype. A port to real data must pass the filters in.
- The title counts all sessions while only the first rows are shown `web/src/prototype/SessionsScreen.tsx:96-96` `web/src/prototype/SessionsScreen.tsx:111-111`; the footer note is the only place that says the list is cut.
- The row is a click target with no key handler and no tab stop `web/src/prototype/SessionsScreen.tsx:168-172`. A keyboard user can reach only the error count, which has `tabIndex` set `web/src/prototype/SessionsScreen.tsx:183-184`. This is a gap for a screen that is meant to be the reference.
- The phone card receives no outcome and no error count `web/src/prototype/SessionsScreen.tsx:132-143`, so those two facts exist only in the table layout.
- A session without token counts gets a total of minus one for sorting `web/src/prototype/SessionsScreen.tsx:47-50`, and the same total is divided by the largest total to give the bar fraction `web/src/prototype/SessionsScreen.tsx:222-222`. That passes a negative fraction to the token cell for such sessions. Open question: does the shared token cell clamp it? The prototype code does not.
- A header click on a column such as client sets a sort value that has no entry in the option list `web/src/prototype/SessionsScreen.tsx:117-117` `web/src/prototype/data.ts:659-668`. How the menu then looks depends on the shared component and is not shown here.
- In the drawer, the context window, trace, insights and capabilities are fixed sample data, the same for every traced session `web/src/prototype/Screens.tsx:181-213`, and the split of cost across buckets uses fixed weights `web/src/prototype/Screens.tsx:50-55`. A reader must not take them as real numbers.

**States the code does not handle.**

- No loading state and no error state exist; the data is a literal list `web/src/prototype/SessionsScreen.tsx:20-20`.
- An empty list draws a table with headers and no rows and no empty message `web/src/prototype/SessionsScreen.tsx:166-237`.
- A failed trace is not a state: a session is either traced or it gets a text that it was recorded before span capture `web/src/prototype/Screens.tsx:216-224`.
- The drawer has an empty state only for a session with no token counts `web/src/prototype/Screens.tsx:164-169`.
