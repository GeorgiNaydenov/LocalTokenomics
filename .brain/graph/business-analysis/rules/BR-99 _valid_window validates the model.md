---
code: BR-99
category: validator
tags:
  - ba/rule
maturity: approved
---
# _valid_window validates the model

## Statement

In _valid_window, the model: the code validates before accepting the value. Located at src/ai_usage_cost/pricing.py lines 54-60.

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_valid_window | inferred
  > def _valid_window(self) -> Peak:
