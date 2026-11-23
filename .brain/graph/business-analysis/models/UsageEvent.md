---
archetype: entity
subdomain: Usage collection
fields:
  - 'source: str'
  - 'client: str'
  - 'provider: str | None'
  - 'model: str | None'
  - 'timestamp: datetime'
  - 'session_id: str'
  - 'request_id: str | None'
  - 'tokens: TokenUsage | None'
  - 'is_sidechain: bool'
  - 'tier: str'
  - 'project: str | None'
  - 'working_directory: str | None'
  - 'repository: str | None'
  - 'branch: str | None'
  - 'title: str | None'
  - 'title_source: Literal[''tool'', ''summary'', ''prompt'', ''folder'']'
  - 'machine: str'
  - 'source_file: str'
  - 'record_offset: int | None'
  - 'raw: dict[str, RawScalar]'
  - 'reported_cost: float | None'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: draft
---
# UsageEvent

## Description

One request read from a log: who made it, when, with which model and how many tokens, plus project and title context. `src/ai_usage_cost/models.py:49`

## Attributes

- source, client, session_id, timestamp: required
- provider, model, request_id, tokens: optional; tokens is None when the log has no counts
- tier: service tier, default standard
- reported_cost: the cost the tool itself logged, kept beside the computed one

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
- [[UC-24 Try the tool with demo data]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::UsageEvent | inferred
  > class UsageEvent(BaseModel):
