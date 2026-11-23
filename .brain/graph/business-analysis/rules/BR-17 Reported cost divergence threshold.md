---
code: BR-17
tags:
  - ba/rule
maturity: approved
---
# Reported cost divergence threshold

## Statement

The tool's own cost is flagged as different when it differs from the computed cost by more than five percent or one cent, whichever is larger.

## Enforced in

- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-09 Read a figure and see how far to trust it]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/pricing-notes.ts | confirmed
  > return Math.abs(computed - reported) > Math.max(0.05 * Math.abs(computed), 0.01)
