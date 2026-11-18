---
code: BR-69
category: data integrity
subdomain: Usage collection
tags:
  - ba/rule
maturity: draft
---
# A request is stored once per fingerprint

## Statement

A later record with the same fingerprint replaces an earlier one only when it carries more output, because streamed records grow and the last one holds the billed count. `src/ai_usage_cost/store.py:359`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/store.py::_insert | inferred
  > the last (equivalently, largest) record carries the final, billed count
