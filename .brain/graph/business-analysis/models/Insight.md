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

## Used by

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-14 Read a tool's SQLite store without a token count]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::Insight | inferred
  > class Insight(BaseModel):
