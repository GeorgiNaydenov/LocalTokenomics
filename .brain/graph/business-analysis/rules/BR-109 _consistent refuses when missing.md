---
code: BR-109
category: guard
tags:
  - ba/rule
maturity: approved
---
# _consistent refuses when missing

## Statement

In _consistent, when missing: the code raises ValueError. Located at src/ai_usage_cost/pricing.py lines 281-282.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_consistent | inferred
  > if missing:
