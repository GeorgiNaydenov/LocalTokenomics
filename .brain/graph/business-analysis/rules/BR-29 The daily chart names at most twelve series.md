---
code: BR-29
category: display
tags:
  - ba/rule
maturity: approved
---
# The daily chart names at most twelve series

## Statement

The stacked daily cost chart gives its twelve largest series their own colour and legend entry, and groups all others under Other with a count.

## Enforced in

- [[UC-01 Compare a dashboard screen with its reference]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-28 Sort the session list and open one session in the prototype]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/chart-time.tsx::TimeChart | confirmed
  >     const overflowKeys = keys.slice(LEGEND_LIMIT)
- [[Code of localtokenomics]] @ enforced-by -> web/src/components/series.ts::SERIES_SLOTS | confirmed
  > export const SERIES_SLOTS = 12
