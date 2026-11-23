---
code: BR-111
category: guard
tags:
  - ba/rule
maturity: approved
---
# resolve_path refuses when index >= len(current)

## Statement

In resolve_path, when index >= len(current): the code raises ContentUnavailable. Located at src/ai_usage_cost/privacy.py lines 109-110.

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/privacy.py::resolve_path | inferred
  > if index >= len(current):
