---
code: BR-64
category: data integrity
subdomain: Cost pricing
tags:
  - ba/rule
maturity: approved
---
# Peak windows must not wrap midnight

## Statement

A peak window uses weekdays 0 to 6 and hour ranges with start below end and end at most 24, so a window across midnight must be split in the file. `src/ai_usage_cost/pricing.py:59`

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::Peak._valid_window | inferred
  > peak utc_hours ranges must satisfy
