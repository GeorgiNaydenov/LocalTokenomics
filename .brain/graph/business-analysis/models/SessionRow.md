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

## Used by

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-15 Print a usage and cost summary in the terminal]]
- [[UC-16 Export a usage and cost chart as a PNG image]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-19 Export a report as a file]]
- [[UC-20 Be alerted when spend rises]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]
- [[UC-24 Try the tool with demo data]]
- [[UC-25 Sample GPU use for local models]]
- [[UC-26 Query the store with SQL]]
- [[UC-27 Browse sessions in the terminal]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::SessionRow | inferred
  > class SessionRow(BaseModel):
