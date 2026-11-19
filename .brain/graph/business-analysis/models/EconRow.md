---
archetype: entity
fields:
  - 'key: str'
  - 'label: str | None'
  - 'ordinal: int | None'
  - 'started_at: datetime | None'
  - 'is_sidechain: bool'
  - 'model_calls: int'
  - 'tool_calls: int'
  - 'tokens: TokenUsage | None'
  - 'tokens_provenance: Provenance'
  - 'cost: CostBreakdown | None'
  - 'cost_state: CostState'
  - 'duration_ms: int | None'
  - 'duration_provenance: Provenance'
  - 'errors: int'
  - 'retries: int | None'
  - 'amplification: float | None'
  - 'cache_hit_ratio: float | None'
  - 'tokens_per_second: float | None'
  - 'model_config: ConfigDict'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# EconRow

## Description

The entity EconRow, declared in src/ai_usage_cost/trace.py lines 154-174. It has 19 fields and 0 relations.

## Attributes

- key: str
- label: str | None
- ordinal: int | None
- started_at: datetime | None
- is_sidechain: bool
- model_calls: int
- tool_calls: int
- tokens: TokenUsage | None
- tokens_provenance: Provenance
- cost: CostBreakdown | None
- cost_state: CostState
- duration_ms: int | None
- duration_provenance: Provenance
- errors: int
- retries: int | None
- amplification: float | None
- cache_hit_ratio: float | None
- tokens_per_second: float | None
- model_config: ConfigDict

## Lifecycle

Lifecycle is described by [[CostState lifecycle]].

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::EconRow | inferred
  > class EconRow(BaseModel):
