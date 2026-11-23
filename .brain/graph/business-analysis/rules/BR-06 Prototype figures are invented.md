---
code: BR-06
tags:
  - ba/rule
maturity: approved
---
# Prototype figures are invented

## Statement

The headline totals are literal numbers and the session list is generated from a few seed sessions.

## Enforced in

- [[UC-01 Compare a dashboard screen with its reference]]
- [[UC-05 Read usage and cost for a period]]
- [[UC-07 Rate a session outcome]]
- [[UC-28 Sort the session list and open one session in the prototype]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/data.ts | confirmed
  > cost: 3_431.96,
- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/data.ts | confirmed
  > for (let index = 0; generated.length + seeded.length < 184; index++) {
