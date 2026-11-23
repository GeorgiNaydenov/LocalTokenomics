---
code: RSK-43
tags:
  - ba/risk
maturity: draft
---
# Overview panels read the first item of a list without a guard

## Risk

The cost by model panel reads the first ranked model and the project panel reads the first project to write its title. With real data and an empty list both would fail. Averages and shares also divide by totals without a zero check.

## Mitigation

Add an empty state for each panel before the layout is ported.

## Sources

- [[Code of localtokenomics]] | confirmed
  > const top = ranked[0]
- [[Code of localtokenomics]] | confirmed
  > const averagePerSession = TOTALS.cost / TOTALS.sessions
