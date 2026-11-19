---
code: RSK-38
impact: low
likelihood: medium
tags:
  - ba/risk
maturity: draft
---
# Every info box keeps a timer and one global pointer listener

## Risk

Each info box starts its own 100 ms interval for its whole lifetime, and one pointer listener is added to the window at load and never removed, so a table with many badges runs many timers. `web/src/components/metric-info.tsx:79` `web/src/components/metric-info.tsx:37`

## Mitigation

Start the timer only while the pointer is near or the box is open.
