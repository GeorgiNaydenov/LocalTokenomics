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

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::OutcomeSignals | inferred
  > class OutcomeSignals(BaseModel):
