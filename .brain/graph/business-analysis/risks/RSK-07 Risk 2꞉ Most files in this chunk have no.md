---
code: RSK-07
tags:
  - ba/risk
maturity: draft
---
# Risk 2: Most files in this chunk have no

## Risk

Most files in this chunk have no test importing them, only the pure helper modules are tested.

## Mitigation

Add component tests for the views if they change often; the tested helpers include `web/src/format.ts:20`.
