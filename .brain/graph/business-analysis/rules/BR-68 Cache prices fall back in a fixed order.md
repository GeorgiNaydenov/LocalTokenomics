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

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_cache_price | inferred
  > the set's own absolute figure
