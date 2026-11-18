---
code: BR-04
tags:
  - ba/rule
maturity: approved
---
# Prototype splits session cost across token buckets by fixed weights

## Statement

The session drawer apportions a session's cost across the four token buckets with constant weights, not with real rates.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Screens.tsx | confirmed
  > const BUCKET_WEIGHT: Record<string, number> = {
- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Screens.tsx | confirmed
  > total > 0 ? (weighted[index] / total) * session.cost! : 0,
