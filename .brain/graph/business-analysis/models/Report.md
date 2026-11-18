---
archetype: aggregate root
subdomain: Spend reporting
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

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::Report | inferred
  > class Report(BaseModel):
