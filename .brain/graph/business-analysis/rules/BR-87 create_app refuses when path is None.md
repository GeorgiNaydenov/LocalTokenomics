---
code: BR-87
category: guard
tags:
  - ba/rule
maturity: approved
---
# create_app refuses when path is None

## Statement

In create_app, when path is None: the code raises HTTPException with status 503, message "this analysis was built without a store". Located at src/ai_usage_cost/api.py lines 222-223.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/api.py::create_app | inferred
  > if path is None:
