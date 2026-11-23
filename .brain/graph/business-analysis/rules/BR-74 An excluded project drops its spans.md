---
code: BR-74
category: privacy
subdomain: Privacy and retention
tags:
  - ba/rule
maturity: approved
---
# An excluded project drops its spans

## Statement

A span whose project equals an excluded entry, or whose working directory starts with it, is not stored. `src/ai_usage_cost/store.py:314`

## Enforced in

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]
- [[UC-25 Sample GPU use for local models]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/store.py::_in_excluded_project | inferred
  > directory.startswith(entry)
