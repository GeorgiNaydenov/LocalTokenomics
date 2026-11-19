---
archetype: entity
fields:
  - 'span_id: TEXT (PK, required)'
  - 'parent_id: TEXT'
  - 'record_parent: TEXT'
  - 'source: TEXT (required)'
  - 'session_id: TEXT (required)'
  - 'turn_id: TEXT'
  - 'agent_id: TEXT'
  - 'is_sidechain: INTEGER (required)'
  - 'seq: INTEGER (required)'
  - 'kind: TEXT (required)'
  - 'name: TEXT'
  - 'model: TEXT'
  - 'status: TEXT (required)'
  - 'started_at: TEXT (required)'
  - 'ended_at: TEXT'
  - 'duration_ms: INTEGER'
  - 'duration_provenance: TEXT (required)'
  - 'ttft_ms: INTEGER'
  - 'uncached_input: INTEGER'
  - 'cache_read: INTEGER'
  - 'cache_write_5m: INTEGER'
  - 'cache_write_1h: INTEGER'
  - 'output: INTEGER'
  - 'reasoning_output: INTEGER'
  - 'tokens_provenance: TEXT (required)'
  - 'context_capacity: INTEGER'
  - 'capacity_provenance: TEXT (required)'
  - 'retry_attempt: INTEGER'
  - 'error: TEXT'
  - 'source_file: TEXT (required)'
  - 'record_offset: INTEGER (required)'
  - 'record_length: INTEGER (required)'
  - 'content_path: TEXT'
  - 'detail: TEXT (required)'
entity_keys:
  - span_id
relations_to: []
tags:
  - ba/model
maturity: approved
---
# trace_events

## Description

The table trace_events trace_events, declared in src/ai_usage_cost/store.py lines 43-60. It has 34 fields and 0 relations.

## Attributes

- span_id: TEXT (PK, required)
- parent_id: TEXT
- record_parent: TEXT
- source: TEXT (required)
- session_id: TEXT (required)
- turn_id: TEXT
- agent_id: TEXT
- is_sidechain: INTEGER (required)
- seq: INTEGER (required)
- kind: TEXT (required)
- name: TEXT
- model: TEXT
- status: TEXT (required)
- started_at: TEXT (required)
- ended_at: TEXT
- duration_ms: INTEGER
- duration_provenance: TEXT (required)
- ttft_ms: INTEGER
- uncached_input: INTEGER
- cache_read: INTEGER
- cache_write_5m: INTEGER
- cache_write_1h: INTEGER
- output: INTEGER
- reasoning_output: INTEGER
- tokens_provenance: TEXT (required)
- context_capacity: INTEGER
- capacity_provenance: TEXT (required)
- retry_attempt: INTEGER
- error: TEXT
- source_file: TEXT (required)
- record_offset: INTEGER (required)
- record_length: INTEGER (required)
- content_path: TEXT
- detail: TEXT (required)

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/store.py::trace_events | inferred
  > CREATE TABLE trace_events (
