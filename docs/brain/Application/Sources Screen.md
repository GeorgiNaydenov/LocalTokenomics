---
title: Sources Screen
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

# Sources Screen

The Sources view (web/src/Sources.tsx): the capability matrix, the readers with data, the readers not detected and the scan warnings. Its map is [[Sources Screen Map]]; each numbered badge in the image is one row below.

## Screen map

| # | Element | What it does | Handler or target | State it depends on | Citation |
|---|---|---|---|---|---|
| 1 | `<Table` capability matrix | One row per reader and one provenance badge per capability. | - | - | [[web/src/Sources.tsx]] `web/src/Sources.tsx:55-55` |
| 2 | `<ProvenanceBadge` provenance | Badge naming where a capability value comes from, with a title that explains it. | - | - | [[web/src/Sources.tsx]] `web/src/Sources.tsx:82-82` |
| 3 | `<DetectedSource` reader detail | One detail block per detected reader with files, sessions, requests and last event. | `detected` | - | [[web/src/Sources.tsx]] `web/src/Sources.tsx:229-234` |
| 4 | `undetected.length > 0` empty section | Shows the folded list of readers not found here only when there are some. | - | empty: `undetected.length > 0` | [[web/src/Sources.tsx]] `web/src/Sources.tsx:234-234` |
| 5 | `<DisclosurePanel` Available, not detected here | Folded list with the expected path and a hint per reader. | - | - | [[web/src/Sources.tsx]] `web/src/Sources.tsx:180-180` |
| 6 | `report.warning_groups.length > 0` error section | Shows the warnings panel only when the report carries warning groups. | - | error: `report.warning_groups.length > 0` | [[web/src/Sources.tsx]] `web/src/Sources.tsx:236-236` |
| 7 | `<WarningsList` warning groups | Grouped scan warnings with severity. | - | - | [[web/src/Sources.tsx]] `web/src/Sources.tsx:243-243` |

### Conditional sections

- empty: `undetected.length > 0`, callout 4, [[web/src/Sources.tsx]] `web/src/Sources.tsx:234-234`
- error: `report.warning_groups.length > 0`, callout 6, [[web/src/Sources.tsx]] `web/src/Sources.tsx:236-236`

## Diagnosis

The reader reads only; nothing on this view changes data. The undetected list tells them how to bring a reader in by giving it a path `web/src/Sources.tsx:202-206`.

What can go wrong:

- When no reader is detected the Readers with data panel renders an empty list with no empty state `web/src/Sources.tsx:222-232`.
- Warnings show only from the current report, so a warning counted by the Flagged figure of the overview may not appear here `web/src/Sources.tsx:236` `web/src/Overview.tsx:322-323`.

States not handled: no loading or error state of its own; the shell renders this view only once the report and the metadata exist `web/src/App.tsx:336`.
