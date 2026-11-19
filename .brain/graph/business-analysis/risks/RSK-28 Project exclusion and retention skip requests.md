---
code: RSK-28
impact: Requests of an excluded or expired project keep their project, working directory and raw record in the store and in reports
likelihood: medium
tags:
  - ba/risk
maturity: draft
---
# Project exclusion and retention skip requests

## Risk

Requests are inserted without the exclusion test `src/ai_usage_cost/store.py:270` and retention deletes only trace rows `src/ai_usage_cost/store.py:302`.

## Mitigation

Not found in the code.
