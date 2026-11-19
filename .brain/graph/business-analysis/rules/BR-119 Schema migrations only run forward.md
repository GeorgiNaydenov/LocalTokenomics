---
code: BR-119
category: data
subdomain: Usage collection
tags:
  - ba/rule
maturity: draft
---
# Schema migrations only run forward

## Statement

Opening the store runs every migration after the stored schema version, in list order, and records the new version after each; there is no downgrade step. `src/ai_usage_cost/store.py:147`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/store.py::open_store | inferred
  > for index, migration in enumerate(MIGRATIONS[current:], start=current):
