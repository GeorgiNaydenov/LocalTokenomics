---
archetype: value object
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
maturity: draft
---
# Bucket

## Description

A group of priced events under one key such as a client, provider, model, project or day, with summed tokens and cost. `src/ai_usage_cost/models.py:123`

## Attributes

- key, label, tokens, cost, events, sessions, reported_cost

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::Bucket | inferred
  > class Bucket(BaseModel):
