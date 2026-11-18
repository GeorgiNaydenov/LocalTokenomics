---
code: BR-63
category: data integrity
subdomain: Cost pricing
tags:
  - ba/rule
maturity: draft
---
# Price periods must not overlap

## Statement

A row whose dated periods overlap is rejected at load, because the first matching period would otherwise decide by file order. `src/ai_usage_cost/pricing.py:159`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::ModelRate._disjoint_periods | inferred
  > overlapping periods
