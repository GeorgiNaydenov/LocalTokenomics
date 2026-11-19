---
code: BR-106
category: guard
tags:
  - ba/rule
maturity: approved
---
# _disjoint_periods refuses when earlier.until is None or (later.from_ or date.min) < ea

## Statement

In _disjoint_periods, when earlier.until is None or (later.from_ or date.min) < earlier.until: the code raises ValueError. Located at src/ai_usage_cost/pricing.py lines 158-159.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_disjoint_periods | inferred
  > if earlier.until is None or (later.from_ or date.min) < earlier.until:
