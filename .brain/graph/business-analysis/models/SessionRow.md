---
archetype: entity
subdomain: Spend reporting
fields:
  - 'session_id: str'
  - 'source: str'
  - 'client: str'
  - 'provider: str'
  - 'models: list[str]'
  - 'start_time: datetime'
  - 'end_time: datetime'
  - 'request_count: int'
  - 'tokens: TokenUsage | None'
  - 'cost: CostBreakdown | None'
  - 'reported_cost: float | None'
  - 'cost_state: CostState'
  - 'cost_states: list[CostState]'
  - 'is_sidechain: bool'
  - 'has_sidechain: bool'
  - 'currency: str'
  - 'project: str | None'
  - 'working_directory: str | None'
  - 'repository: str | None'
  - 'branch: str | None'
  - 'machine: str'
  - 'raw_source: list[str]'
  - 'outcome: OutcomeLabel'
  - 'traced: bool'
  - 'error_count: int'
  - 'title: str | None'
entity_keys: []
relations_to: []
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

## Lifecycle

Lifecycle is described by [[CostState lifecycle]].

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::SessionRow | inferred
  > class SessionRow(BaseModel):
