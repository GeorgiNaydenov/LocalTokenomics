---
code: BR-96
category: guard
tags:
  - ba/rule
maturity: approved
---
# alert refuses when days < 1

## Statement

In alert, when days < 1: the code raises typer.BadParameter, message "--days must be at least 1". Located at src/ai_usage_cost/cli.py lines 320-321.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/cli.py::alert | inferred
  > if days < 1:
