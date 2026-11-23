---
tags:
  - ba/event
maturity: draft
---
# GPU sample recorded

## Description

Written once per successful reading of the GPU sampler, into the samples table. `src/ai_usage_cost/collect.py:275`

## Used by

- [[UC-13 Discover AI tool usage from local files]]

## Sources

- [[Code of localtokenomics]] | inferred
  > def insert_sample(conn: sqlite3.Connection, sample: Sample) -> None:
