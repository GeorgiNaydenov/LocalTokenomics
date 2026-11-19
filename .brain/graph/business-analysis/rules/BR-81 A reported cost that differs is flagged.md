---
code: BR-81
category: reporting
subdomain: Spend reporting
tags:
  - ba/rule
maturity: approved
---
# A reported cost that differs is flagged

## Statement

A session whose tool reported cost and computed cost differ by more than five percent of the reported figure or one cent gets a warning. Free models are never compared. `src/ai_usage_cost/pipeline.py:133`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pipeline.py::reported_cost_divergences | inferred
  > if abs(reported - computed) > max(0.05 * reported, 0.01):
