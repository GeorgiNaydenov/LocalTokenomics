---
archetype: entity
fields:
  - 'totals: EconRow'
  - 'by_turn: list[EconRow]'
  - 'by_model: list[EconRow]'
  - 'by_tool: list[EconRow]'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Economics

## Description

The entity Economics, declared in src/ai_usage_cost/trace.py lines 177-181. It has 4 fields and 0 relations.

## Attributes

- totals: EconRow
- by_turn: list[EconRow]
- by_model: list[EconRow]
- by_tool: list[EconRow]

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::Economics | inferred
  > class Economics(BaseModel):
