---
code: BR-40
tags:
  - ba/rule
maturity: approved
---
# A reader is found by its SOURCE value

## Statement

The registry keeps the SOURCE of every module in the readers package except the base module, so adding a reader needs no list edit.

## Enforced in

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/sources/__init__.py | inferred
  > source = getattr(module, "SOURCE", None)
