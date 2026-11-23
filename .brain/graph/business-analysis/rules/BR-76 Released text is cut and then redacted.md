---
code: BR-76
category: privacy
subdomain: Privacy and retention
tags:
  - ba/rule
maturity: approved
---
# Released text is cut and then redacted

## Statement

Text that is released is truncated to the configured byte limit and then has secrets replaced by a marker that names the kind. `src/ai_usage_cost/privacy.py:97`

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/privacy.py::read_content | inferred
  > text, truncated = truncate(text, config.max_content_bytes)
