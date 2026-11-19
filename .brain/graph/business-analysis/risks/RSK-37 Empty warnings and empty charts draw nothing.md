---
code: RSK-37
impact: low
likelihood: medium
tags:
  - ba/risk
maturity: draft
---
# Empty warnings and empty charts draw nothing

## Risk

The warnings list, the time chart, the sparkline and the context bars return an empty area or nothing when they have no data, and the component gives no message, so a page that forgets its own empty card shows a blank space. `web/src/components/chart-time.tsx:95` `web/src/components/states.tsx:272`

## Mitigation

Pages already pass an empty card in most places; add the same in every place that renders these parts, or give the parts an empty message prop.
