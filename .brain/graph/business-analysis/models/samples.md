---
archetype: entity
fields:
  - 'machine: TEXT (required)'
  - 'sampled_at: TEXT (required)'
  - 'gpu_util: REAL'
  - 'vram_used: INTEGER'
  - 'vram_total: INTEGER'
  - 'power_w: REAL'
  - 'source: TEXT (required)'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# samples

## Description

The table samples samples, declared in src/ai_usage_cost/collect.py lines 19-23. It has 7 fields and 0 relations.

## Attributes

- machine: TEXT (required)
- sampled_at: TEXT (required)
- gpu_util: REAL
- vram_used: INTEGER
- vram_total: INTEGER
- power_w: REAL
- source: TEXT (required)

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/collect.py::samples | inferred
  > CREATE TABLE IF NOT EXISTS samples (
