---
code: BR-11
category: quality
tags:
  - ba/rule
maturity: approved
---
# Python code must keep a pylint score of 9.0

## Statement

Both the Python workflow and the pre-commit hook fail when pylint scores below 9.0.

## Enforced in

- [[UC-04 Check a change before merge]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> pyproject.toml | confirmed
  > fail-under = 9.0
- [[Code of localtokenomics]] @ enforced-by -> .github/workflows/python.yml | confirmed
  > run: uv run --no-sync pylint src tests --fail-under=9.0
