---
code: BR-67
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: approved
---
# An unpriced tier is billed standard and flagged

## Statement

A service tier other than standard and batch that the row has no price for is billed at the standard price and flagged tier unpriced, which raises a warning. `src/ai_usage_cost/pricing.py:526`

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::cost_of | inferred
  > tier_unpriced = True
