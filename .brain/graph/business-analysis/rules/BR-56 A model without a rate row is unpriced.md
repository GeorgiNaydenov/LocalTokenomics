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

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::cost_state_of | inferred
  > return "unpriced"
