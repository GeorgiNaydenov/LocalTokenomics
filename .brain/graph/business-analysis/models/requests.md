---
archetype: entity
fields:
  - 'fingerprint: TEXT (PK, required)'
  - 'source: TEXT (required)'
  - 'client: TEXT (required)'
  - 'provider: TEXT'
  - 'model: TEXT'
  - 'session_id: TEXT (required)'
  - 'timestamp: TEXT (required)'
  - 'request_id: TEXT'
  - 'uncached_input: INTEGER'
  - 'cache_read: INTEGER'
  - 'cache_write_5m: INTEGER'
  - 'cache_write_1h: INTEGER'
  - 'output: INTEGER'
  - 'reasoning_output: INTEGER'
  - 'is_sidechain: INTEGER (required)'
  - 'tier: TEXT (required)'
  - 'project: TEXT'
  - 'working_directory: TEXT'
  - 'repository: TEXT'
  - 'branch: TEXT'
  - 'machine: TEXT (required)'
  - 'source_file: TEXT (required)'
  - 'raw: TEXT (required)'
  - 'title: TEXT'
  - 'title_source: TEXT (required), default ''folder'''
  - 'reported_cost: REAL'
entity_keys:
  - fingerprint
relations_to: []
tags:
  - ba/model
maturity: approved
---
# requests

## Description

The table requests requests, declared in src/ai_usage_cost/store.py lines 23-85. It has 26 fields and 0 relations.

## Attributes

- fingerprint: TEXT (PK, required)
- source: TEXT (required)
- client: TEXT (required)
- provider: TEXT
- model: TEXT
- session_id: TEXT (required)
- timestamp: TEXT (required)
- request_id: TEXT
- uncached_input: INTEGER
- cache_read: INTEGER
- cache_write_5m: INTEGER
- cache_write_1h: INTEGER
- output: INTEGER
- reasoning_output: INTEGER
- is_sidechain: INTEGER (required)
- tier: TEXT (required)
- project: TEXT
- working_directory: TEXT
- repository: TEXT
- branch: TEXT
- machine: TEXT (required)
- source_file: TEXT (required)
- raw: TEXT (required)
- title: TEXT
- title_source: TEXT (required), default 'folder'
- reported_cost: REAL

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

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/store.py::requests | inferred
  > CREATE TABLE requests (
