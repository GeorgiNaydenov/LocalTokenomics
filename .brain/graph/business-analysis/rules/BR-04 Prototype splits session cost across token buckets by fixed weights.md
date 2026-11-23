---
code: BR-04
tags:
  - ba/rule
maturity: approved
---
# Prototype splits session cost across token buckets by fixed weights

## Statement

The session drawer apportions a session's cost across the four token buckets with constant weights, not with real rates.

## Enforced in

- [[UC-01 Compare a dashboard screen with its reference]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-10 Narrow a list and choose its columns]]
- [[UC-12 Review a session's spans and context use]]
- [[UC-28 Sort the session list and open one session in the prototype]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Screens.tsx | confirmed
  > const BUCKET_WEIGHT: Record<string, number> = {
- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Screens.tsx | confirmed
  > total > 0 ? (weighted[index] / total) * session.cost! : 0,
