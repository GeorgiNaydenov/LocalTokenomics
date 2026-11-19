---
code: RSK-47
impact: low
likelihood: low
tags:
  - ba/risk
maturity: draft
---
# Risk 7: Outcome saves are not sequenced

## Risk

A rating pick and a notes or tags blur each start a save while another may still run, and the toggle stays enabled during a save, so answers can arrive out of order and the older one can win. `web/src/SessionWorkspace.tsx:274` `web/src/SessionWorkspace.tsx:312`

## Mitigation

Queue saves or ignore answers of superseded saves.
