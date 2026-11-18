---
code: BR-43
tags:
  - ba/rule
maturity: approved
---
# Repeated Codex token totals are not counted twice

## Statement

A Codex token_count record whose total is unchanged is skipped, because Codex repeats it on rate limit updates.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/sources/codex.py | inferred
  > if total == previous_total_snapshot:
