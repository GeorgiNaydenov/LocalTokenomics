---
code: BR-86
category: privacy
subdomain: Usage collection
tags:
  - ba/rule
maturity: approved
---
# Source databases are opened read only

## Statement

A source database is opened with a read only URI, so the tool never changes another tool's data. `src/ai_usage_cost/sources/base.py:123`

## Enforced in

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-14 Read a tool's SQLite store without a token count]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-22 Forget a session]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/sources/base.py::read_sqlite | inferred
  > ?mode=ro
