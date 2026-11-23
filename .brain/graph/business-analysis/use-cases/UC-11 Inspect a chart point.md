---
code: UC-11
primary_actor: Dashboard reader
subdomain: Web UI components area
no_models_reason: No model of the specification is declared in the code this use case cites or in a file that code imports directly.
rules:
  - Caller class names override primitive defaults
tags:
  - ba/use-case
maturity: approved
---
# Inspect a chart point

## Description

The reader moves the pointer or uses the keyboard over a chart to read the value behind one point or day.

## Preconditions

- A sparkline with labels and a formatter, or a context occupancy chart, is on screen.

## Postconditions

- A detail box shows the title and values of the chosen point, and a live region announces it.

## Main flow

1. The pointer position is turned into a point index. `web/src/components/chart-hover.tsx:43`
2. Arrow keys, Home and End move the index, and Escape clears it. `web/src/components/chart-hover.tsx:63`
3. The detail box is drawn above the chart at the point. `web/src/components/chart-hover.tsx:91`
4. A polite live region reads the point aloud. `web/src/components/chart-hover.tsx:114`

## Alternative flows

- At step 1, a sparkline given no labels or no formatter has no hover. `web/src/components/sparkline.tsx:129`

## Acceptance criteria

- A sparkline keeps every y coordinate inside the box height, even for a series with negative dips. `web/src/components/sparkline.test.ts:10`

## Glossary

- [[Context occupancy]]
- [[Reader]]

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/components/chart-hover.tsx::HoverFrame | inferred
  > export function HoverFrame({
