---
code: BR-101
category: guard
tags:
  - ba/rule
maturity: approved
---
# _valid_window refuses when any((not 0 <= start < end <= 24 for start, end in self.

## Statement

In _valid_window, when any((not 0 <= start < end <= 24 for start, end in self.utc_hours)): the code raises ValueError, message "peak utc_hours ranges must satisfy 0 <= start < end <= 24". Located at src/ai_usage_cost/pricing.py lines 58-59.

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_valid_window | inferred
  > if any(not 0 <= start < end <= 24 for start, end in self.utc_hours):
