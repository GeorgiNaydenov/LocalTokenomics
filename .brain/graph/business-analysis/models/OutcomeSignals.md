---
archetype: entity
fields:
  - 'aborted_turns: int'
  - 'interrupted_tools: int'
  - 'errors: int'
  - 'last_turn_status: SpanStatus'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# OutcomeSignals

## Description

The entity OutcomeSignals, declared in src/ai_usage_cost/trace.py lines 134-138. It has 4 fields and 0 relations.

## Attributes

- aborted_turns: int
- interrupted_tools: int
- errors: int
- last_turn_status: SpanStatus

## Lifecycle

Lifecycle is described by [[SpanStatus lifecycle]].

## Used by

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-14 Read a tool's SQLite store without a token count]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::OutcomeSignals | inferred
  > class OutcomeSignals(BaseModel):
