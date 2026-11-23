---
code: BR-108
category: guard
tags:
  - ba/rule
maturity: approved
---
# _consistent refuses when duplicates

## Statement

In _consistent, when duplicates: the code raises ValueError. Located at src/ai_usage_cost/pricing.py lines 275-276.

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_consistent | inferred
  > if duplicates:
