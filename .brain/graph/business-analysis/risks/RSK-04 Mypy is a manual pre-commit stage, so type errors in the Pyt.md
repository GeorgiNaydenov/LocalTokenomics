---
code: RSK-04
impact: low
likelihood: medium
tags:
  - ba/risk
maturity: approved
---
# Mypy is a manual pre-commit stage, so type errors in the Pyt

## Risk

Mypy is a manual pre-commit stage, so type errors in the Python package are caught only by the workflow or a deliberate local run.

## Mitigation

The Python workflow runs mypy on src for every pull request.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> .pre-commit-config.yaml | confirmed
  > stages: [manual]
