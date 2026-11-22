---
archetype: entity
fields:
  - 'fire: bool'
  - 'message: str'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# AlertDecision

## Description

The entity AlertDecision, declared in src/ai_usage_cost/cli.py lines 252-254. It has 2 fields and 0 relations.

## Attributes

- fire: bool
- message: str

## Lifecycle

None. It is a frozen dataclass built once by the alert check at src/ai_usage_cost/cli.py line 282 and never changed: fire is true when the amount passes the threshold, and message holds the report lines.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/cli.py::AlertDecision | inferred
  > class AlertDecision:
