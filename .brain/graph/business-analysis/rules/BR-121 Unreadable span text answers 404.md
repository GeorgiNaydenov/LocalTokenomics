---
code: BR-121
category: interface
subdomain: Privacy and retention
tags:
  - ba/rule
maturity: draft
---
# Unreadable span text answers 404

## Statement

The content route answers 404 when the span is not in the session, and also when its text is not released or cannot be read. `src/ai_usage_cost/api.py:382`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/api.py::create_app.span_content | inferred
  > raise HTTPException(404, f"no readable content for span {span_id!r}") from exc
