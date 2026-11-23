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

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/privacy.py::read_content | inferred
  > if config.metadata_only or span.content_path is None:
