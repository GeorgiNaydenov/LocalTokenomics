---
archetype: entity
fields:
  - 'path: TEXT (PK, required)'
  - 'source: TEXT (required)'
  - 'mtime: REAL (required)'
  - 'size: INTEGER (required)'
  - 'ingested_at: TEXT (required)'
  - 'warnings: TEXT (required)'
  - 'parser_version: INTEGER (required), default 0'
  - 'ingested_offset: INTEGER (required), default 0'
  - 'boundary_hash: TEXT'
  - 'title_seed: TEXT'
entity_keys:
  - path
relations_to: []
tags:
  - ba/model
maturity: approved
---
# files

## Description

The table files files, declared in src/ai_usage_cost/store.py lines 36-82. It has 10 fields and 0 relations.

## Attributes

- path: TEXT (PK, required)
- source: TEXT (required)
- mtime: REAL (required)
- size: INTEGER (required)
- ingested_at: TEXT (required)
- warnings: TEXT (required)
- parser_version: INTEGER (required), default 0
- ingested_offset: INTEGER (required), default 0
- boundary_hash: TEXT
- title_seed: TEXT

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

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/store.py::files | inferred
  > CREATE TABLE files (
