---
code: RSK-32
impact: medium
likelihood: low
tags:
  - ba/risk
maturity: draft
---
# Chart style text is built from config keys without escaping

## Risk

The chart style element is filled by putting each config key and colour into a template string and passing it as HTML. The time chart builds its config keys from row data, so a key that holds a closing brace or a closing style tag would change the style rules or end the element. The data comes from local logs, so the exposure is small, but nothing validates the key. `web/src/components/ui/chart.tsx:102` `web/src/components/ui/chart.tsx:92` `web/src/components/chart-time.tsx:65`

## Mitigation

Map keys to safe indexed names such as series-1 before they enter the style text, and keep the readable name only in the label.

## Sources

- [[Code of localtokenomics]] | confirmed
  > return color ? `  --color-${key}: ${color};` : null
