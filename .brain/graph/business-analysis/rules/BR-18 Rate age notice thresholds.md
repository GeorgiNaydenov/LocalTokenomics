---
code: BR-18
tags:
  - ba/rule
maturity: approved
---
# Rate age notice thresholds

## Statement

A notice about old prices appears from 30 days and becomes a caution from 90 days. Unknown age shows nothing.

## Enforced in

- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-09 Read a figure and see how far to trust it]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/pricing-notes.ts | confirmed
  > if (days < STALE_INFO_DAYS) return null
- [[Code of localtokenomics]] @ enforced-by -> web/src/pricing-notes.ts | confirmed
  > severity: days >= STALE_CAUTION_DAYS ? 'caution' : 'info',
