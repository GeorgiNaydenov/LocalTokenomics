---
archetype: entity
fields:
  - 'id: INTEGER (PK, required)'
  - 'app_id: INTEGER'
  - 'title: TEXT'
  - 'created_at: INTEGER'
  - 'initial_commit_hash: TEXT'
entity_keys:
  - id
relations_to: []
tags:
  - ba/model
maturity: approved
---
# chats

## Description

The table chats chats, declared in src/ai_usage_cost/demo.py lines 71-77. It has 5 fields and 0 relations.

## Attributes

- id: INTEGER (PK, required)
- app_id: INTEGER
- title: TEXT
- created_at: INTEGER
- initial_commit_hash: TEXT

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/demo.py::chats | inferred
  > CREATE TABLE chats (
