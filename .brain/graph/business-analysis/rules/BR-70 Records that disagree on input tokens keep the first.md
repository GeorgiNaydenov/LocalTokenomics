---
code: BR-70
category: data integrity
subdomain: Usage collection
tags:
  - ba/rule
maturity: approved
---
# Records that disagree on input tokens keep the first

## Statement

When two records for one request disagree on input tokens, the first is kept and a warning is added. `src/ai_usage_cost/store.py:352`

## Enforced in

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]
- [[UC-25 Sample GPU use for local models]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/store.py::_insert | inferred
  > disagree on input tokens -- keeping the first
