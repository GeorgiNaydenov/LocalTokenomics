---
code: BR-45
tags:
  - ba/rule
maturity: approved
---
# Experimental readers carry a flag

## Statement

A reader whose parser has not been checked against a real session sets experimental to true.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/sources/base.py | inferred
  > experimental: bool = False
