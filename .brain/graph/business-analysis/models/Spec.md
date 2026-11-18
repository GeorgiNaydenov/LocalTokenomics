---
archetype: entity
fields:
  - 'source_id: str'
  - 'client: str'
  - 'ext_id: str'
  - 'tokens_in_inclusive: bool'
  - 'sdk: bool'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Spec

## Description

The entity Spec, declared in src/ai_usage_cost/sources/cline.py lines 82-87. It has 5 fields and 0 relations.

## Attributes

- source_id: str
- client: str
- ext_id: str
- tokens_in_inclusive: bool
- sdk: bool

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/sources/cline.py::Spec | inferred
  > class Spec:
