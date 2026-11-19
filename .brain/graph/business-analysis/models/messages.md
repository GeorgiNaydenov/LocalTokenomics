---
archetype: entity
fields:
  - 'id: INTEGER (PK, required)'
  - 'chat_id: INTEGER'
  - 'role: TEXT'
  - 'content: TEXT'
  - 'created_at: INTEGER'
  - 'approval_state: TEXT'
  - 'commit_hash: TEXT'
entity_keys:
  - id
relations_to: []
tags:
  - ba/model
maturity: approved
---
# messages

## Description

The table messages messages, declared in src/ai_usage_cost/demo.py lines 79-87. It has 7 fields and 0 relations.

## Attributes

- id: INTEGER (PK, required)
- chat_id: INTEGER
- role: TEXT
- content: TEXT
- created_at: INTEGER
- approval_state: TEXT
- commit_hash: TEXT

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/demo.py::messages | inferred
  > CREATE TABLE messages (
