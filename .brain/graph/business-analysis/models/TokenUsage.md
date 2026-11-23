---
archetype: value object
subdomain: Cost pricing
fields:
  - 'uncached_input: int'
  - 'cache_read: int'
  - 'cache_write_5m: int'
  - 'cache_write_1h: int'
  - 'output: int'
  - 'reasoning_output: int'
entity_keys: []
relations_to: []
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

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::TokenUsage | inferred
  > class TokenUsage(BaseModel):
