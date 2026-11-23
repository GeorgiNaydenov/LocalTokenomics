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

## Used by

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-15 Print a usage and cost summary in the terminal]]
- [[UC-16 Export a usage and cost chart as a PNG image]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-19 Export a report as a file]]
- [[UC-20 Be alerted when spend rises]]
- [[UC-22 Forget a session]]
- [[UC-24 Try the tool with demo data]]
- [[UC-25 Sample GPU use for local models]]
- [[UC-26 Query the store with SQL]]
- [[UC-27 Browse sessions in the terminal]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/collect.py::Sample | inferred
  > class Sample(BaseModel):
