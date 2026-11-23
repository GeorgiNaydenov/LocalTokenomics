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

## Used by

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-14 Read a tool's SQLite store without a token count]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::Economics | inferred
  > class Economics(BaseModel):
