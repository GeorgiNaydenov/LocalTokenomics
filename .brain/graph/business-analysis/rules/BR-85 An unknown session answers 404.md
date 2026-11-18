---
code: BR-85
category: interface
subdomain: Spend reporting
tags:
  - ba/rule
maturity: draft
---
# An unknown session answers 404

## Statement

A session route for a source and session id that the store does not hold, or that was forgotten, answers 404. `src/ai_usage_cost/api.py:236`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/api.py::create_app.session_spans | inferred
  > no session {session_id!r} under source {source!r}
