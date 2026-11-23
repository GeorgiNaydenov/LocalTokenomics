---
archetype: entity
fields:
  - 'clients: list[ClientInfo]'
  - 'providers: list[str]'
  - 'models: list[str]'
  - 'projects: list[str]'
  - 'first_day: date | None'
  - 'last_day: date | None'
  - 'rates_as_of: str'
  - 'rates_age_days: int | None'
  - 'currency: str'
  - 'files_scanned: int'
  - 'events: int'
  - 'warnings: list[str]'
  - 'warning_summary: WarningSummary'
  - 'session_warnings: dict[str, list[str]]'
  - 'sources: list[SourceInfo]'
  - 'client_last_seen: dict[str, str]'
  - 'model_last_seen: dict[str, str]'
  - 'project_last_seen: dict[str, str]'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Meta

## Description

The entity Meta, declared in src/ai_usage_cost/api.py lines 105-128. It has 18 fields and 0 relations.

## Attributes

- clients: list[ClientInfo]
- providers: list[str]
- models: list[str]
- projects: list[str]
- first_day: date | None
- last_day: date | None
- rates_as_of: str
- rates_age_days: int | None
- currency: str
- files_scanned: int
- events: int
- warnings: list[str]
- warning_summary: WarningSummary
- session_warnings: dict[str, list[str]]
- sources: list[SourceInfo]
- client_last_seen: dict[str, str]
- model_last_seen: dict[str, str]
- project_last_seen: dict[str, str]

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

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/api.py::Meta | inferred
  > class Meta(BaseModel):
