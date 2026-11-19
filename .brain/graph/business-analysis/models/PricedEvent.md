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
maturity: approved
---
# PricedEvent

## Description

The entity PricedEvent, declared in src/ai_usage_cost/models.py lines 117-120. It has 3 fields and 0 relations.

## Attributes

- event: UsageEvent
- cost: CostBreakdown | None
- state: CostState

## Lifecycle

Lifecycle is described by [[CostState lifecycle]].

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::PricedEvent | inferred
  > class PricedEvent(BaseModel):
