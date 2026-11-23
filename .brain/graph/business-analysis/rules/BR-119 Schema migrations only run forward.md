---
code: BR-119
category: data
subdomain: Usage collection
tags:
  - ba/rule
maturity: draft
---
# Schema migrations only run forward

## Statement

Opening the store runs every migration after the stored schema version, in list order, and records the new version after each; there is no downgrade step. `src/ai_usage_cost/store.py:147`

## Enforced in

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]
- [[UC-25 Sample GPU use for local models]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/store.py::open_store | inferred
  > for index, migration in enumerate(MIGRATIONS[current:], start=current):
