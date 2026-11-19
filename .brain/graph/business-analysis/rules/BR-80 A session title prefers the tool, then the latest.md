---
code: BR-80
category: reporting
subdomain: Spend reporting
tags:
  - ba/rule
maturity: approved
---
# A session title prefers the tool, then the latest

## Statement

The title of a session comes from the highest ranked title source among its events, a tool title first and a folder fallback last, and among equals the latest wins. `src/ai_usage_cost/aggregate.py:21`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/aggregate.py::_TITLE_SOURCE_RANK | inferred
  > Lower rank wins when picking a session's display title
