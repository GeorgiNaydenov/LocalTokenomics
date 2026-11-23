---
code: BR-54
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: approved
---
# Missing token counts mean unavailable

## Statement

A request whose log carries no token counts has the cost state unavailable. It is never priced as zero and never called free. `src/ai_usage_cost/pricing.py:420`

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::cost_state_of | inferred
  > if tokens is None:
