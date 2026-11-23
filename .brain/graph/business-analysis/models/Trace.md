---
archetype: entity
fields:
  - 'source: str'
  - 'session_id: str'
  - 'capabilities: Capabilities'
  - 'spans: list[Span]'
  - 'outcome: Outcome | None'
  - 'insights: list[Insight]'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Trace

## Description

The entity Trace, declared in src/ai_usage_cost/trace.py lines 192-198. It has 6 fields and 0 relations.

## Attributes

- source: str
- session_id: str
- capabilities: Capabilities
- spans: list[Span]
- outcome: Outcome | None
- insights: list[Insight]

## Lifecycle

No lifecycle field was found in the code.

## Used by

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-14 Read a tool's SQLite store without a token count]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::Trace | inferred
  > class Trace(BaseModel):
