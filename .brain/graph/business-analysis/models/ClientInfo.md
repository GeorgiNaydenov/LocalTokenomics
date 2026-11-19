---
archetype: entity
fields:
  - 'id: str'
  - 'label: str'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# ClientInfo

## Description

The entity ClientInfo, declared in src/ai_usage_cost/api.py lines 86-88. It has 2 fields and 0 relations.

## Attributes

- id: str
- label: str

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/api.py::ClientInfo | inferred
  > class ClientInfo(BaseModel):
