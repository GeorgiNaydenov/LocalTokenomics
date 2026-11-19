---
archetype: entity
fields:
  - 'kind: str'
  - 'severity: Literal[''info'', ''warning'', ''critical'']'
  - 'span_id: str'
  - 'message: str'
  - 'count: int'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Insight

## Description

The entity Insight, declared in src/ai_usage_cost/trace.py lines 184-189. It has 5 fields and 0 relations.

## Attributes

- kind: str
- severity: Literal['info', 'warning', 'critical']
- span_id: str
- message: str
- count: int

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::Insight | inferred
  > class Insight(BaseModel):
