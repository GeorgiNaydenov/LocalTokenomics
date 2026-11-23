---
archetype: entity
fields:
  - 'source: TEXT (PK, required)'
  - 'session_id: TEXT (PK, required)'
  - 'outcome: TEXT (required)'
  - 'notes: TEXT (required)'
  - 'tags: TEXT (required)'
  - 'updated_at: TEXT (required)'
entity_keys:
  - source
  - session_id
relations_to: []
tags:
  - ba/model
maturity: approved
---
# outcomes

## Description

The table outcomes outcomes, declared in src/ai_usage_cost/store.py lines 63-68. It has 6 fields and 0 relations.

## Attributes

- source: TEXT (PK, required)
- session_id: TEXT (PK, required)
- outcome: TEXT (required)
- notes: TEXT (required)
- tags: TEXT (required)
- updated_at: TEXT (required)

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

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/store.py::outcomes | inferred
  > CREATE TABLE outcomes (
