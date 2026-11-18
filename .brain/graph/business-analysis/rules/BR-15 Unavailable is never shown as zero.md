---
code: BR-15
tags:
  - ba/rule
maturity: approved
---
# Unavailable is never shown as zero

## Statement

When a log does not carry a value, the dashboard shows it as unavailable instead of a zero or a guess.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/Sources.tsx | inferred
  > unavailable: 'the log does not carry it',
- [[Code of localtokenomics]] @ enforced-by -> web/src/SessionWorkspace.tsx | inferred
  > return 'This client logs no token counts, so cost is left blank instead of guessed.'
