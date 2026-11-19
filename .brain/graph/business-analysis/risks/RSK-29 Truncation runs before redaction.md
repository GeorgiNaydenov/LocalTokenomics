---
code: RSK-29
impact: A secret cut at the byte limit can fall below a pattern's minimum length and be returned unredacted
likelihood: low, and only when metadata only is off
tags:
  - ba/risk
maturity: draft
---
# Truncation runs before redaction

## Risk

Released text is truncated first and redacted after `src/ai_usage_cost/privacy.py:97` `src/ai_usage_cost/privacy.py:98`.

## Mitigation

Content is off by default `src/ai_usage_cost/privacy.py:53`.
