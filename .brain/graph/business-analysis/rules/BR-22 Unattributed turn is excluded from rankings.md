---
code: BR-22
tags:
  - ba/rule
maturity: approved
---
# Unattributed turn is excluded from rankings

## Statement

Turn rankings and insights ignore the row for spend outside any turn.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/turn-insights.ts | confirmed
  > return rows.filter((row) => row.key !== UNATTRIBUTED_TURN_KEY)
