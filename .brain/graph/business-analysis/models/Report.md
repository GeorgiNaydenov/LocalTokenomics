---
archetype: aggregate root
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
maturity: draft
---
# Report

## Description

The answer to one query: totals, buckets by client, provider, model, project and day, session rows, warnings and facets. `src/ai_usage_cost/aggregate.py:462`

## Attributes

- totals, by_client, by_provider, by_model, by_project, by_day, series, sessions
- unknown_models, warnings, scan_warnings, warning_groups, facets, model_matches
- rates_as_of, rates_age_days, currency, files_scanned, files_in_slice

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::Report | inferred
  > class Report(BaseModel):
