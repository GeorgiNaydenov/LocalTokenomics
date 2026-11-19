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
maturity: draft
---
# Spec

## Description

Per tool settings shared by the Cline family readers: source id, client name, extension id, whether input tokens include cache buckets, and whether the SDK store is read.

## Attributes

- source_id: str
- client: str
- ext_id: str
- tokens_in_inclusive: bool
- sdk: bool

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/sources/cline.py | inferred
  > class Spec:
