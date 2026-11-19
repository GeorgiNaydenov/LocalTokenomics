---
code: OQ-18
priority: low
tags:
  - ba/open-question
maturity: draft
---
# Is the scan helper in the shared module still needed

## Question

The shared module has a scan function that loops over roots, files and parse, but the real ingest loop in the store does its own looping with skip and resume logic. Only a test file calls the helper. Should it be removed or reused by the store?

## Sources

- [[Code of localtokenomics]] @ declared-in -> src/ai_usage_cost/sources/base.py | inferred
  > def scan(
- [[Code of localtokenomics]] @ declared-in -> src/ai_usage_cost/store.py | inferred
  > for path in source.files(root):
