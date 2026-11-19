---
code: BR-58
category: pricing
subdomain: Cost pricing
tags:
  - ba/rule
maturity: approved
---
# Only listed suffixes count as the same model

## Statement

A remainder after a row's match key counts as the same model only when it is a dated snapshot, a context window tag, a version or latest. `src/ai_usage_cost/pricing.py:221`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_BENIGN_SUFFIX | inferred
  > _BENIGN_SUFFIX = re.compile(
