---
code: BR-45
tags:
  - ba/rule
maturity: approved
---
# Experimental readers carry a flag

## Statement

A reader whose parser has not been checked against a real session sets experimental to true.

## Enforced in

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-14 Read a tool's SQLite store without a token count]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-22 Forget a session]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/sources/base.py | inferred
  > experimental: bool = False
