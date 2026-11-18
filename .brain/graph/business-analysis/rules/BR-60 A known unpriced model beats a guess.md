---
code: BR-60
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: draft
---
# A known unpriced model beats a guess

## Statement

An unpriced entry at least as specific as the matching row stops a prefix estimate, so a variant of a priced model is not guessed from its parent. `src/ai_usage_cost/pricing.py:314`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::RateTable.lookup | inferred
  > An unpriced entry at least as specific as the row
