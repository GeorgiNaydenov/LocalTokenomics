---
code: RSK-15
impact: Anyone who can reach the port can read costs and, with the content route, span text if metadata only is off, and can forget sessions
likelihood: low while the host stays on loopback
tags:
  - ba/risk
maturity: approved
---
# HTTP routes have no authentication

## Risk

No route checks a caller `src/ai_usage_cost/api.py:198`.

## Mitigation

The default host is the loopback address `src/ai_usage_cost/cli.py:110` and metadata only is on by default `src/ai_usage_cost/privacy.py:53`.
