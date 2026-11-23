---
code: BR-20
tags:
  - ba/rule
maturity: approved
---
# Rate row state

## Statement

A rate row is free when its rules say free, priced when matched buckets carry spend, and unused otherwise.

## Enforced in

- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/Pricing.tsx | confirmed
  > const state: RateState = isFree ? 'free' : spendValue > 0 ? 'priced' : 'unused'
