---
code: BR-21
tags:
  - ba/rule
maturity: approved
---
# Sub cent money keeps four decimals

## Statement

A nonzero amount under one cent is shown with up to four decimals so it never reads as zero dollars.

## Enforced in

- [[UC-01 Compare a dashboard screen with its reference]]
- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-28 Sort the session list and open one session in the prototype]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/format.ts | confirmed
  > return value !== 0 && Math.abs(value) < 0.01 ? moneyPrecise.format(value) : money.format(value)
