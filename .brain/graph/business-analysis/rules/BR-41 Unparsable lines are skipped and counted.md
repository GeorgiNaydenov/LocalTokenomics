---
code: BR-41
tags:
  - ba/rule
maturity: approved
---
# Unparsable lines are skipped and counted

## Statement

A JSON Lines reader skips lines that are not valid JSON and adds one warning per file with the count.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/sources/base.py | inferred
  > warnings.append(f"{path.name}: skipped {bad} unparsable lines")
