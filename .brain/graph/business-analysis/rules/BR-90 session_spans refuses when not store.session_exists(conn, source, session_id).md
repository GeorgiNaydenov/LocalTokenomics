---
code: BR-90
category: guard
tags:
  - ba/rule
maturity: approved
---
# session_spans refuses when not store.session_exists(conn, source, session_id)

## Statement

In session_spans, when not store.session_exists(conn, source, session_id): the code raises HTTPException with status 404. Located at src/ai_usage_cost/api.py lines 235-236.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/api.py::session_spans | inferred
  > if not store.session_exists(conn, source, session_id):
