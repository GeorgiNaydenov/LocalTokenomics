---
archetype: entity
subdomain: Spend reporting
tags:
  - ba/model
maturity: draft
---
# SessionRow

## Description

One session in a report: its time span, models, summed tokens and cost, worst cost state and rating. `src/ai_usage_cost/aggregate.py:48`

## Attributes

- session_id, source, client, provider: identity
- start_time, end_time, request_count, tokens, cost, reported_cost
- cost_state: worst of its requests; outcome, traced, error_count, title

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::SessionRow | inferred
  > class SessionRow(BaseModel):
