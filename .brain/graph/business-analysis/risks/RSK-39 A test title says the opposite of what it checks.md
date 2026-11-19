---
code: RSK-39
impact: low
likelihood: low
tags:
  - ba/risk
maturity: draft
---
# A test title says the opposite of what it checks

## Risk

The rank test named picks measured as the best expects the result derived, which is the worst of the two inputs, so the title misleads a reader of the test list. `web/src/components/rank.test.ts:28`

## Mitigation

Rename the test to say that the worse of measured and derived wins.
