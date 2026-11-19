---
code: RSK-31
impact: One malformed rates.json row stops scan, serve, export, alert and tui with a validation error
likelihood: low for the bundled file, medium for a file passed with --rates
tags:
  - ba/risk
maturity: draft
---
# An invalid rate file stops every command

## Risk

Loading validates the whole file with no handler `src/ai_usage_cost/pricing.py:287`.

## Mitigation

The model validators reject duplicate keys and overlapping periods at load, so a bad file fails loudly rather than pricing quietly.
