---
archetype: entity
fields:
  - 'source: TEXT (PK, required)'
  - 'session_id: TEXT (PK, required)'
  - 'excluded_at: TEXT (required)'
entity_keys:
  - source
  - session_id
relations_to: []
tags:
  - ba/model
maturity: approved
---
# session_exclusions

## Description

The table session_exclusions session_exclusions, declared in src/ai_usage_cost/store.py lines 69-72. It has 3 fields and 0 relations.

## Attributes

- source: TEXT (PK, required)
- session_id: TEXT (PK, required)
- excluded_at: TEXT (required)

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/store.py::session_exclusions | inferred
  > CREATE TABLE session_exclusions (
