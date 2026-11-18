---
archetype: entity
subdomain: Usage collection
tags:
  - ba/model
maturity: draft
---
# Span

## Description

One step of a session trace: a turn, a message, a model call, a tool call or an error, with timing, tokens and where its record sits in the log. `src/ai_usage_cost/trace.py:55`

## Attributes

- span_id, parent_id, session_id, turn_id, agent_id, kind, status
- started_at, ended_at, duration_ms, tokens, context_capacity, each with a provenance
- source_file, record_offset, record_length, content_path

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::Span | inferred
  > class Span(BaseModel):
