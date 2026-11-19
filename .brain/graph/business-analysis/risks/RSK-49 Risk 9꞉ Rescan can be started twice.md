---
code: RSK-49
impact: low
likelihood: medium
tags:
  - ba/risk
maturity: draft
---
# Risk 9: Rescan can be started twice

## Risk

The Rescan logs button stays enabled while a scan runs, only its label changes, so a second press sends a second refresh. `web/src/Header.tsx:128` `web/src/App.tsx:211`

## Mitigation

Disable the button while rescanning is true.
