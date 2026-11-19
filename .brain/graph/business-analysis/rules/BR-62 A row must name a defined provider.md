---
code: BR-62
category: data integrity
subdomain: Cost pricing
tags:
  - ba/rule
maturity: approved
---
# A row must name a defined provider

## Statement

When a rate table defines provider blocks, every row must name one of them, so no row is priced silently with default cache rules. `src/ai_usage_cost/pricing.py:282`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::RateTable._consistent | inferred
  > models reference undefined providers
