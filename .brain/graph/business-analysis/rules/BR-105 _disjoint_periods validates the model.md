---
code: BR-105
category: validator
tags:
  - ba/rule
maturity: approved
---
# _disjoint_periods validates the model

## Statement

In _disjoint_periods, the model: the code validates before accepting the value. Located at src/ai_usage_cost/pricing.py lines 153-160.

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_disjoint_periods | inferred
  > def _disjoint_periods(self) -> ModelRate:
