---
code: BR-59
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: draft
---
# The longest matching row wins

## Statement

When several rows match a model id, the row with the longest match key is used. `src/ai_usage_cost/pricing.py:302`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::RateTable.lookup | inferred
  > len(rate.match) > len(best.match)
