---
code: BR-77
category: privacy
subdomain: Privacy and retention
tags:
  - ba/rule
maturity: approved
---
# A bad configuration file gives the defaults

## Statement

A missing, unreadable or invalid config.json is replaced by the defaults, which keep metadata only on. `src/ai_usage_cost/privacy.py:63`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/privacy.py::load_config | inferred
  > except (OSError, ValueError):
