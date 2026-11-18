---
code: RSK-16
impact: The by day buckets and the series can place the same event on different days near midnight
likelihood: medium
tags:
  - ba/risk
maturity: draft
---
# Daily series uses the UTC date

## Risk

Buckets by day use the local day `src/ai_usage_cost/aggregate.py:704` while the series uses `src/ai_usage_cost/aggregate.py:544`.

## Mitigation

Not found in the code. See the open question on the series day.
