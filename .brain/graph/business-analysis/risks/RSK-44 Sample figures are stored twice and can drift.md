---
code: RSK-44
tags:
  - ba/risk
maturity: draft
---
# Sample figures are stored twice and can drift

## Risk

The spend of each model is written once in the model list and once in the rate table, for example the figure of the top model, with no link between them. An edit to one copy leaves the other stale, and the overview and pricing screens would disagree.

## Mitigation

Derive one list from the other, or add a test that compares them.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/data.ts | confirmed
  > cost: 1489.22,
- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/data.ts | confirmed
  > spend: 1489.22
