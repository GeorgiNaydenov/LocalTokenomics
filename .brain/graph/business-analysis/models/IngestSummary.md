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

## Used by

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]
- [[UC-25 Sample GPU use for local models]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/store.py::IngestSummary | inferred
  > class IngestSummary:
