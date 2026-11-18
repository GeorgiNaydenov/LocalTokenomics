---
persists_models:
  - RateTable
  - ModelRate
tags:
  - arch/data-store
maturity: draft
---
# Rate table file

## Description

The shipped rates.json beside the pricing code, replaceable with the rates option: `src/ai_usage_cost/pricing.py:22`.

## Sources

- [[Code of localtokenomics]] @ declared-in -> src/ai_usage_cost/pricing.py::DEFAULT_RATES_PATH | inferred
  > DEFAULT_RATES_PATH = Path(__file__)
