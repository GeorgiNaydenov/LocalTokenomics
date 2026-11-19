---
code: RSK-33
impact: medium
likelihood: low
tags:
  - ba/risk
maturity: draft
---
# A chart part outside its container throws with no error boundary above it

## Risk

The chart hook throws a plain error when no container is above it, and the app is mounted with one render call and no error boundary, so the error would leave the page blank. `web/src/components/ui/chart.tsx:33` `web/src/main.tsx:7`

## Mitigation

Add one error boundary around the app that shows the existing error card with a retry button.
