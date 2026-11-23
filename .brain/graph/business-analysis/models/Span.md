---
archetype: entity
subdomain: Usage collection
fields:
  - 'model_config: ConfigDict'
  - 'span_id: str'
  - 'parent_id: str | None'
  - 'record_parent: str | None'
  - 'source: str'
  - 'session_id: str'
  - 'turn_id: str | None'
  - 'agent_id: str | None'
  - 'is_sidechain: bool'
  - 'seq: int'
  - 'kind: SpanKind'
  - 'name: str | None'
  - 'model: str | None'
  - 'status: SpanStatus'
  - 'started_at: datetime'
  - 'ended_at: datetime | None'
  - 'duration_ms: int | None'
  - 'duration_provenance: Provenance'
  - 'ttft_ms: int | None'
  - 'tokens: TokenUsage | None'
  - 'tokens_provenance: Provenance'
  - 'context_capacity: int | None'
  - 'capacity_provenance: Provenance'
  - 'retry_attempt: int | None'
  - 'error: str | None'
  - 'source_file: str'
  - 'record_offset: int'
  - 'record_length: int'
  - 'content_path: str | None'
  - 'detail: dict[str, RawScalar]'
entity_keys: []
relations_to: []
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

## Lifecycle

Lifecycle is described by [[SpanKind lifecycle]]. Lifecycle is described by [[SpanStatus lifecycle]].

## Used by

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-14 Read a tool's SQLite store without a token count]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::Span | inferred
  > class Span(BaseModel):
