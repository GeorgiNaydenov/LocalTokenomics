---
archetype: entity
subdomain: Usage collection
tags:
  - ba/model
maturity: draft
---
# UsageEvent

## Description

One request read from a log: who made it, when, with which model and how many tokens, plus project and title context. `src/ai_usage_cost/models.py:49`

## Attributes

- source, client, session_id, timestamp: required
- provider, model, request_id, tokens: optional; tokens is None when the log has no counts
- tier: service tier, default standard
- reported_cost: the cost the tool itself logged, kept beside the computed one

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::UsageEvent | inferred
  > class UsageEvent(BaseModel):
