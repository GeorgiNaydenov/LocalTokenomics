---
archetype: value object
subdomain: Cost pricing
fields:
  - 'uncached_input: float'
  - 'cache_read: float'
  - 'cache_write: float'
  - 'output: float'
  - 'no_cache_equivalent: float'
  - 'estimated: bool'
  - 'tier_unpriced: bool'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: draft
---
# CostBreakdown

## Description

The computed cost of a request or of a group of requests, split into uncached input, cache read, cache write and output, with the no cache baseline. `src/ai_usage_cost/models.py:75`

## Attributes

- uncached_input, cache_read, cache_write, output, no_cache_equivalent: dollars
- estimated: true when any part was priced from a shorter id prefix
- total, cache_savings: derived

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::CostBreakdown | inferred
  > class CostBreakdown(BaseModel):
