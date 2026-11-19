---
code: RSK-18
impact: A person who mistypes config.json believes a project is excluded but the defaults apply
likelihood: medium
tags:
  - ba/risk
maturity: approved
---
# A privacy typo silently resets the settings

## Risk

An invalid file is replaced by defaults without a message `src/ai_usage_cost/privacy.py:67`.

## Mitigation

Not found in the code.
