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
maturity: approved
---
# UsageEvent

## Description

The entity UsageEvent, declared in src/ai_usage_cost/models.py lines 49-72. It has 21 fields and 0 relations.

## Attributes

- source: str
- client: str
- provider: str | None
- model: str | None
- timestamp: datetime
- session_id: str
- request_id: str | None
- tokens: TokenUsage | None
- is_sidechain: bool
- tier: str
- project: str | None
- working_directory: str | None
- repository: str | None
- branch: str | None
- title: str | None
- title_source: Literal['tool', 'summary', 'prompt', 'folder']
- machine: str
- source_file: str
- record_offset: int | None
- raw: dict[str, RawScalar]
- reported_cost: float | None

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::UsageEvent | inferred
  > class UsageEvent(BaseModel):
