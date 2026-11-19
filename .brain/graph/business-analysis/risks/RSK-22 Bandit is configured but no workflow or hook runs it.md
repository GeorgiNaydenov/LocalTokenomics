---
code: RSK-22
impact: low
likelihood: high
tags:
  - ba/risk
maturity: draft
---
# Bandit is configured but no workflow or hook runs it

## Risk

The package file holds a bandit section and the dev extras install bandit, but the Python workflow steps and the pre-commit hooks never call it. The security lint therefore never gates a change; only CodeQL does.

## Mitigation

Add a bandit step to the Python workflow, or remove the unused section and extra so the files do not suggest a check that does not run.

## Sources

- [[Code of localtokenomics]] @ declared-in -> pyproject.toml | confirmed
  > [tool.bandit]
- [[Code of localtokenomics]] @ declared-in -> pyproject.toml | confirmed
  > "bandit>=1.7",
- [[Code of localtokenomics]] @ enforced-by -> .github/workflows/python.yml | inferred
  > run: uv run --no-sync pytest -q
