---
tags:
  - ba/event
maturity: draft
---
# Analysis refreshed

## Description

Happens when the dashboard asks for a refresh: the analysis is rebuilt and the span cache is cleared. `src/ai_usage_cost/api.py:391`

## Sources

- [[Code of localtokenomics]] @ declared-in -> src/ai_usage_cost/api.py::create_app.refresh | inferred
  > state["analysis"] = analyze(db_path=db_path, roots=roots, rates_path=rates_path)
