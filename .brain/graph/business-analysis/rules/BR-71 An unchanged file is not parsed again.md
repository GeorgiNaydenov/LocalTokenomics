---
code: BR-71
category: performance
subdomain: Usage collection
tags:
  - ba/rule
maturity: approved
---
# An unchanged file is not parsed again

## Statement

A file whose modification time, size and parser version match the stored values is skipped. `src/ai_usage_cost/store.py:229`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/store.py::ingest | inferred
  > (mtime, size, PARSER_VERSION) == prior[:3]
