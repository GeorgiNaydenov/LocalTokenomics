---
code: BR-68
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: approved
---
# Cache prices fall back in a fixed order

## Statement

A cache price is the price set's own figure, else the row's published cache to input ratio times the set's input price, else the provider multiplier times it. `src/ai_usage_cost/pricing.py:486`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_cache_price | inferred
  > the set's own absolute figure
