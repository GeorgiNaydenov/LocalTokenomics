---
code: BR-92
category: guard
tags:
  - ba/rule
maturity: approved
---
# forget_session refuses when not store.session_exists(conn, source, session_id)

## Statement

In forget_session, when not store.session_exists(conn, source, session_id): the code raises HTTPException with status 404. Located at src/ai_usage_cost/api.py lines 364-365.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/api.py::forget_session | inferred
  > if not store.session_exists(conn, source, session_id):
