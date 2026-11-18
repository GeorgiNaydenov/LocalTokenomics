---
code: BR-47
tags:
  - ba/rule
maturity: approved
---
# Day breakdown is listed oldest first

## Statement

Only the day grouping is sorted ascending by key; every other grouping keeps the order of the report.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/terminal.py::render | confirmed
  > ascending=group_by == "day"
