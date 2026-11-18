---
archetype: aggregate root
subdomain: Cost pricing
tags:
  - ba/model
maturity: draft
---
# RateTable

## Description

The loaded rates.json: model rows, provider cache rules, gateway prefixes and models known to have no price. `src/ai_usage_cost/pricing.py:252`

## Attributes

- as_of, currency, units, notes
- models: rows keyed by a match prefix
- providers: cache and batch rules per provider
- prefixes, unpriced_models

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/pricing.py::RateTable | inferred
  > class RateTable(BaseModel):
