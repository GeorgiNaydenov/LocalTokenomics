---
code: BR-94
category: guard
tags:
  - ba/rule
maturity: approved
---
# span_content refuses when span is None

## Statement

In span_content, when span is None: the code raises HTTPException with status 404. Located at src/ai_usage_cost/api.py lines 377-378.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/api.py::span_content | inferred
  > if span is None:
