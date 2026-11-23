---
code: BR-19
tags:
  - ba/rule
maturity: approved
---
# Cache price derivation

## Statement

A cache price is the published figure when present, otherwise the input price times the provider ratio, otherwise it is not shown.

## Enforced in

- [[UC-05 Read usage and cost for a period]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/pricing-format.ts | confirmed
  > return rate.input * rules[field]
