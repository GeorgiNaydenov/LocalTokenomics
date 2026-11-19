---
title: UC-11 Inspect a chart point
aliases: [UC-11, Inspect a chart point]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [web/src/components/chart-hover.tsx, web/src/components/sparkline.tsx, web/src/components/sparkline.test.ts]
generated: true
use-cases: [UC-11]
subdomain: ''
---

# UC-11 Inspect a chart point

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Actors:** [[Actors#Dashboard reader|Dashboard reader]]
- **Maturity:** approved

## Description

The reader moves the pointer or uses the keyboard over a chart to read the value behind one point or day.

## Preconditions

A sparkline with labels and a formatter, or a context occupancy chart, is on screen.

## Main flow

1. The pointer position is turned into a point index. [[web/src/components/chart-hover.tsx|web/src/components/chart-hover.tsx:43]]
2. Arrow keys, Home and End move the index, and Escape clears it. [[web/src/components/chart-hover.tsx|web/src/components/chart-hover.tsx:63]]
3. The detail box is drawn above the chart at the point. [[web/src/components/chart-hover.tsx|web/src/components/chart-hover.tsx:91]]
4. A polite live region reads the point aloud. [[web/src/components/chart-hover.tsx|web/src/components/chart-hover.tsx:114]]

## Alternative flows

- At step 1, a sparkline given no labels or no formatter has no hover. [[web/src/components/sparkline.tsx|web/src/components/sparkline.tsx:129]]

## Postconditions

A detail box shows the title and values of the chosen point, and a live region announces it.

## Acceptance criteria

- A sparkline keeps every y coordinate inside the box height, even for a series with negative dips. [[web/src/components/sparkline.test.ts|web/src/components/sparkline.test.ts:10]]

## Code

- [[web/src/components/chart-hover.tsx]]
- [[web/src/components/sparkline.tsx]]
- [[web/src/components/sparkline.test.ts]]
