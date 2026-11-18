---
code: BR-16
tags:
  - ba/rule
maturity: approved
---
# Unpriced cost stays out of totals

## Statement

A session whose model matches no rate entry shows its tokens but its cost is kept out of totals.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/SessionWorkspace.tsx | inferred
  > return 'Tokens are counted, no rate entry matches this model, so cost stays out of totals.'
