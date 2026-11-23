---
code: BR-125
category: behaviour
tags:
  - ba/rule
maturity: draft
---
# Span text is fetched once per span

## Statement

The text of a trace span is requested the first time the reader opens it and the stored result, content or error, is reused afterwards. `web/src/TraceTab.tsx:791`

## Enforced in

- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-10 Narrow a list and choose its columns]]
- [[UC-12 Review a session's spans and context use]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/TraceTab.tsx::toggleContent | confirmed
  >     if (alreadyOpen || contents[span.span_id]) return
