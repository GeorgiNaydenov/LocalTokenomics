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

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/api.py::Meta | inferred
  > class Meta(BaseModel):
