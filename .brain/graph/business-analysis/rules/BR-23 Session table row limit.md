---
code: BR-23
tags:
  - ba/rule
maturity: approved
---
# Session table row limit

## Statement

The sessions table shows at most 120 rows of the sorted list.

## Enforced in

- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-10 Narrow a list and choose its columns]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/Sessions.tsx | confirmed
  > const SHOWN_LIMIT = 120
