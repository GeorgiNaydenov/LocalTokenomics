---
type: core
tags:
  - ba/subdomain
maturity: draft
---
# Spend reporting

## Description

Joins priced requests into totals, buckets, sessions, facets and warning groups and presents them on the command line and over HTTP. Main code: `src/ai_usage_cost/pipeline.py:166`, `src/ai_usage_cost/aggregate.py:675`, `src/ai_usage_cost/cli.py:24` and `src/ai_usage_cost/api.py:198`.

## Sources

- [[Code of localtokenomics]] @ bounded-by -> src/ai_usage_cost/aggregate.py::build_report | inferred
  > def build_report(
