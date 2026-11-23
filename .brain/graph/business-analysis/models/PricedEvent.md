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

## Used by

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-14 Read a tool's SQLite store without a token count]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::PricedEvent | inferred
  > class PricedEvent(BaseModel):
