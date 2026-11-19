---
archetype: entity
subdomain: Cost pricing
tags:
  - ba/model
maturity: draft
---
# ModelRate

## Description

One row of the rate table: prices per million tokens for a model id prefix, with variants, bands, a peak window and dated periods. `src/ai_usage_cost/pricing.py:126`

## Attributes

- match, provider, display: required
- input, output, cache_read, cache_write_5m, cache_write_1h: dollars per million tokens
- variants, bands, peak, periods, cache_rules, context_window, status

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/pricing.py::ModelRate | inferred
  > class ModelRate(PriceSet):
