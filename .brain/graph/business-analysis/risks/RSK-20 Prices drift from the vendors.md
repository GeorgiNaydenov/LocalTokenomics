---
code: RSK-20
impact: Cost figures can be wrong without any warning until the table is 30 days old
likelihood: medium
tags:
  - ba/risk
maturity: approved
---
# Prices drift from the vendors

## Risk

The table carries an as of date and warns only after a fixed age `src/ai_usage_cost/aggregate.py:179`.

## Mitigation

Estimated, unpriced and tier gaps are warned about each scan.
