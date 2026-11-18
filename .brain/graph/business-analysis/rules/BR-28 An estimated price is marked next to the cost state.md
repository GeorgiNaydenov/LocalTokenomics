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

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/status.tsx::CostBadges | confirmed
  >       {isEstimatedPriced(state, cost) ? <EstimatedBadge className={className} /> : null}
