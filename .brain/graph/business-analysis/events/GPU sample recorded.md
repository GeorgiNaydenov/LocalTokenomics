---
tags:
  - ba/event
maturity: draft
---
# GPU sample recorded

## Description

Written once per successful reading of the GPU sampler, into the samples table. `src/ai_usage_cost/collect.py:275`

## Sources

- [[Code of localtokenomics]] @ declared-in -> src/ai_usage_cost/collect.py::insert_sample | inferred
  > def insert_sample(conn: sqlite3.Connection, sample: Sample) -> None:
