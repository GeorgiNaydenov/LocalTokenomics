---
code: RSK-34
impact: low
likelihood: low
tags:
  - ba/risk
maturity: draft
---
# A chart legend label is empty for a series with no config entry

## Risk

The legend content prints only the config label, with no fallback to the series name, so a series missing from the config shows a colour square and no text, while the tooltip falls back to the raw name. `web/src/components/ui/chart.tsx:319` `web/src/components/ui/chart.tsx:249`

## Mitigation

Fall back to the series name in the legend as the tooltip does.
