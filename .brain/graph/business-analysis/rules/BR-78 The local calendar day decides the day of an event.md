---
code: BR-78
category: reporting
subdomain: Spend reporting
tags:
  - ba/rule
maturity: approved
---
# The local calendar day decides the day of an event

## Statement

An event belongs to the machine's local calendar day, a timestamp without an offset is read as UTC, and both bucketing and date filters use the same function. `src/ai_usage_cost/models.py:146`

## Enforced in

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-14 Read a tool's SQLite store without a token count]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/models.py::local_day | inferred
  > return aware.astimezone().date()
