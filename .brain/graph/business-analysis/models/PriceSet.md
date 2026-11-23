---
archetype: entity
fields:
  - 'input: float'
  - 'output: float'
  - 'cache_read: float | None'
  - 'cache_write_5m: float | None'
  - 'cache_write_1h: float | None'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# PriceSet

## Description

The entity PriceSet, declared in src/ai_usage_cost/pricing.py lines 29-37. It has 5 fields and 0 relations.

## Attributes

- input: float
- output: float
- cache_read: float | None
- cache_write_5m: float | None
- cache_write_1h: float | None

## Lifecycle

No lifecycle field was found in the code.

## Used by

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/pricing.py::PriceSet | inferred
  > class PriceSet(BaseModel):
