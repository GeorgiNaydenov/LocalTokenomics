---
archetype: entity
subdomain: Cost pricing
fields:
  - 'uncached_input: float'
  - 'cache_read: float'
  - 'cache_write: float'
  - 'output: float'
  - 'no_cache_equivalent: float'
  - 'estimated: bool'
  - 'tier_unpriced: bool'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# CostBreakdown

## Description

The entity CostBreakdown, declared in src/ai_usage_cost/models.py lines 75-114. It has 7 fields and 0 relations.

## Attributes

- uncached_input: float
- cache_read: float
- cache_write: float
- output: float
- no_cache_equivalent: float
- estimated: bool
- tier_unpriced: bool

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::CostBreakdown | inferred
  > class CostBreakdown(BaseModel):
