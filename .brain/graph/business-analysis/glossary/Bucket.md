---
in_application: 'One row of a breakdown: a key, a label, a cost, token counts and a request count (`Bucket` at `src/ai_usage_cost/models.py:123`). The code declares it at `src/ai_usage_cost/models.py:123`, where the line reads `class Bucket(BaseModel):`.'
tags:
  - ba/glossary-term
maturity: draft
---
# Bucket

## Definition

One row of a breakdown: a key, a label, a cost, token counts and a request count. The terminal tables and the model and project charts are drawn from lists of buckets.

## Sources

- [[Code of localtokenomics]] @ declared-in -> src/ai_usage_cost/models.py::Bucket | inferred
  > class Bucket(BaseModel):
