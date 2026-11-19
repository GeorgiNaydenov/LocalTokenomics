---
code: BR-98
category: guard
tags:
  - ba/rule
maturity: approved
---
# alert refuses when threshold is None

## Statement

In alert, when threshold is None: the code raises typer.BadParameter, message "pass --over (window total) or --rise-over (rise vs before)". Located at src/ai_usage_cost/cli.py lines 325-326.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/cli.py::alert | inferred
  > if threshold is None:
