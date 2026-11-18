---
code: BR-19
tags:
  - ba/rule
maturity: approved
---
# Cache price derivation

## Statement

A cache price is the published figure when present, otherwise the input price times the provider ratio, otherwise it is not shown.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/pricing-format.ts | confirmed
  > return rate.input * rules[field]
