---
title: Economics Tab Screen
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

# Economics Tab Screen

The Economics tab of the session workspace (web/src/EconomicsTab.tsx): session totals, turn insights, and the per turn, per model and per tool tables. Its map is [[Economics Tab Screen Map]]; each numbered badge in the image is one row below.

## Screen map

| # | Element | What it does | Handler or target | State it depends on | Citation |
|---|---|---|---|---|---|
| 1 | `<Stat` Tokens | Session tokens, or a note that the client logs none. | - | - | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:615-615` |
| 2 | `<Stat` Cost | Session cost at list prices, or unavailable. | - | - | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:635-635` |
| 3 | `<Stat` Duration | Active time across turns. | - | - | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:663-663` |
| 4 | `<Stat` Calls | Model and tool calls with the error count. | - | - | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:674-674` |
| 5 | `<Stat` Retries | Extra attempts, absent when the reader logs none. | - | - | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:683-683` |
| 6 | `<Stat` Amplification | Input tokens per output token. | - | - | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:694-694` |
| 7 | `<Stat` Cache hit ratio | Share of input served from cache. | - | - | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:705-705` |
| 8 | `<Stat` Tokens per second | Output rate, only from measured values. | - | - | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:715-715` |
| 9 | `<Stat` Cost concentration and other cards | Insight cards that select a turn in the table. | `onSelectTurn` | - | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:439-444` |
| 10 | `cards.length === 0` empty section | Hides the strip when no insight applies. | - | empty: `cards.length === 0` | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:508-508` |
| 11 | `<SortSelect` Sort turns | Sorts all turns once they are shown. | `setSortKey` | shown only after Show all | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:555-561` |
| 12 | `<ColumnChooser` columns | Hides or shows turn columns. | `toggleColumn` | - | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:568-568` |
| 13 | `props.rows.length === 0` empty section | Empty state when no turn carries spans. | - | empty: `props.rows.length === 0` | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:573-573` |
| 14 | `<DataRows` turn rows | Turn table with the selected turn highlighted. | `selectedKey` | - | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:578-583` |
| 15 | `<Button` Show all | Shows every turn instead of the top ones. | `setShowAll` | - | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:588-588` |
| 16 | `<EconPanel` Per model | Per model table. | - | - | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:747-747` |
| 17 | `<EconPanel` Per tool | Per tool table. | - | - | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:758-758` |
| 18 | `props.rows.length === 0` empty section | Empty state of a per model or per tool table. | - | empty: `props.rows.length === 0` | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:402-402` |
| 19 | `<Button` Show more | Reveals the next batch of rows. | `setRevealed` | - | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:415-415` |

### Conditional sections

- empty: `cards.length === 0`, callout 10, [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:508-508`
- empty: `props.rows.length === 0`, callout 13, [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:573-573`
- empty: `props.rows.length === 0`, callout 18, [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:402-402`

## Diagnosis

The reader reads totals, picks an insight card to find a turn, and compares models and tools. Selecting a turn scrolls it into view `web/src/EconomicsTab.tsx:533-538`.

What can go wrong:

- On a phone the sort select and column chooser are not rendered, so the turn table keeps its default order `web/src/EconomicsTab.tsx:552` `web/src/EconomicsTab.tsx:579`.
- The exact value of the Cost figure uses the same rounding as the headline, unlike the overview which uses an exact format `web/src/EconomicsTab.tsx:645` `web/src/Overview.tsx:200`.

States not handled: there is no way back from Show all to the top turns `web/src/EconomicsTab.tsx:586-592`.
