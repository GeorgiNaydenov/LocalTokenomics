---
archetype: entity
fields:
  - 'states: dict[str, int]'
  - 'clients: dict[str, int]'
  - 'models: dict[str, int]'
  - 'projects: dict[str, int]'
  - 'outcomes: dict[str, int]'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Facets

## Description

The entity Facets, declared in src/ai_usage_cost/aggregate.py lines 454-459. It has 5 fields and 0 relations.

## Attributes

- states: dict[str, int]
- clients: dict[str, int]
- models: dict[str, int]
- projects: dict[str, int]
- outcomes: dict[str, int]

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::Facets | inferred
  > class Facets(BaseModel):
