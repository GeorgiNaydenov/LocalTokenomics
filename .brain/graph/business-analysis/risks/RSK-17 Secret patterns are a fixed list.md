---
code: RSK-17
impact: A secret in a form the patterns do not match is returned in released text
likelihood: low, and only when metadata only is off
tags:
  - ba/risk
maturity: approved
---
# Secret patterns are a fixed list

## Risk

Redaction relies on nine patterns `src/ai_usage_cost/privacy.py:14`.

## Mitigation

Content is off by default `src/ai_usage_cost/privacy.py:53` and text is cut to a byte limit `src/ai_usage_cost/privacy.py:11`.
