---
code: BR-59
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: approved
---
# The longest matching row wins

## Statement

When several rows match a model id, the row with the longest match key is used. `src/ai_usage_cost/pricing.py:302`

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::RateTable.lookup | inferred
  > len(rate.match) > len(best.match)
