---
persists_models:
  - UsageEvent
  - Span
  - Outcome
tags:
  - arch/data-store
maturity: approved
---
# Usage store

## Description

A SQLite file in the home folder that holds requests, files, trace events, outcomes, exclusions and GPU samples: `src/ai_usage_cost/pipeline.py:28`.

## Sources

- [[Code of localtokenomics]] @ declared-in -> src/ai_usage_cost/pipeline.py::DEFAULT_DB_PATH | inferred
  > DEFAULT_DB_PATH = Path.home()
