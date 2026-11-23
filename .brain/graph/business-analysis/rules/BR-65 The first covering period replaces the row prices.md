---
code: BR-65
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: approved
---
# The first covering period replaces the row prices

## Statement

The first period that covers the request's UTC date replaces the row's own price fields, and only the fields the file wrote. `src/ai_usage_cost/pricing.py:449`

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_period_applied | inferred
  > The row's price fields after the first period covering
