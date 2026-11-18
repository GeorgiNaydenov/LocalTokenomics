---
code: BR-83
category: privacy
subdomain: Privacy and retention
tags:
  - ba/rule
maturity: draft
---
# Content retention is inert

## Statement

Setting content retention days only adds a warning, because no content is stored. `src/ai_usage_cost/pipeline.py:242`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pipeline.py::analyze | inferred
  > content_retention_days is set but inert
