---
archetype: entity
subdomain: Cost pricing
fields:
  - 'uncached_input: int'
  - 'cache_read: int'
  - 'cache_write_5m: int'
  - 'cache_write_1h: int'
  - 'output: int'
  - 'reasoning_output: int'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# TokenUsage

## Description

The entity TokenUsage, declared in src/ai_usage_cost/models.py lines 12-43. It has 6 fields and 0 relations.

## Attributes

- uncached_input: int
- cache_read: int
- cache_write_5m: int
- cache_write_1h: int
- output: int
- reasoning_output: int

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::TokenUsage | inferred
  > class TokenUsage(BaseModel):
