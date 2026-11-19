---
title: UC-04 Check a change before merge
aliases: [UC-04, Check a change before merge]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
use-cases: [UC-04]
subdomain: ''
---

# UC-04 Check a change before merge

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Actors:** [[Actors#GitHub workflow runner|GitHub workflow runner]], [[Actors|Python code must keep a pylint score of 9.0]], [[Actors|Web dependencies are installed from the lockfile]]
- **Maturity:** approved

## Description

A pull request triggers the Python, web and CodeQL workflows, which run the same checks a maintainer runs locally.

## Preconditions

A pull request is opened or main is pushed.

## Main flow

1. 1. The workflows start on a pull request or a push to main. `.github/workflows/python.yml:6`
2. 2. The Python workflow runs ruff, pylint, mypy and pytest. `.github/workflows/python.yml:54`
3. 3. The web workflow lints, type checks, tests and builds. `.github/workflows/web.yml:46`
4. 4. CodeQL analyses Python and JavaScript or TypeScript. `.github/workflows/codeql.yml:25`

## Alternative flows

2a. A failure in one Python version and operating system pair does not cancel the others. `.github/workflows/python.yml:20`

## Postconditions

Each workflow reports pass or fail.

## Acceptance criteria

The pylint step fails below 9.0. `.github/workflows/python.yml:48`
