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

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_consistent | inferred
  > if duplicates:
