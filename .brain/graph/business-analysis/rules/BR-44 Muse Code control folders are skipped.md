---
code: BR-44
tags:
  - ba/rule
maturity: approved
---
# Muse Code control folders are skipped

## Statement

The Muse Code reader skips the view and model catalog folders when it lists session files.

## Enforced in

- [[UC-13 Discover AI tool usage from local files]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/sources/muse_code.py | inferred
  > _SKIP_DIRS = frozenset({".msp-view-v1", "model-catalog"})
