---
code: BR-60
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: approved
---
# A known unpriced model beats a guess

## Statement

An unpriced entry at least as specific as the matching row stops a prefix estimate, so a variant of a priced model is not guessed from its parent. `src/ai_usage_cost/pricing.py:314`

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::RateTable.lookup | inferred
  > An unpriced entry at least as specific as the row
