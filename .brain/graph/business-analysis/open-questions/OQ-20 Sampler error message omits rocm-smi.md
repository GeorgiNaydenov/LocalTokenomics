---
code: OQ-20
priority: low
status: open
linked:
  - Sample GPU use for local models
tags:
  - ba/open-question
maturity: draft
---
# Sampler error message omits rocm-smi

## Question

The sampler supports rocm-smi `src/ai_usage_cost/collect.py:88` but the error names only nvidia-smi and PowerShell `src/ai_usage_cost/cli.py:214`. Is the message stale?

## Raised by

Reading cli.py and collect.py
