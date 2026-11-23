---
code: BR-27
category: calculation
tags:
  - ba/rule
maturity: approved
---
# A rollup shows its least trustworthy cost state and provenance

## Statement

When several rows are combined, the worst cost state (unavailable over unpriced over free over priced) and the worst provenance are shown. An empty list gives unavailable.

## Enforced in

- [[UC-05 Read usage and cost for a period]]
- [[UC-07 Rate a session outcome]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/rank.ts::worstState | confirmed
  >   return [...states].sort((a, b) => STATE_RANK[b] - STATE_RANK[a])[0] ?? 'unavailable'
- [[Code of localtokenomics]] @ enforced-by -> web/src/components/rank.ts::worstProvenance | confirmed
  >   return [...values].sort((a, b) => PROVENANCE_RANK[b] - PROVENANCE_RANK[a])[0] ?? 'unavailable'
