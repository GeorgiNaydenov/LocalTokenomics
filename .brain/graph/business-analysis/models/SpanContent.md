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

## Used by

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-14 Read a tool's SQLite store without a token count]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::SpanContent | inferred
  > class SpanContent(BaseModel):
