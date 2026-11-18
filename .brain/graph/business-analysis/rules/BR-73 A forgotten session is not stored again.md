---
code: BR-73
category: privacy
subdomain: Privacy and retention
tags:
  - ba/rule
maturity: draft
---
# A forgotten session is not stored again

## Statement

After a person forgets a session its spans and rating are deleted and an exclusion row keeps its spans out of later scans. Its requests stay. `src/ai_usage_cost/store.py:273`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/store.py::ingest | inferred
  > if (span.source, span.session_id) in excluded_sessions:
