---
archetype: entity
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
maturity: approved
---
# RateTable

## Description

The entity RateTable, declared in src/ai_usage_cost/pricing.py lines 252-372. It has 11 fields and 0 relations.

## Attributes

- as_of: str
- currency: str
- units: str
- notes: list[str]
- prefixes: list[Prefix]
- providers: dict[str, ProviderRules]
- models: list[ModelRate]
- unpriced_models: list[UnpricedModel]
- _lookup_cache: dict[str, ModelRate | None]
- _rules_cache: dict[str, ProviderRules]
- _prefix_cache: list[Prefix] | None

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/pricing.py::RateTable | inferred
  > class RateTable(BaseModel):
