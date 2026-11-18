---
code: BR-55
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: draft
---
# A free provider costs zero

## Statement

A request from a provider marked free gets the state free and a zero cost breakdown, provided its tokens are known. `src/ai_usage_cost/pricing.py:434`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::price_event | inferred
  > return CostBreakdown(), "free"
