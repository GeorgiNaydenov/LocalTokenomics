---
archetype: entity
fields:
  - 'cache_read: float'
  - 'cache_write_5m: float'
  - 'cache_write_1h: float'
  - 'batch: float'
  - 'free: bool'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# ProviderRules

## Description

The entity ProviderRules, declared in src/ai_usage_cost/pricing.py lines 101-106. It has 5 fields and 0 relations.

## Attributes

- cache_read: float
- cache_write_5m: float
- cache_write_1h: float
- batch: float
- free: bool

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/pricing.py::ProviderRules | inferred
  > class ProviderRules(BaseModel):
