---
title: Overview Screen Map
aliases: []
tags: [diagram, drawio, screen-map]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
sources: [docs/brain/architecture/drawio/drawio-screen-overview.drawio]
chunk: ch-localtokenomics-web-src
authored: true
screen-note: Overview Screen
node_citations:
  drawio-screen-overview:
    el-1: ['web/src/Overview.tsx:117-117']
    el-2: ['web/src/Overview.tsx:151-153']
    el-3: ['web/src/Overview.tsx:193-193']
    el-4: ['web/src/Overview.tsx:223-223']
    el-5: ['web/src/Overview.tsx:246-246']
    el-6: ['web/src/Overview.tsx:265-265']
    el-7: ['web/src/Overview.tsx:284-284']
    el-8: ['web/src/Overview.tsx:325-329']
    el-9: ['web/src/Overview.tsx:362-362']
    el-10: ['web/src/Overview.tsx:377-377']
    el-11: ['web/src/Overview.tsx:392-392']
    el-12: ['web/src/Overview.tsx:472-472']
    el-13: ['web/src/Overview.tsx:479-479']
    el-14: ['web/src/Overview.tsx:492-492']
    el-15: ['web/src/Overview.tsx:499-499']
    el-16: ['web/src/Overview.tsx:554-559']
    el-17: ['web/src/Overview.tsx:565-570']
    el-18: ['web/src/Overview.tsx:579-579']
    el-19: ['web/src/Overview.tsx:585-585']
    el-20: ['web/src/Overview.tsx:667-667']
    el-21: ['web/src/Overview.tsx:708-711']
    el-22: ['web/src/Overview.tsx:751-751']
    el-23: ['web/src/Overview.tsx:790-790']
    el-24: ['web/src/Overview.tsx:803-803']
    el-25: ['web/src/Overview.tsx:848-848']
    el-26: ['web/src/Overview.tsx:877-880']
    badge-1: ['web/src/Overview.tsx:117-117']
    badge-2: ['web/src/Overview.tsx:151-153']
    badge-3: ['web/src/Overview.tsx:193-193']
    badge-4: ['web/src/Overview.tsx:223-223']
    badge-5: ['web/src/Overview.tsx:246-246']
    badge-6: ['web/src/Overview.tsx:265-265']
    badge-7: ['web/src/Overview.tsx:284-284']
    badge-8: ['web/src/Overview.tsx:325-329']
    badge-9: ['web/src/Overview.tsx:362-362']
    badge-10: ['web/src/Overview.tsx:377-377']
    badge-11: ['web/src/Overview.tsx:392-392']
    badge-12: ['web/src/Overview.tsx:472-472']
    badge-13: ['web/src/Overview.tsx:479-479']
    badge-14: ['web/src/Overview.tsx:492-492']
    badge-15: ['web/src/Overview.tsx:499-499']
    badge-16: ['web/src/Overview.tsx:554-559']
    badge-17: ['web/src/Overview.tsx:565-570']
    badge-18: ['web/src/Overview.tsx:579-579']
    badge-19: ['web/src/Overview.tsx:585-585']
    badge-20: ['web/src/Overview.tsx:667-667']
    badge-21: ['web/src/Overview.tsx:708-711']
    badge-22: ['web/src/Overview.tsx:751-751']
    badge-23: ['web/src/Overview.tsx:790-790']
    badge-24: ['web/src/Overview.tsx:803-803']
    badge-25: ['web/src/Overview.tsx:848-848']
    badge-26: ['web/src/Overview.tsx:877-880']
    region-1: ['web/src/Overview.tsx:117-117', 'web/src/Overview.tsx:151-153']
    region-2: ['web/src/Overview.tsx:193-193', 'web/src/Overview.tsx:223-223', 'web/src/Overview.tsx:246-246',
      'web/src/Overview.tsx:265-265', 'web/src/Overview.tsx:284-284', 'web/src/Overview.tsx:325-329']
    region-3: ['web/src/Overview.tsx:362-362', 'web/src/Overview.tsx:377-377', 'web/src/Overview.tsx:392-392']
    region-4: ['web/src/Overview.tsx:472-472', 'web/src/Overview.tsx:479-479', 'web/src/Overview.tsx:492-492',
      'web/src/Overview.tsx:499-499']
    region-5: ['web/src/Overview.tsx:554-559', 'web/src/Overview.tsx:565-570', 'web/src/Overview.tsx:579-579',
      'web/src/Overview.tsx:585-585']
    region-6: ['web/src/Overview.tsx:667-667', 'web/src/Overview.tsx:708-711']
    region-7: ['web/src/Overview.tsx:751-751']
    region-8: ['web/src/Overview.tsx:790-790', 'web/src/Overview.tsx:803-803']
    region-9: ['web/src/Overview.tsx:848-848', 'web/src/Overview.tsx:877-880']
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Overview Screen Map

This map shows the first view a reader lands on. It lets them see in one place what the slice cost, which readers found logs and where the spend went. Each numbered part says which figures it shows and when it shows nothing instead of a guess.

## What the diagram shows

- The view stacks the detected readers panel, the headline figures, the outcome row, the heaviest sessions, the time chart and four panels in two grids `web/src/Overview.tsx:900-916`.
- The headline row has six figures, and the last one, Flagged, opens the Sources view when warnings exist `web/src/Overview.tsx:191-318` `web/src/Overview.tsx:321-329`.
- The time chart has two toggle groups, one for the stacking and one for the metric `web/src/Overview.tsx:552-576`.
- Each panel that may lack data draws an unavailable marker or an empty state rather than a zero `web/src/Overview.tsx:479-481` `web/src/Overview.tsx:579-584` `web/src/Overview.tsx:803-814`.

## Capability and related functionality

The view is selected from [[App Screen]]. The figures come from the report described in [[Web Data Model]], and the rule that an absent figure is never drawn as zero is part of [[Web Specification]]. The Flagged figure leads to [[Sources Screen]].

## Overview Screen screen map

![[docs/brain/architecture/rendered/drawio-screen-overview.svg]]

> [!example]- Code references
> | Badge | Element | Code |
> |---|---|---|
> | 1 | `<SourceCard` reader cards | `web/src/Overview.tsx:117-117` |
> | 2 | `<button` more readers | `web/src/Overview.tsx:151-153` |
> | 3 | `<Stat` API equivalent cost | `web/src/Overview.tsx:193-193` |
> | 4 | `<Stat` Tokens | `web/src/Overview.tsx:223-223` |
> | 5 | `<Stat` Requests | `web/src/Overview.tsx:246-246` |
> | 6 | `<Stat` Sessions | `web/src/Overview.tsx:265-265` |
> | 7 | `<Stat` Cache saved | `web/src/Overview.tsx:284-284` |
> | 8 | `<Stat` Flagged | `web/src/Overview.tsx:325-329` |
> | 9 | `<Stat` Success rate | `web/src/Overview.tsx:362-362` |
> | 10 | `<Stat` Tokens per success | `web/src/Overview.tsx:377-377` |
> | 11 | `<Stat` Cost per success | `web/src/Overview.tsx:392-392` |
> | 12 | `<HeavyRow` Most expensive | `web/src/Overview.tsx:472-472` |
> | 13 | `byCost.length === 0` empty section | `web/src/Overview.tsx:479-479` |
> | 14 | `<HeavyRow` Longest log span | `web/src/Overview.tsx:492-492` |
> | 15 | `bySpan.length === 0` empty section | `web/src/Overview.tsx:499-499` |
> | 16 | `<ToggleGroup` Client, Provider, Model | `web/src/Overview.tsx:554-559` |
> | 17 | `<ToggleGroup` Cost, Tokens | `web/src/Overview.tsx:565-570` |
> | 18 | `rows.length === 0` empty section | `web/src/Overview.tsx:579-579` |
> | 19 | `<TimeChart` daily bars | `web/src/Overview.tsx:585-585` |
> | 20 | `<MeterRow` model rows | `web/src/Overview.tsx:667-667` |
> | 21 | `<button` Show more | `web/src/Overview.tsx:708-711` |
> | 22 | `<BucketBar` per model buckets | `web/src/Overview.tsx:751-751` |
> | 23 | `<ComparisonMeter` no cache against billed | `web/src/Overview.tsx:790-790` |
> | 24 | `{priced ? (` empty section | `web/src/Overview.tsx:803-803` |
> | 25 | `<MeterRow` project rows | `web/src/Overview.tsx:848-848` |
> | 26 | `<button` Show more | `web/src/Overview.tsx:877-880` |
