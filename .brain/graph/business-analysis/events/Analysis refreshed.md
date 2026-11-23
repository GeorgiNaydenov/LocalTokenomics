---
tags:
  - ba/event
maturity: draft
---
# Analysis refreshed

## Description

Happens when the dashboard asks for a refresh: the analysis is rebuilt and the span cache is cleared. `src/ai_usage_cost/api.py:391`

## Used by

- [[UC-13 Discover AI tool usage from local files]]

## Sources

- [[Code of localtokenomics]] | inferred
  > state["analysis"] = analyze(db_path=db_path, roots=roots, rates_path=rates_path)
