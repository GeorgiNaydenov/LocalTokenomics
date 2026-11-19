---
code: RSK-36
impact: low
likelihood: medium
tags:
  - ba/risk
maturity: draft
---
# A failed copy of the start command gives no feedback

## Risk

The offline card swallows a rejected clipboard write, so on a browser that blocks clipboard access the button stays at Copy command and the reader is not told that nothing was copied. `web/src/components/states.tsx:300`

## Mitigation

Show a short failure label or select the command text so the reader can copy it by hand.
