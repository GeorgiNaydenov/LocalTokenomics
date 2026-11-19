---
code: BR-89
category: guard
tags:
  - ba/rule
maturity: approved
---
# create_app refuses when not store.session_exists(conn, source, session_id)

## Statement

In create_app, when not store.session_exists(conn, source, session_id): the code raises HTTPException with status 404. Located at src/ai_usage_cost/api.py lines 235-236.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/api.py::create_app | inferred
  > if not store.session_exists(conn, source, session_id):
