---
archetype: entity
fields:
  - 'span_id: str'
  - 'content: str'
  - 'truncated: bool'
  - 'redactions: int'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# SpanContent

## Description

The entity SpanContent, declared in src/ai_usage_cost/trace.py lines 201-205. It has 4 fields and 0 relations.

## Attributes

- span_id: str
- content: str
- truncated: bool
- redactions: int

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::SpanContent | inferred
  > class SpanContent(BaseModel):
