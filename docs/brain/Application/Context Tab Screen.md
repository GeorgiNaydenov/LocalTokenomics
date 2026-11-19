---
title: Context Tab Screen
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

# Context Tab Screen

The Context tab of the session workspace (web/src/ContextTab.tsx): occupancy over the session and one card per model call. Its map is [[Context Tab Screen Map]]; each numbered badge in the image is one row below.

## Screen map

| # | Element | What it does | Handler or target | State it depends on | Citation |
|---|---|---|---|---|---|
| 1 | `snapshots.length === 0` empty section | Empty state when the session has no call with an input count. | - | empty: `snapshots.length === 0` | [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:164-164` |
| 2 | `<ContextOccupancy` occupancy chart | Occupancy of every call over the session. | - | - | [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:192-192` |
| 3 | `props.source === 'claude-code'` info section | Note that capacity is estimated for this reader. | - | info: `props.source === 'claude-code'` | [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:199-199` |
| 4 | `snapshot.compacted_before` info section | Marker that the context was compacted before this call. | - | info: `snapshot.compacted_before` | [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:74-74` |
| 5 | `snapshot.occupancy === null` empty section | Unavailable marker instead of a bar when a size is unknown. | - | empty: `snapshot.occupancy === null` | [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:42-42` |
| 6 | `<ProvenanceBadge` capacity, occupancy, tokens | Provenance badges of the three figures. | - | - | [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:115-115` |
| 7 | `<Button` added span | Jumps to a span that added to the context, in the trace tab. | `onFocusSpan` | - | [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:135-139` |
| 8 | `snapshot.added_span_ids.length === 0` empty section | Says no records were added since the previous call. | - | empty: `snapshot.added_span_ids.length === 0` | [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:149-149` |
| 9 | `<Button` Show more calls | Reveals the next batch of call cards. | `setRevealed` | shown only while cards are hidden | [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:216-220` |

### Conditional sections

- empty: `snapshots.length === 0`, callout 1, [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:164-164`
- info: `props.source === 'claude-code'`, callout 3, [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:199-199`
- info: `snapshot.compacted_before`, callout 4, [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:74-74`
- empty: `snapshot.occupancy === null`, callout 5, [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:42-42`
- empty: `snapshot.added_span_ids.length === 0`, callout 8, [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:149-149`

## Diagnosis

The reader scans occupancy and jumps to contributing spans. A jump selects the trace tab and focuses the span `web/src/SessionWorkspace.tsx:481-484`.

What can go wrong:

- Only the first six contributors get a button; the rest are a count the reader cannot open `web/src/ContextTab.tsx:69-70` `web/src/ContextTab.tsx:146-148`.
- A jump to a span hidden by a trace filter lands on an unhighlighted list `web/src/TraceTab.tsx:765-768`.

States not handled: the high occupancy colour is the only signal of a near full window; there is no text label for it `web/src/ContextTab.tsx:57`.
