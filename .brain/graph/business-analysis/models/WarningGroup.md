---
archetype: entity
fields:
  - 'kind: str'
  - 'label: str'
  - 'count: int'
  - 'summary: str'
  - 'severity: WarningSeverity'
  - 'total_delta_tokens: int'
  - 'total_delta_cost: float'
  - 'worst_example: WarningInstance | None'
  - 'affected_sessions: int'
  - 'instances: list[WarningInstance]'
  - 'warnings: list[str]'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# WarningGroup

## Description

The entity WarningGroup, declared in src/ai_usage_cost/aggregate.py lines 115-127. It has 11 fields and 0 relations.

## Attributes

- kind: str
- label: str
- count: int
- summary: str
- severity: WarningSeverity
- total_delta_tokens: int
- total_delta_cost: float
- worst_example: WarningInstance | None
- affected_sessions: int
- instances: list[WarningInstance]
- warnings: list[str]

## Lifecycle

No lifecycle field was found in the code.

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

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::WarningGroup | inferred
  > class WarningGroup(BaseModel):
