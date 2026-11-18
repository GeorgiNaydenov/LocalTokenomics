---
code: BR-75
category: privacy
subdomain: Privacy and retention
tags:
  - ba/rule
maturity: draft
---
# Span text is refused in metadata only mode

## Statement

While metadata only is on, or when a span has no content path, reading its text raises content unavailable and the API answers 404. `src/ai_usage_cost/privacy.py:87`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/privacy.py::read_content | inferred
  > if config.metadata_only or span.content_path is None:
