---
code: RSK-50
impact: medium
likelihood: high
tags:
  - ba/risk
maturity: draft
---
# Risk 10: Session rows cannot be opened from the keyboard

## Risk

A sessions table row opens the workspace on click only, with no tab stop or key handler, while the turn rows of the trace tab do have both. `web/src/Sessions.tsx:355` `web/src/TraceTab.tsx:686`

## Mitigation

Give the row a tab stop and an Enter handler, or put a button in the session cell.
