---
code: BR-107
category: validator
tags:
  - ba/rule
maturity: approved
---
# _consistent validates the model

## Statement

In _consistent, the model: the code validates before accepting the value. Located at src/ai_usage_cost/pricing.py lines 272-283.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_consistent | inferred
  > def _consistent(self) -> RateTable:
