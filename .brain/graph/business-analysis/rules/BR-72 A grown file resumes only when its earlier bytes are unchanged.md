---
code: BR-72
category: performance
subdomain: Usage collection
tags:
  - ba/rule
maturity: approved
---
# A grown file resumes only when its earlier bytes are unchanged

## Statement

A file is read from its old end only when its source has a resume hook, it only grew, the previous scan reached its old end and a hash of the bytes before that point still matches. `src/ai_usage_cost/store.py:250`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/store.py::ingest | inferred
  > _boundary_hash(path, prior[1]) == prior[4]
