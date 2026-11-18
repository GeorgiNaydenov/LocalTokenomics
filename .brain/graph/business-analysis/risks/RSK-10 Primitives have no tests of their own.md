---
code: RSK-10
tags:
  - ba/risk
maturity: approved
---
# Primitives have no tests of their own

## Risk

No test file lives in this folder, so a change to a shared primitive is exercised only through the screens that import it.

## Mitigation

Cover primitives through the screens that use them, or add tests beside the primitives.
