---
code: RSK-09
impact: low
likelihood: low
tags:
  - ba/risk
maturity: approved
---
# Popover timing depends on a polling interval

## Risk

The info popover decides to open and close from a 100 ms poll of the pointer position, so it can lag on a slow machine. `web/src/components/metric-info.tsx:11`

## Mitigation

The popover also opens on focus and click, so it is reachable without the poll. `web/src/components/metric-info.tsx:143`
