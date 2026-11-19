---
code: BR-111
category: guard
tags:
  - ba/rule
maturity: approved
---
# resolve_path refuses when index >= len(current)

## Statement

In resolve_path, when index >= len(current): the code raises ContentUnavailable. Located at src/ai_usage_cost/privacy.py lines 109-110.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/privacy.py::resolve_path | inferred
  > if index >= len(current):
