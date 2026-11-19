---
code: BR-110
category: guard
tags:
  - ba/rule
maturity: approved
---
# read_content refuses when config.metadata_only or span.content_path is None

## Statement

In read_content, when config.metadata_only or span.content_path is None: the code raises ContentUnavailable. Located at src/ai_usage_cost/privacy.py lines 87-88.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/privacy.py::read_content | inferred
  > if config.metadata_only or span.content_path is None:
