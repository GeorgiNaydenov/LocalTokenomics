---
code: RSK-35
impact: low
likelihood: medium
tags:
  - ba/risk
maturity: draft
---
# Hidden columns and shown columns can disagree

## Risk

When a reader unchecks every column, the table guard returns the full column list, so the table still shows every column while the chooser shows every box unchecked. `web/src/components/columns.tsx:59` `web/src/components/columns.tsx:85`

## Mitigation

Either keep the last column checked and disabled in the chooser, or show an explanation when the guard applies.
