---
code: BR-78
category: reporting
subdomain: Spend reporting
tags:
  - ba/rule
maturity: draft
---
# The local calendar day decides the day of an event

## Statement

An event belongs to the machine's local calendar day, a timestamp without an offset is read as UTC, and both bucketing and date filters use the same function. `src/ai_usage_cost/models.py:146`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/models.py::local_day | inferred
  > return aware.astimezone().date()
