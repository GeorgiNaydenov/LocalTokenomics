---
code: BR-97
category: guard
tags:
  - ba/rule
maturity: approved
---
# alert refuses when over is not None and rise_over is not None

## Statement

In alert, when over is not None and rise_over is not None: the code raises typer.BadParameter, message "pass --over or --rise-over, not both". Located at src/ai_usage_cost/cli.py lines 322-323.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/cli.py::alert | inferred
  > if over is not None and rise_over is not None:
