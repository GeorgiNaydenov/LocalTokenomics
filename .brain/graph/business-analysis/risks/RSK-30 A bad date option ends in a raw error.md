---
code: RSK-30
impact: A mistyped since or until value shows a Python error instead of a usage message
likelihood: medium
tags:
  - ba/risk
maturity: draft
---
# A bad date option ends in a raw error

## Risk

Dates are parsed with no guard `src/ai_usage_cost/cli.py:45`.

## Mitigation

Not found in the code.
