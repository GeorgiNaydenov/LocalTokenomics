---
code: BR-120
category: interface
subdomain: Spend reporting
tags:
  - ba/rule
maturity: draft
---
# A route without a store answers 503

## Statement

A route that must open the store answers 503 when the analysis was built without a store path. `src/ai_usage_cost/api.py:223`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/api.py::create_app.opened | inferred
  > raise HTTPException(503, "this analysis was built without a store")
