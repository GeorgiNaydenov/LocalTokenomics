---
code: BR-118
category: calculation
subdomain: Spend reporting
tags:
  - ba/rule
maturity: draft
---
# An alert fires only above the threshold

## Statement

The alert fires when the compared amount is strictly greater than the threshold; an equal amount sends nothing. `src/ai_usage_cost/cli.py:282`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/cli.py::alert_decision | inferred
  > return AlertDecision(fire=amount > threshold, message="\n".join(lines))
