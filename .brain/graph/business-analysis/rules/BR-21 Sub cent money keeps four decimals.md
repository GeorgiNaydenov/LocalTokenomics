---
code: BR-21
tags:
  - ba/rule
maturity: approved
---
# Sub cent money keeps four decimals

## Statement

A nonzero amount under one cent is shown with up to four decimals so it never reads as zero dollars.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/format.ts | confirmed
  > return value !== 0 && Math.abs(value) < 0.01 ? moneyPrecise.format(value) : money.format(value)
