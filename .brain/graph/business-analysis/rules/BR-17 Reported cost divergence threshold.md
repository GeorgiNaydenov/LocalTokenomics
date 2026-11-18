---
code: BR-17
tags:
  - ba/rule
maturity: approved
---
# Reported cost divergence threshold

## Statement

The tool's own cost is flagged as different when it differs from the computed cost by more than five percent or one cent, whichever is larger.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/pricing-notes.ts | confirmed
  > return Math.abs(computed - reported) > Math.max(0.05 * Math.abs(computed), 0.01)
