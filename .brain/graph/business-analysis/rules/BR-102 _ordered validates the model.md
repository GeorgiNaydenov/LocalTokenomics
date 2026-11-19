---
code: BR-102
category: validator
tags:
  - ba/rule
maturity: approved
---
# _ordered validates the model

## Statement

In _ordered, the model: the code validates before accepting the value. Located at src/ai_usage_cost/pricing.py lines 90-93.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_ordered | inferred
  > def _ordered(self) -> Period:
