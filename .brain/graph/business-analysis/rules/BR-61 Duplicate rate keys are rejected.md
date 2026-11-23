---
code: BR-61
category: data integrity
subdomain: Cost pricing
tags:
  - ba/rule
maturity: approved
---
# Duplicate rate keys are rejected

## Statement

A rate table with two rows that share a match key fails to load. `src/ai_usage_cost/pricing.py:276`

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::RateTable._consistent | inferred
  > duplicate model match keys
