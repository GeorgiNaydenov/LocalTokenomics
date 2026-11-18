---
code: BR-48
tags:
  - ba/rule
maturity: approved
---
# Unknown grouping falls back to model

## Statement

A grouping name that is not model, client, provider, project or day is treated as model.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/terminal.py::render | confirmed
  > tables.get(group_by, tables["model"])
