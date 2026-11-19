---
code: BR-124
category: behaviour
tags:
  - ba/rule
maturity: draft
---
# A workspace tab loads its data only when first opened

## Statement

The Trace, Economics and Context tabs of a session fetch from the server only after the reader has selected them once; the Summary tab needs no request. `web/src/SessionWorkspace.tsx:472`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/SessionWorkspace.tsx::useLazyResource | confirmed
  >     if (!enabled) return
