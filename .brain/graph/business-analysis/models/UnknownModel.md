---
archetype: entity
fields:
  - 'model: str'
  - 'tokens: int'
  - 'events: int'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# UnknownModel

## Description

The entity UnknownModel, declared in src/ai_usage_cost/aggregate.py lines 77-80. It has 3 fields and 0 relations.

## Attributes

- model: str
- tokens: int
- events: int

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::UnknownModel | inferred
  > class UnknownModel(BaseModel):
