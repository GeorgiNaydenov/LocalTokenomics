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

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::Report | inferred
  > class Report(BaseModel):
