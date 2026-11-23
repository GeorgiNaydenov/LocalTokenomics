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

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_disjoint_periods | inferred
  > if earlier.until is None or (later.from_ or date.min) < earlier.until:
