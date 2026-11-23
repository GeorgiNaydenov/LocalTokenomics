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

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/privacy.py::load_config | inferred
  > except (OSError, ValueError):
