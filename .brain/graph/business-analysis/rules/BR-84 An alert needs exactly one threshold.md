---
code: BR-84
category: reporting
subdomain: Spend reporting
tags:
  - ba/rule
maturity: approved
---
# An alert needs exactly one threshold

## Statement

The alert command needs a window length of at least one day and exactly one of a window total threshold or a rise threshold. `src/ai_usage_cost/cli.py:323`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/cli.py::alert | inferred
  > pass --over or --rise-over, not both
