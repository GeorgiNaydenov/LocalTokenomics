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

## Used by

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

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/cli.py::AlertDecision | inferred
  > class AlertDecision:
