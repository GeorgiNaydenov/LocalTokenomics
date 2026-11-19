---
archetype: entity
fields:
  - 'files_parsed: int'
  - 'files_skipped: int'
  - 'warnings: list[str]'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# IngestSummary

## Description

The entity IngestSummary, declared in src/ai_usage_cost/store.py lines 134-137. It has 3 fields and 0 relations.

## Attributes

- files_parsed: int
- files_skipped: int
- warnings: list[str]

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/store.py::IngestSummary | inferred
  > class IngestSummary:
