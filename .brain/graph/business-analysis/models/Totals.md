---
archetype: entity
fields:
  - 'tokens: TokenUsage'
  - 'cost: CostBreakdown'
  - 'reported_cost: float | None'
  - 'events: int'
  - 'priced_events: int'
  - 'sessions: int'
  - 'first_event: datetime | None'
  - 'last_event: datetime | None'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Totals

## Description

The entity Totals, declared in src/ai_usage_cost/aggregate.py lines 26-34. It has 8 fields and 0 relations.

## Attributes

- tokens: TokenUsage
- cost: CostBreakdown
- reported_cost: float | None
- events: int
- priced_events: int
- sessions: int
- first_event: datetime | None
- last_event: datetime | None

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::Totals | inferred
  > class Totals(BaseModel):
