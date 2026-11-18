---
code: BR-53
tags:
  - ba/rule
maturity: approved
---
# Export accepts only json and png

## Statement

The export command refuses any other extension with exit code 2.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/cli.py::export | confirmed
  > raise typer.Exit(code=2)
