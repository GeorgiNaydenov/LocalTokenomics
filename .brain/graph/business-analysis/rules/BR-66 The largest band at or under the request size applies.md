---
code: BR-66
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: approved
---
# The largest band at or under the request size applies

## Statement

Bands are sorted by minimum input and the last band whose minimum is at or under the request's total input prices the whole request. `src/ai_usage_cost/pricing.py:511`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::cost_of | inferred
  > sorted ascending: the last band at or under the request size wins
