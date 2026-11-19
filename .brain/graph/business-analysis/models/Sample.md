---
archetype: entity
fields:
  - 'machine: str'
  - 'sampled_at: datetime'
  - 'gpu_util: float | None'
  - 'vram_used: int | None'
  - 'vram_total: int | None'
  - 'power_w: float | None'
  - 'source: str'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Sample

## Description

The entity Sample, declared in src/ai_usage_cost/collect.py lines 49-56. It has 7 fields and 0 relations.

## Attributes

- machine: str
- sampled_at: datetime
- gpu_util: float | None
- vram_used: int | None
- vram_total: int | None
- power_w: float | None
- source: str

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/collect.py::Sample | inferred
  > class Sample(BaseModel):
