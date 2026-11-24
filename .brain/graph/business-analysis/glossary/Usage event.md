---
tags:
  - ba/glossary-term
maturity: draft
---
# Usage event

## Definition

The record a reader yields for one request or one conversation turn: model, timestamp, session id, request id, project, title and, when the reader can see them, token counts.

## Sources

- [[Code of localtokenomics]] @ src/ai_usage_cost/models.py:49 | inferred
  > class UsageEvent(BaseModel):
