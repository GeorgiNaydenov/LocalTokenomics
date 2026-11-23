---
code: BR-03
tags:
  - ba/rule
maturity: approved
---
# Prototype session table shows at most 120 rows

## Statement

The prototype sorts all sessions and then displays only the first 120.

## Enforced in

- [[UC-01 Compare a dashboard screen with its reference]]
- [[UC-05 Read usage and cost for a period]]
- [[UC-07 Rate a session outcome]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-10 Narrow a list and choose its columns]]
- [[UC-28 Sort the session list and open one session in the prototype]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/data.ts | confirmed
  > export const SESSION_LIMIT = 120
- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/SessionsScreen.tsx | confirmed
  > const shown = sorted.slice(0, SESSION_LIMIT)
