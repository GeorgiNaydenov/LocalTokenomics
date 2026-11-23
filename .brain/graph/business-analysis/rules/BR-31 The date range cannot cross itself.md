---
code: BR-31
category: validation
tags:
  - ba/rule
maturity: approved
---
# The date range cannot cross itself

## Statement

The from date cannot be later than the to date, and the to date cannot be earlier than the from date.

## Enforced in

- [[UC-01 Compare a dashboard screen with its reference]]
- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-10 Narrow a list and choose its columns]]
- [[UC-28 Sort the session list and open one session in the prototype]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/filters.tsx::DateRange | confirmed
  >         max={until ?? max}
- [[Code of localtokenomics]] @ enforced-by -> web/src/components/filters.tsx::DateRange | confirmed
  >         min={since ?? min}
