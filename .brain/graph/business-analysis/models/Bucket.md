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

## Used by

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-14 Read a tool's SQLite store without a token count]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::Bucket | inferred
  > class Bucket(BaseModel):
