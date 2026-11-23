---
code: BR-72
category: performance
subdomain: Usage collection
tags:
  - ba/rule
maturity: approved
---
# A grown file resumes only when its earlier bytes are unchanged

## Statement

A file is read from its old end only when its source has a resume hook, it only grew, the previous scan reached its old end and a hash of the bytes before that point still matches. `src/ai_usage_cost/store.py:250`

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
  > _boundary_hash(path, prior[1]) == prior[4]
