---
code: BR-69
category: data integrity
subdomain: Usage collection
tags:
  - ba/rule
maturity: approved
---
# A request is stored once per fingerprint

## Statement

A later record with the same fingerprint replaces an earlier one only when it carries more output, because streamed records grow and the last one holds the billed count. `src/ai_usage_cost/store.py:359`

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
  > the last (equivalently, largest) record carries the final, billed count
