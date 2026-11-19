---
code: RSK-48
impact: low
likelihood: low
tags:
  - ba/risk
maturity: draft
---
# Risk 8: A missing span text is recognised by message wording

## Risk

The trace tab treats an error as not found when its message contains 404, which depends on the wording of the API helper rather than on a status field. `web/src/TraceTab.tsx:60` `web/src/api.ts:497`

## Mitigation

Carry the HTTP status on the error object and test it.
