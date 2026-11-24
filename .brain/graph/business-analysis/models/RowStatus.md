---
archetype: entity
fields: []
tags:
  - ba/model
maturity: draft
---
# RowStatus

## Description

The entity RowStatus, declared in src/ai_usage_cost/pricing.py line 26. It is the entity that the state machine RowStatus lifecycle describes.

## Lifecycle

Lifecycle is described by [[RowStatus lifecycle]].

## Used by

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ declared-in -> src/ai_usage_cost/pricing.py::RowStatus | inferred
  > RowStatus = Literal["ga", "preview", "retired"]
