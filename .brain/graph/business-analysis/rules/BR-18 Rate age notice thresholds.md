---
code: BR-18
tags:
  - ba/rule
maturity: approved
---
# Rate age notice thresholds

## Statement

A notice about old prices appears from 30 days and becomes a caution from 90 days. Unknown age shows nothing.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/pricing-notes.ts | confirmed
  > if (days < STALE_INFO_DAYS) return null
- [[Code of localtokenomics]] @ enforced-by -> web/src/pricing-notes.ts | confirmed
  > severity: days >= STALE_CAUTION_DAYS ? 'caution' : 'info',
