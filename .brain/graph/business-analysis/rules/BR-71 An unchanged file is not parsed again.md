---
code: BR-71
category: performance
subdomain: Usage collection
tags:
  - ba/rule
maturity: approved
---
# An unchanged file is not parsed again

## Statement

A file whose modification time, size and parser version match the stored values is skipped. `src/ai_usage_cost/store.py:229`

## Enforced in

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]
- [[UC-25 Sample GPU use for local models]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/store.py::ingest | inferred
  > (mtime, size, PARSER_VERSION) == prior[:3]
