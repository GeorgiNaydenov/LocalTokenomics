---
code: BR-86
category: privacy
subdomain: Usage collection
tags:
  - ba/rule
maturity: draft
---
# Source databases are opened read only

## Statement

A source database is opened with a read only URI, so the tool never changes another tool's data. `src/ai_usage_cost/sources/base.py:123`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/sources/base.py::read_sqlite | inferred
  > ?mode=ro
