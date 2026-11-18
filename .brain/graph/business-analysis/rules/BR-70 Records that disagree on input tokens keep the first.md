---
code: BR-70
category: data integrity
subdomain: Usage collection
tags:
  - ba/rule
maturity: draft
---
# Records that disagree on input tokens keep the first

## Statement

When two records for one request disagree on input tokens, the first is kept and a warning is added. `src/ai_usage_cost/store.py:352`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/store.py::_insert | inferred
  > disagree on input tokens -- keeping the first
