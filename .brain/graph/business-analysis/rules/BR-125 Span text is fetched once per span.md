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

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/TraceTab.tsx::toggleContent | confirmed
  >     if (alreadyOpen || contents[span.span_id]) return
