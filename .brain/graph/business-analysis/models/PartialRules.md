---
archetype: entity
fields:
  - 'cache_read: float | None'
  - 'cache_write_5m: float | None'
  - 'cache_write_1h: float | None'
  - 'batch: float | None'
  - 'free: bool | None'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# PartialRules

## Description

The entity PartialRules, declared in src/ai_usage_cost/pricing.py lines 109-117. It has 5 fields and 0 relations.

## Attributes

- cache_read: float | None
- cache_write_5m: float | None
- cache_write_1h: float | None
- batch: float | None
- free: bool | None

## Lifecycle

No lifecycle field was found in the code.

## Used by

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/pricing.py::PartialRules | inferred
  > class PartialRules(BaseModel):
