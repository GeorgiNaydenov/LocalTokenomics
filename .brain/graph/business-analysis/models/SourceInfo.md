---
archetype: entity
fields:
  - 'id: str'
  - 'label: str'
  - 'clients: list[str]'
  - 'token_data: TokenData'
  - 'path: str'
  - 'root_hint: str'
  - 'detected: bool'
  - 'files: int'
  - 'capabilities: Capabilities'
  - 'experimental: bool'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# SourceInfo

## Description

The entity SourceInfo, declared in src/ai_usage_cost/pipeline.py lines 31-41. It has 10 fields and 0 relations.

## Attributes

- id: str
- label: str
- clients: list[str]
- token_data: TokenData
- path: str
- root_hint: str
- detected: bool
- files: int
- capabilities: Capabilities
- experimental: bool

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/pipeline.py::SourceInfo | inferred
  > class SourceInfo(BaseModel):
