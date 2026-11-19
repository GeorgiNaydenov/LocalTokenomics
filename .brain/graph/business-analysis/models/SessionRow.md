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
maturity: approved
---
# SessionRow

## Description

The entity SessionRow, declared in src/ai_usage_cost/aggregate.py lines 48-74. It has 26 fields and 0 relations.

## Attributes

- session_id: str
- source: str
- client: str
- provider: str
- models: list[str]
- start_time: datetime
- end_time: datetime
- request_count: int
- tokens: TokenUsage | None
- cost: CostBreakdown | None
- reported_cost: float | None
- cost_state: CostState
- cost_states: list[CostState]
- is_sidechain: bool
- has_sidechain: bool
- currency: str
- project: str | None
- working_directory: str | None
- repository: str | None
- branch: str | None
- machine: str
- raw_source: list[str]
- outcome: OutcomeLabel
- traced: bool
- error_count: int
- title: str | None

## Lifecycle

Lifecycle is described by [[CostState lifecycle]].

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::SessionRow | inferred
  > class SessionRow(BaseModel):
