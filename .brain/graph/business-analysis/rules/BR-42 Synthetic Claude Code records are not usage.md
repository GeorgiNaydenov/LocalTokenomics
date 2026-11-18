---
code: BR-42
tags:
  - ba/rule
maturity: approved
---
# Synthetic Claude Code records are not usage

## Statement

A Claude Code assistant record with no model or a synthetic model is skipped.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/sources/claude_code.py | inferred
  > if not model or model in SYNTHETIC_MODELS:
