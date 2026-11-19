---
code: BR-88
category: guard
tags:
  - ba/rule
maturity: approved
---
# opened refuses when path is None

## Statement

In opened, when path is None: the code raises HTTPException with status 503, message "this analysis was built without a store". Located at src/ai_usage_cost/api.py lines 222-223.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/api.py::opened | inferred
  > if path is None:
