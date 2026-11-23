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

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::cost_of | inferred
  > sorted ascending: the last band at or under the request size wins
