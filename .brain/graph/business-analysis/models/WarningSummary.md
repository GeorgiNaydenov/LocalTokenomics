---
archetype: entity
fields:
  - 'critical: int'
  - 'caution: int'
  - 'info: int'
  - 'total_delta_cost: float'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# WarningSummary

## Description

The entity WarningSummary, declared in src/ai_usage_cost/api.py lines 91-102. It has 4 fields and 0 relations.

## Attributes

- critical: int
- caution: int
- info: int
- total_delta_cost: float

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/api.py::WarningSummary | inferred
  > class WarningSummary(BaseModel):
