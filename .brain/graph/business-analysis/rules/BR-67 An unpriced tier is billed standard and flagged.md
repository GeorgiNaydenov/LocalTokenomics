---
code: BR-67
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: draft
---
# An unpriced tier is billed standard and flagged

## Statement

A service tier other than standard and batch that the row has no price for is billed at the standard price and flagged tier unpriced, which raises a warning. `src/ai_usage_cost/pricing.py:526`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::cost_of | inferred
  > tier_unpriced = True
