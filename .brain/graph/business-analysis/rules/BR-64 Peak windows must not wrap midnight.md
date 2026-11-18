---
code: BR-64
category: data integrity
subdomain: Cost pricing
tags:
  - ba/rule
maturity: draft
---
# Peak windows must not wrap midnight

## Statement

A peak window uses weekdays 0 to 6 and hour ranges with start below end and end at most 24, so a window across midnight must be split in the file. `src/ai_usage_cost/pricing.py:59`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::Peak._valid_window | inferred
  > peak utc_hours ranges must satisfy
