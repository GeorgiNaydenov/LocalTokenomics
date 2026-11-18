---
code: BR-82
category: reporting
subdomain: Spend reporting
tags:
  - ba/rule
maturity: draft
---
# Old rates raise a warning

## Statement

When the rate table's as of date is more than 30 days old a warning asks for the table to be checked again. `src/ai_usage_cost/pipeline.py:235`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pipeline.py::analyze | inferred
  > if age is not None and age > STALE_INFO_DAYS:
