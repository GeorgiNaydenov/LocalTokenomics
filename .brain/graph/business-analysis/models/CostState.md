---
archetype: entity
fields: []
tags:
  - ba/model
maturity: draft
---
# CostState

## Description

The entity CostState, declared in src/ai_usage_cost/models.py line 8. It is the entity that the state machine CostState lifecycle describes.

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

- [[Code of localtokenomics]] @ declared-in -> src/ai_usage_cost/models.py::CostState | inferred
  > CostState = Literal["priced", "free", "unpriced", "unavailable"]
