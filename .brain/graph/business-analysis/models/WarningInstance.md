---
archetype: entity
fields:
  - 'kind: str'
  - 'message: str'
  - 'source: str'
  - 'file: str | None'
  - 'session_id: str | None'
  - 'severity: WarningSeverity'
  - 'delta_tokens: int | None'
  - 'delta_cost: float | None'
  - 'likely_cause: str | None'
  - 'auto_corrected: bool'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# WarningInstance

## Description

The entity WarningInstance, declared in src/ai_usage_cost/aggregate.py lines 100-111. It has 10 fields and 0 relations.

## Attributes

- kind: str
- message: str
- source: str
- file: str | None
- session_id: str | None
- severity: WarningSeverity
- delta_tokens: int | None
- delta_cost: float | None
- likely_cause: str | None
- auto_corrected: bool

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::WarningInstance | inferred
  > class WarningInstance(BaseModel):
