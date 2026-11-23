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

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/collect.py::samples | inferred
  > CREATE TABLE IF NOT EXISTS samples (
