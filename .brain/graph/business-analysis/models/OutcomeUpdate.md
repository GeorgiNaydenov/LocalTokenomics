---
archetype: entity
fields:
  - 'outcome: OutcomeLabel'
  - 'notes: str'
  - 'tags: list[str]'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# OutcomeUpdate

## Description

The entity OutcomeUpdate, declared in src/ai_usage_cost/trace.py lines 141-144. It has 3 fields and 0 relations.

## Attributes

- outcome: OutcomeLabel
- notes: str
- tags: list[str]

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::OutcomeUpdate | inferred
  > class OutcomeUpdate(BaseModel):
