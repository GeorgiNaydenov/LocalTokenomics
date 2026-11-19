---
archetype: entity
fields:
  - 'day: date'
  - 'client: str'
  - 'provider: str'
  - 'model: str'
  - 'source: str'
  - 'cost: float'
  - 'tokens: int'
  - 'events: int'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# SeriesPoint

## Description

The entity SeriesPoint, declared in src/ai_usage_cost/aggregate.py lines 37-45. It has 8 fields and 0 relations.

## Attributes

- day: date
- client: str
- provider: str
- model: str
- source: str
- cost: float
- tokens: int
- events: int

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/aggregate.py::SeriesPoint | inferred
  > class SeriesPoint(BaseModel):
