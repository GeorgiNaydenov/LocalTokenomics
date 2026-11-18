---
code: BR-20
tags:
  - ba/rule
maturity: approved
---
# Rate row state

## Statement

A rate row is free when its rules say free, priced when matched buckets carry spend, and unused otherwise.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/Pricing.tsx | confirmed
  > const state: RateState = isFree ? 'free' : spendValue > 0 ? 'priced' : 'unused'
