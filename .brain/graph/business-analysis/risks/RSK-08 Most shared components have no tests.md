---
code: RSK-08
impact: medium
likelihood: medium
tags:
  - ba/risk
maturity: approved
---
# Most shared components have no tests

## Risk

Only the info popover, the ranking helpers and the sparkline geometry have tests. The stat cards, the daily chart, the filters, the column chooser and the session and trace views are untested, so a change can break a figure shown to the reader unnoticed. `web/src/components/rank.test.ts:4`

## Mitigation

Add tests for the display rules recorded in this chunk, starting with the unavailable marker and the twelve series limit.
