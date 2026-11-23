---
code: BR-16
tags:
  - ba/rule
maturity: approved
---
# Unpriced cost stays out of totals

## Statement

A session whose model matches no rate entry shows its tokens but its cost is kept out of totals.

## Enforced in

- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/SessionWorkspace.tsx | inferred
  > return 'Tokens are counted, no rate entry matches this model, so cost stays out of totals.'
