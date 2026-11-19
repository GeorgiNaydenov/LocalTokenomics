---
title: Overview Screen
aliases: []
tags: [ui, reference, screen-map]
area: application
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
chunk: ch-localtokenomics-web-src
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Overview Screen

The Overview view (web/src/Overview.tsx): readers found, headline figures, outcomes, heaviest sessions, the time chart and the cost, token, cache and project panels. Its map is [[Overview Screen Map]]; each numbered badge in the image is one row below.

## Screen map

| # | Element | What it does | Handler or target | State it depends on | Citation |
|---|---|---|---|---|---|
| 1 | `<SourceCard` reader cards | One card per top reader with its cost or request count and a trend line. | `shown` | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:117-117` |
| 2 | `<button` more readers | Opens the Sources view when more readers exist than are shown. | `onSelectView` | shown only while readers are hidden | [[web/src/Overview.tsx]] `web/src/Overview.tsx:151-153` |
| 3 | `<Stat` API equivalent cost | Total list price cost of the slice with a daily sparkline. | - | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:193-193` |
| 4 | `<Stat` Tokens | Total tokens with the cache read share. | - | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:223-223` |
| 5 | `<Stat` Requests | Logged requests and the files they came from. | - | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:246-246` |
| 6 | `<Stat` Sessions | Distinct sessions with the average cost. | - | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:265-265` |
| 7 | `<Stat` Cache saved | Saving against full input price, or unavailable when nothing is priced. | - | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:284-284` |
| 8 | `<Stat` Flagged | Scan warning count that opens Sources when above zero. | `onSelectView` | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:325-329` |
| 9 | `<Stat` Success rate | Share of rated sessions marked successful. | - | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:362-362` |
| 10 | `<Stat` Tokens per success | Average tokens of successful sessions. | - | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:377-377` |
| 11 | `<Stat` Cost per success | Average priced cost of successful sessions. | - | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:392-392` |
| 12 | `<HeavyRow` Most expensive | The six costliest priced sessions. | - | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:472-472` |
| 13 | `byCost.length === 0` empty section | Says nothing can be ranked when no session is priced. | - | empty: `byCost.length === 0` | [[web/src/Overview.tsx]] `web/src/Overview.tsx:479-479` |
| 14 | `<HeavyRow` Longest log span | The six sessions with the longest log span. | - | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:492-492` |
| 15 | `bySpan.length === 0` empty section | Says no session has a usable span. | - | empty: `bySpan.length === 0` | [[web/src/Overview.tsx]] `web/src/Overview.tsx:499-499` |
| 16 | `<ToggleGroup` Client, Provider, Model | Chooses what the daily bars are stacked by. | `setStackBy` | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:554-559` |
| 17 | `<ToggleGroup` Cost, Tokens | Chooses the metric of the bars. | `setMetric` | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:565-570` |
| 18 | `rows.length === 0` empty section | Shows an empty state when the slice has no requests. | - | empty: `rows.length === 0` | [[web/src/Overview.tsx]] `web/src/Overview.tsx:579-579` |
| 19 | `<TimeChart` daily bars | Stacked daily bars with the slice mean. | - | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:585-585` |
| 20 | `<MeterRow` model rows | One meter per model with spend and share, unpriced models kept. | - | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:667-667` |
| 21 | `<button` Show more | Shows models not used in the recency window. | `setShowAll` | shown only while stale models are hidden | [[web/src/Overview.tsx]] `web/src/Overview.tsx:708-711` |
| 22 | `<BucketBar` per model buckets | Token buckets per model. | - | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:751-751` |
| 23 | `<ComparisonMeter` no cache against billed | Two meters comparing the no cache price with the billed price. | - | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:790-790` |
| 24 | `{priced ? (` empty section | Shows the saving only when the slice has priced tokens. | - | empty: `{priced ? (` | [[web/src/Overview.tsx]] `web/src/Overview.tsx:803-803` |
| 25 | `<MeterRow` project rows | Top five projects by cost. | - | - | [[web/src/Overview.tsx]] `web/src/Overview.tsx:848-848` |
| 26 | `<button` Show more | Shows the remaining projects. | `setShowAll` | shown only while projects are hidden | [[web/src/Overview.tsx]] `web/src/Overview.tsx:877-880` |

### Conditional sections

- empty: `byCost.length === 0`, callout 13, [[web/src/Overview.tsx]] `web/src/Overview.tsx:479-479`
- empty: `bySpan.length === 0`, callout 15, [[web/src/Overview.tsx]] `web/src/Overview.tsx:499-499`
- empty: `rows.length === 0`, callout 18, [[web/src/Overview.tsx]] `web/src/Overview.tsx:579-579`
- empty: `{priced ? (`, callout 24, [[web/src/Overview.tsx]] `web/src/Overview.tsx:803-803`

## Diagnosis

The reader reads the slice at a glance and can jump to Sources from two places: the hidden readers line and the Flagged figure `web/src/Overview.tsx:150-158` `web/src/Overview.tsx:329`.

What can go wrong:

- The rows of the heaviest sessions panel carry no click handler, so a reader who spots a costly session cannot open it from here `web/src/Overview.tsx:436-444`.
- The Flagged figure counts the warning summary of the last scan, while the Sources view shows the warning groups of the current report, so the two can disagree `web/src/Overview.tsx:322-323` `web/src/Sources.tsx:236-243`.
- The project meters colour unpriced projects with a series colour, while the model meters use the cost state colour for the same case `web/src/Overview.tsx:866` `web/src/Overview.tsx:696`.

States not handled: the Show more buttons have no way back to the short list once pressed `web/src/Overview.tsx:705-716` `web/src/Overview.tsx:874-885`.
