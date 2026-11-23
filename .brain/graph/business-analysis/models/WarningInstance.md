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

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::WarningInstance | inferred
  > class WarningInstance(BaseModel):
