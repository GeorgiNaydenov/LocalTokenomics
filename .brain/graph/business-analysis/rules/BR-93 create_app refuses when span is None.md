---
code: BR-93
category: guard
tags:
  - ba/rule
maturity: approved
---
# create_app refuses when span is None

## Statement

In create_app, when span is None: the code raises HTTPException with status 404. Located at src/ai_usage_cost/api.py lines 377-378.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/api.py::create_app | inferred
  > if span is None:
