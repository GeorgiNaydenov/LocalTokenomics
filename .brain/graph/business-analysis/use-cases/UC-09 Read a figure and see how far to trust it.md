---
code: UC-09
primary_actor: Dashboard reader
tags:
  - ba/use-case
maturity: approved
---
# Read a figure and see how far to trust it

## Description

The reader looks at a headline number, a session row or a source card and wants to know whether the figure is measured, estimated, unpriced or missing.

## Preconditions

The dashboard has received values and labels for the view.

## Postconditions

Each figure is shown with its cost state or provenance, or as unavailable. Nothing is invented.

## Main flow

1. The screen passes a value, label and cost state to a stat card, session card or source card. `web/src/components/stat.tsx:61`
2. The component draws the badge for the cost state, provenance or outcome. `web/src/components/status.tsx:149`
3. A priced row that used a sibling rate also gets an Estimated badge. `web/src/components/status.tsx:180`
4. The reader hovers, focuses or taps the badge or the info glyph to open the explanation. `web/src/components/metric-info.tsx:46`

## Alternative flows

- At step 2, when the value is null, the component shows the unavailable marker instead of a number or bar. `web/src/components/session.tsx:200`

## Acceptance criteria

- The explanation opens on click and shows the plain text. `web/src/components/metric-info.test.tsx:7`
- The worst state of a mixed set is unavailable over unpriced, free and priced. `web/src/components/rank.test.ts:5`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/components/status.tsx::CostBadges | inferred
  > export function CostBadges({
- [[Code of localtokenomics]] @ implemented-by -> web/src/components/metric-info.tsx::MetricInfo | inferred
  > export function MetricInfo({
