---
code: BR-40
tags:
  - ba/rule
maturity: approved
---
# A reader is found by its SOURCE value

## Statement

The registry keeps the SOURCE of every module in the readers package except the base module, so adding a reader needs no list edit.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/sources/__init__.py | inferred
  > source = getattr(module, "SOURCE", None)
