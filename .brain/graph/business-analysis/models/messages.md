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

## Used by

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-15 Print a usage and cost summary in the terminal]]
- [[UC-16 Export a usage and cost chart as a PNG image]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-19 Export a report as a file]]
- [[UC-20 Be alerted when spend rises]]
- [[UC-24 Try the tool with demo data]]
- [[UC-25 Sample GPU use for local models]]
- [[UC-26 Query the store with SQL]]
- [[UC-27 Browse sessions in the terminal]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/demo.py::messages | inferred
  > CREATE TABLE messages (
