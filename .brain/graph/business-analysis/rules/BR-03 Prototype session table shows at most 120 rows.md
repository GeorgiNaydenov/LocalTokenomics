---
code: BR-03
tags:
  - ba/rule
maturity: approved
---
# Prototype session table shows at most 120 rows

## Statement

The prototype sorts all sessions and then displays only the first 120.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/data.ts | confirmed
  > export const SESSION_LIMIT = 120
- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/SessionsScreen.tsx | confirmed
  > const shown = sorted.slice(0, SESSION_LIMIT)
