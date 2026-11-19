---
archetype: aggregate root
subdomain: Cost pricing
fields:
  - 'as_of: str'
  - 'currency: str'
  - 'units: str'
  - 'notes: list[str]'
  - 'prefixes: list[Prefix]'
  - 'providers: dict[str, ProviderRules]'
  - 'models: list[ModelRate]'
  - 'unpriced_models: list[UnpricedModel]'
  - '_lookup_cache: dict[str, ModelRate | None]'
  - '_rules_cache: dict[str, ProviderRules]'
  - '_prefix_cache: list[Prefix] | None'
entity_keys: []
relations_to: []
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

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/pricing.py::RateTable | inferred
  > class RateTable(BaseModel):
