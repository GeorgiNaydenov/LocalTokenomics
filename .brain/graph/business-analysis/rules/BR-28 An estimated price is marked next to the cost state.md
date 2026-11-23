---
code: BR-28
category: display
tags:
  - ba/rule
maturity: approved
---
# An estimated price is marked next to the cost state

## Statement

A priced row that used a sibling model's rate gets an Estimated badge in a purple hue, so it is not mistaken for an unpriced row, which is left out of totals.

## Enforced in

- [[UC-01 Compare a dashboard screen with its reference]]
- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-12 Review a session's spans and context use]]
- [[UC-28 Sort the session list and open one session in the prototype]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/status.tsx::CostBadges | confirmed
  >       {isEstimatedPriced(state, cost) ? <EstimatedBadge className={className} /> : null}
