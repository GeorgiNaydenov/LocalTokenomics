---
code: BR-61
category: data integrity
subdomain: Cost pricing
tags:
  - ba/rule
maturity: draft
---
# Duplicate rate keys are rejected

## Statement

A rate table with two rows that share a match key fails to load. `src/ai_usage_cost/pricing.py:276`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::RateTable._consistent | inferred
  > duplicate model match keys
