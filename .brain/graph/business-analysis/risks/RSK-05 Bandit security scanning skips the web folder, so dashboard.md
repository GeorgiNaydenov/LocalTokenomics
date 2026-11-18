---
code: RSK-05
impact: low
likelihood: low
tags:
  - ba/risk
maturity: draft
---
# Bandit security scanning skips the web folder, so dashboard

## Risk

Bandit security scanning skips the web folder, so dashboard code gets security analysis only from CodeQL.

## Mitigation

The CodeQL workflow scans JavaScript and TypeScript on every pull request and weekly.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> pyproject.toml | confirmed
  > exclude_dirs = ["tests", ".venv", "web"]
