---
archetype: entity
fields:
  - 'events: list[PricedEvent]'
  - 'table: RateTable'
  - 'files: int'
  - 'warnings: list[str]'
  - 'scan_warnings: list[str]'
  - 'sources: list[SourceInfo]'
  - 'session_flags: dict[tuple[str, str], tuple[bool, int, str]]'
  - 'db_path: Path | None'
  - 'today: date | None'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Analysis

## Description

The entity Analysis, declared in src/ai_usage_cost/pipeline.py lines 45-63. It has 9 fields and 0 relations.

## Attributes

- events: list[PricedEvent]
- table: RateTable
- files: int
- warnings: list[str]
- scan_warnings: list[str]
- sources: list[SourceInfo]
- session_flags: dict[tuple[str, str], tuple[bool, int, str]]
- db_path: Path | None
- today: date | None

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/pipeline.py::Analysis | inferred
  > class Analysis:
