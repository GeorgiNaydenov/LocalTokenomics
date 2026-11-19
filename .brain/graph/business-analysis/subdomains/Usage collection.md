---
type: supporting
tags:
  - ba/subdomain
maturity: approved
---
# Usage collection

## Description

Finds the logs and databases that AI coding tools write, parses changed files and keeps one stored request per fingerprint. Main code: `src/ai_usage_cost/store.py:190` and `src/ai_usage_cost/sources/base.py:18`.

## Sources

- [[Code of localtokenomics]] @ bounded-by -> src/ai_usage_cost/store.py::ingest | inferred
  > def ingest(
