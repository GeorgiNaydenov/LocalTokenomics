---
code: BR-105
category: validator
tags:
  - ba/rule
maturity: approved
---
# _disjoint_periods validates the model

## Statement

In _disjoint_periods, the model: the code validates before accepting the value. Located at src/ai_usage_cost/pricing.py lines 153-160.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_disjoint_periods | inferred
  > def _disjoint_periods(self) -> ModelRate:
