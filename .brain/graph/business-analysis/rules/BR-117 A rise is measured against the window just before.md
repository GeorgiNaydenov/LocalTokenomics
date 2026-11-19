---
code: BR-117
category: calculation
subdomain: Spend reporting
tags:
  - ba/rule
maturity: draft
---
# A rise is measured against the window just before

## Statement

With the rise threshold the earlier window has the same length and ends the day before the current window starts. `src/ai_usage_cost/cli.py:336`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/cli.py::alert | inferred
  > analysis, since=since - timedelta(days=days), until=since - timedelta(days=1)
