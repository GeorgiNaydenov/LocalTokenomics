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

## Enforced in

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-15 Print a usage and cost summary in the terminal]]
- [[UC-16 Export a usage and cost chart as a PNG image]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-19 Export a report as a file]]
- [[UC-20 Be alerted when spend rises]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]
- [[UC-24 Try the tool with demo data]]
- [[UC-25 Sample GPU use for local models]]
- [[UC-26 Query the store with SQL]]
- [[UC-27 Browse sessions in the terminal]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/api.py::create_app.span_content | inferred
  > raise HTTPException(404, f"no readable content for span {span_id!r}") from exc
