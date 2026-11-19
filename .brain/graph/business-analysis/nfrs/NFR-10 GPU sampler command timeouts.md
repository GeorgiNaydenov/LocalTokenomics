---
code: NFR-10
category: reliability
target: 10 seconds for nvidia-smi and rocm-smi, 30 seconds for PowerShell counters, 0.5 seconds for Ollama
applies_to:
  - Usage collection
tags:
  - ba/nfr
maturity: approved
---
# GPU sampler command timeouts

## Statement

Each external sampler call has a timeout: `src/ai_usage_cost/collect.py:214`, `src/ai_usage_cost/collect.py:183` and `src/ai_usage_cost/collect.py:197`.
