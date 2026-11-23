---
code: UC-04
primary_actor: GitHub workflow runner
subdomain: localtokenomics root area
actors:
  - GitHub workflow runner
no_models_reason: No model of the specification is declared in the code this use case cites or in a file that code imports directly.
rules:
  - Python code must keep a pylint score of 9.0
  - Web dependencies are installed from the lockfile
tags:
  - ba/use-case
maturity: approved
---
# Check a change before merge

## Description

A pull request triggers the Python, web and CodeQL workflows, which run the same checks a maintainer runs locally.

## Preconditions

- A pull request is opened or main is pushed.

## Postconditions

- Each workflow reports pass or fail.

## Main flow

1. 1. The workflows start on a pull request or a push to main. `.github/workflows/python.yml:6`
2. 2. The Python workflow runs ruff, pylint, mypy and pytest. `.github/workflows/python.yml:54`
3. 3. The web workflow lints, type checks, tests and builds. `.github/workflows/web.yml:46`
4. 4. CodeQL analyses Python and JavaScript or TypeScript. `.github/workflows/codeql.yml:25`

## Alternative flows

- 2a. A failure in one Python version and operating system pair does not cancel the others. `.github/workflows/python.yml:20`

## Special requirements

CodeQL also runs weekly on Monday. `.github/workflows/codeql.yml:8`

## Acceptance criteria

- The pylint step fails below 9.0. `.github/workflows/python.yml:48`
- 2a: A failure in one Python version and operating system pair does not cancel the others. `.github/workflows/python.yml:20`

## Glossary

- [[Request]]

## Sources

- [[Code of localtokenomics]] @ implemented-by -> .github/workflows/python.yml | inferred
  > pull_request:
