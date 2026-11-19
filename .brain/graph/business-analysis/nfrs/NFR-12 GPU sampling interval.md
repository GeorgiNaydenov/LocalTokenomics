---
code: NFR-12
category: performance
target: One reading every 2 seconds by default, until stopped or a duration ends
applies_to:
  - Usage collection
tags:
  - ba/nfr
maturity: draft
---
# GPU sampling interval

## Statement

The collect command samples at a default interval of two seconds and sleeps between readings. `src/ai_usage_cost/cli.py:201` `src/ai_usage_cost/collect.py:277`
