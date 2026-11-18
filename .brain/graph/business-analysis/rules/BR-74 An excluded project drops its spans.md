---
code: BR-74
category: privacy
subdomain: Privacy and retention
tags:
  - ba/rule
maturity: draft
---
# An excluded project drops its spans

## Statement

A span whose project equals an excluded entry, or whose working directory starts with it, is not stored. `src/ai_usage_cost/store.py:314`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/store.py::_in_excluded_project | inferred
  > directory.startswith(entry)
