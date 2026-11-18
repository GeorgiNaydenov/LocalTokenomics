---
code: BR-39
category: privacy
tags:
  - ba/rule
maturity: approved
---
# Readers only read

## Statement

A SQLite store is opened through a read only URI and a database error becomes a warning, so a reader never changes the file it measures.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/sources/base.py | inferred
  > uri = f"file:{path.as_posix()}?mode=ro"
