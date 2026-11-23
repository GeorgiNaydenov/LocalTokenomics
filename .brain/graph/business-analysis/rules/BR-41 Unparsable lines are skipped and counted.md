---
code: BR-41
tags:
  - ba/rule
maturity: approved
---
# Unparsable lines are skipped and counted

## Statement

A JSON Lines reader skips lines that are not valid JSON and adds one warning per file with the count.

## Enforced in

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-14 Read a tool's SQLite store without a token count]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-22 Forget a session]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/sources/base.py | inferred
  > warnings.append(f"{path.name}: skipped {bad} unparsable lines")
