---
code: BR-57
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: approved
---
# A prefix match is an estimate

## Statement

When a model id matches a row only through a shorter prefix and a remainder that is not a known suffix, the price is flagged estimated and the pipeline raises a warning. `src/ai_usage_cost/pricing.py:313`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::RateTable.lookup | inferred
  > kind = "estimated"
