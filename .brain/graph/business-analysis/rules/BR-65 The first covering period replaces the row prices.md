---
code: BR-65
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: draft
---
# The first covering period replaces the row prices

## Statement

The first period that covers the request's UTC date replaces the row's own price fields, and only the fields the file wrote. `src/ai_usage_cost/pricing.py:449`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_period_applied | inferred
  > The row's price fields after the first period covering
