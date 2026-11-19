---
archetype: entity
subdomain: Spend reporting
fields:
  - 'key: str'
  - 'label: str'
  - 'tokens: TokenUsage'
  - 'cost: CostBreakdown'
  - 'events: int'
  - 'sessions: int'
  - 'reported_cost: float | None'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Bucket

## Description

The entity Bucket, declared in src/ai_usage_cost/models.py lines 123-134. It has 7 fields and 0 relations.

## Attributes

- key: str
- label: str
- tokens: TokenUsage
- cost: CostBreakdown
- events: int
- sessions: int
- reported_cost: float | None

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::Bucket | inferred
  > class Bucket(BaseModel):
