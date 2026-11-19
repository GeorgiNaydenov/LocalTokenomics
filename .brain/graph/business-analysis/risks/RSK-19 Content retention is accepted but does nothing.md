---
code: RSK-19
impact: A person may expect text to expire
likelihood: low
tags:
  - ba/risk
maturity: approved
---
# Content retention is accepted but does nothing

## Risk

The setting is read but no content is stored `src/ai_usage_cost/pipeline.py:242`.

## Mitigation

The pipeline adds a warning when it is set.
