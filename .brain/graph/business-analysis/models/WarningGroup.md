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

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::WarningGroup | inferred
  > class WarningGroup(BaseModel):
