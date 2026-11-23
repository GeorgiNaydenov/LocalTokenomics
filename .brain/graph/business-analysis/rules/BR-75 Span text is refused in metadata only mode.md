---
code: BR-75
category: privacy
subdomain: Privacy and retention
tags:
  - ba/rule
maturity: approved
---
# Span text is refused in metadata only mode

## Statement

While metadata only is on, or when a span has no content path, reading its text raises content unavailable and the API answers 404. `src/ai_usage_cost/privacy.py:87`

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/privacy.py::read_content | inferred
  > if config.metadata_only or span.content_path is None:
