---
type: supporting
tags:
  - ba/subdomain
maturity: approved
---
# Privacy and retention

## Description

Decides whether span text may be shown, cuts and redacts it, and applies project exclusion and trace retention. Main code: `src/ai_usage_cost/privacy.py:86` and `src/ai_usage_cost/privacy.py:52`.

## Sources

- [[Code of localtokenomics]] @ bounded-by -> src/ai_usage_cost/privacy.py::read_content | inferred
  > def read_content(
