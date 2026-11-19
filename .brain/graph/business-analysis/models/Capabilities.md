---
archetype: entity
fields:
  - 'trace: Provenance'
  - 'tokens: Provenance'
  - 'cost: Provenance'
  - 'context: Provenance'
  - 'latency: Provenance'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Capabilities

## Description

The entity Capabilities, declared in src/ai_usage_cost/trace.py lines 104-109. It has 5 fields and 0 relations.

## Attributes

- trace: Provenance
- tokens: Provenance
- cost: Provenance
- context: Provenance
- latency: Provenance

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::Capabilities | inferred
  > class Capabilities(BaseModel):
