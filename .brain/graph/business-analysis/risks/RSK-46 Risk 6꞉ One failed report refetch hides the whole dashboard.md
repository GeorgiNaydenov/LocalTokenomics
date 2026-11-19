---
code: RSK-46
impact: medium
likelihood: medium
tags:
  - ba/risk
maturity: draft
---
# Risk 6: One failed report refetch hides the whole dashboard

## Risk

A failed report request after the first load sets the shared error, and the shell then replaces every view with an error card that has no retry action. `web/src/App.tsx:193` `web/src/App.tsx:274`

## Mitigation

Keep the last report on screen with an inline error and a retry, or pass a retry handler to the error card.
