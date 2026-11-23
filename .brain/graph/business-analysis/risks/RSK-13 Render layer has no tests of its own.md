---
code: RSK-13
impact: medium
likelihood: medium
tags:
  - ba/risk
maturity: approved
---
# Render layer has no tests of its own

## Risk

No test file imports or lives inside the render folder, so output format changes are not caught here.

## Mitigation

Add tests for the headline text, the 30 row cut and the empty project panel.

## Sources

- [[Code of localtokenomics]] | open
  > def render(
