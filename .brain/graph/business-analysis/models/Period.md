---
archetype: entity
fields:
  - 'model_config: ConfigDict'
  - 'from_: date | None'
  - 'until: date | None'
  - 'input: float | None'
  - 'output: float | None'
  - 'cache_read: float | None'
  - 'cache_write_5m: float | None'
  - 'cache_write_1h: float | None'
  - 'variants: dict[str, PriceSet] | None'
  - 'bands: list[Band] | None'
  - 'peak: Peak | None'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Period

## Description

The entity Period, declared in src/ai_usage_cost/pricing.py lines 68-98. It has 11 fields and 0 relations.

## Attributes

- model_config: ConfigDict
- from_: date | None
- until: date | None
- input: float | None
- output: float | None
- cache_read: float | None
- cache_write_5m: float | None
- cache_write_1h: float | None
- variants: dict[str, PriceSet] | None
- bands: list[Band] | None
- peak: Peak | None

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/pricing.py::Period | inferred
  > class Period(BaseModel):
