---
archetype: entity
subdomain: Cost pricing
fields:
  - 'event: UsageEvent'
  - 'cost: CostBreakdown | None'
  - 'state: CostState'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: draft
---
# PricedEvent

## Description

A usage event with its cost breakdown (absent when not priced) and its cost state. `src/ai_usage_cost/models.py:117`

## Attributes

- event: the usage event
- cost: breakdown or None
- state: priced, free, unpriced or unavailable

## Lifecycle

Lifecycle is described by [[CostState lifecycle]].

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::PricedEvent | inferred
  > class PricedEvent(BaseModel):
