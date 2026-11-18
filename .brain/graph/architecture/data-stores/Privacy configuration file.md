---
persists_models:
  - Config
tags:
  - arch/data-store
maturity: draft
---
# Privacy configuration file

## Description

An optional config.json in the store folder. When it is missing or invalid the defaults apply: `src/ai_usage_cost/privacy.py:12`.

## Sources

- [[Code of localtokenomics]] @ declared-in -> src/ai_usage_cost/privacy.py::DEFAULT_CONFIG_PATH | inferred
  > DEFAULT_CONFIG_PATH = Path.home()
