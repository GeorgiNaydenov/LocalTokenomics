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

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::RateTable._consistent | inferred
  > models reference undefined providers
