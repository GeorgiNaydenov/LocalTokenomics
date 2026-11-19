---
code: BR-116
category: calculation
subdomain: Spend reporting
tags:
  - ba/rule
maturity: draft
---
# The alert window ends today

## Statement

The alert reports the window of local days that ends today and starts the given number of days back, today included. `src/ai_usage_cost/cli.py:330`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/cli.py::alert | inferred
  > since = until - timedelta(days=days - 1)
