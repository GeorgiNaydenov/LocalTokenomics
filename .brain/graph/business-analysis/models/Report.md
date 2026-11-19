---
archetype: entity
subdomain: Spend reporting
fields:
  - 'generated_at: datetime'
  - 'rates_as_of: str'
  - 'rates_age_days: int | None'
  - 'currency: str'
  - 'files_scanned: int'
  - 'files_in_slice: int'
  - 'totals: Totals'
  - 'by_client: list[Bucket]'
  - 'by_provider: list[Bucket]'
  - 'by_model: list[Bucket]'
  - 'by_project: list[Bucket]'
  - 'by_day: list[Bucket]'
  - 'series: list[SeriesPoint]'
  - 'sessions: list[SessionRow]'
  - 'unknown_models: list[UnknownModel]'
  - 'warnings: list[str]'
  - 'scan_warnings: list[str]'
  - 'warning_groups: list[WarningGroup]'
  - 'facets: Facets'
  - 'model_matches: dict[str, ModelMatch]'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Report

## Description

The entity Report, declared in src/ai_usage_cost/aggregate.py lines 462-482. It has 20 fields and 0 relations.

## Attributes

- generated_at: datetime
- rates_as_of: str
- rates_age_days: int | None
- currency: str
- files_scanned: int
- files_in_slice: int
- totals: Totals
- by_client: list[Bucket]
- by_provider: list[Bucket]
- by_model: list[Bucket]
- by_project: list[Bucket]
- by_day: list[Bucket]
- series: list[SeriesPoint]
- sessions: list[SessionRow]
- unknown_models: list[UnknownModel]
- warnings: list[str]
- scan_warnings: list[str]
- warning_groups: list[WarningGroup]
- facets: Facets
- model_matches: dict[str, ModelMatch]

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::Report | inferred
  > class Report(BaseModel):
