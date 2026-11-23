---
code: BR-104
category: validator
tags:
  - ba/rule
maturity: approved
---
# _sorted_bands validates bands

## Statement

In _sorted_bands, bands: the code validates before accepting the value. Located at src/ai_usage_cost/pricing.py lines 149-150.

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_sorted_bands | inferred
  > def _sorted_bands(cls, bands: list[Band]) -> list[Band]:
