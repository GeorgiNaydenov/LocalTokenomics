---
archetype: value object
subdomain: Cost pricing
tags:
  - ba/model
maturity: draft
---
# TokenUsage

## Description

The token counts of one request, split into uncached input, cache read, two cache write buckets, output and reasoning output. `src/ai_usage_cost/models.py:12`

## Attributes

- uncached_input, cache_read, cache_write_5m, cache_write_1h, output, reasoning_output: whole numbers, default 0
- cache_write, input_total, total: derived, never stored

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::TokenUsage | inferred
  > class TokenUsage(BaseModel):
