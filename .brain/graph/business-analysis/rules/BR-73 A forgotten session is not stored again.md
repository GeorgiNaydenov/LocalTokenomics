---
code: BR-73
category: privacy
subdomain: Privacy and retention
tags:
  - ba/rule
maturity: approved
---
# A forgotten session is not stored again

## Statement

After a person forgets a session its spans and rating are deleted and an exclusion row keeps its spans out of later scans. Its requests stay. `src/ai_usage_cost/store.py:273`

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
  > if (span.source, span.session_id) in excluded_sessions:
