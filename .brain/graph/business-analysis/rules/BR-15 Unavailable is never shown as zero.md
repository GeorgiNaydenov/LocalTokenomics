---
code: BR-15
tags:
  - ba/rule
maturity: approved
---
# Unavailable is never shown as zero

## Statement

When a log does not carry a value, the dashboard shows it as unavailable instead of a zero or a guess.

## Enforced in

- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/Sources.tsx | inferred
  > unavailable: 'the log does not carry it',
- [[Code of localtokenomics]] @ enforced-by -> web/src/SessionWorkspace.tsx | inferred
  > return 'This client logs no token counts, so cost is left blank instead of guessed.'
