---
code: BR-95
category: guard
tags:
  - ba/rule
maturity: approved
---
# _roots refuses when not path

## Statement

In _roots, when not path: the code raises typer.BadParameter. Located at src/ai_usage_cost/cli.py lines 65-66.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/cli.py::_roots | inferred
  > if not path:
