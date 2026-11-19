---
archetype: entity
fields:
  - 'span_id: str'
  - 'model: str | None'
  - 'started_at: datetime'
  - 'input_total: int | None'
  - 'tokens_provenance: Provenance'
  - 'capacity: int | None'
  - 'capacity_provenance: Provenance'
  - 'occupancy: float | None'
  - 'occupancy_provenance: Provenance'
  - 'delta_input: int | None'
  - 'added_span_ids: list[str]'
  - 'compacted_before: bool'
  - 'composition: dict[str, float]'
  - 'model_config: ConfigDict'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# ContextSnapshot

## Description

The entity ContextSnapshot, declared in src/ai_usage_cost/trace.py lines 112-131. It has 14 fields and 0 relations.

## Attributes

- span_id: str
- model: str | None
- started_at: datetime
- input_total: int | None
- tokens_provenance: Provenance
- capacity: int | None
- capacity_provenance: Provenance
- occupancy: float | None
- occupancy_provenance: Provenance
- delta_input: int | None
- added_span_ids: list[str]
- compacted_before: bool
- composition: dict[str, float]
- model_config: ConfigDict

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::ContextSnapshot | inferred
  > class ContextSnapshot(BaseModel):
