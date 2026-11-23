---
code: BR-22
tags:
  - ba/rule
maturity: approved
---
# Unattributed turn is excluded from rankings

## Statement

Turn rankings and insights ignore the row for spend outside any turn.

## Enforced in

- [[UC-05 Read usage and cost for a period]]
- [[UC-07 Rate a session outcome]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/turn-insights.ts | confirmed
  > return rows.filter((row) => row.key !== UNATTRIBUTED_TURN_KEY)
