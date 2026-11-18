---
code: RSK-06
tags:
  - ba/risk
maturity: draft
---
# Risk 1: The dashboard client can write to the

## Risk

The dashboard client can write to the server with PUT for outcomes and DELETE for sessions, although it mainly reads usage.

## Mitigation

Confirm in the server chunk that delete only removes derived trace data; see `web/src/api.ts:593`.
