---
code: BR-56
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: approved
---
# A model without a rate row is unpriced

## Statement

A request whose model matches no rate row has the state unpriced. Its tokens are counted and its cost is excluded from totals. `src/ai_usage_cost/pricing.py:425`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::cost_state_of | inferred
  > return "unpriced"
