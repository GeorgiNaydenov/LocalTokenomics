---
code: BR-54
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: draft
---
# Missing token counts mean unavailable

## Statement

A request whose log carries no token counts has the cost state unavailable. It is never priced as zero and never called free. `src/ai_usage_cost/pricing.py:420`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::cost_state_of | inferred
  > if tokens is None:
