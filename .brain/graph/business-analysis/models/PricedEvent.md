---
archetype: entity
subdomain: Cost pricing
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

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::PricedEvent | inferred
  > class PricedEvent(BaseModel):
