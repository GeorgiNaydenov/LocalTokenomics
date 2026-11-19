---
title: Repository root capabilities
aliases: []
tags: [capability, diagram, drawio]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [pyproject.toml, .pre-commit-config.yaml, .github/workflows/**, web/*.ts,
  web/*.js, web/*.json]
verified-against: cfd43f684f91
sources: [docs/brain/architecture/drawio/drawio-root-families.drawio]
chunk: ch-localtokenomics-root
authored: true
node_citations:
  drawio-root-families:
    c1: ['pyproject.toml:29-30']
    c2: ['pyproject.toml:15-27']
    c3: ['pyproject.toml:36-37', 'web/vite.config.ts:14-17']
    c4: ['web/vite.config.ts:14-17', 'web/package.json:8']
    c5: ['web/vite.config.ts:18-26']
    c6: ['web/vite.config.ts:27-30', 'web/src/test-setup.ts:6-8']
    c7: ['pyproject.toml:39-44']
    c8: ['pyproject.toml:46-49', 'web/tsconfig.json:19-22']
    c9: ['pyproject.toml:112-113']
    c10: ['web/eslint.config.js:8-23']
    c11: ['.pre-commit-config.yaml:1-33']
    c12: ['pyproject.toml:119-120', '.github/workflows/python.yml:41-54']
    c13: ['.github/workflows/python.yml:21-23', '.github/workflows/python.yml:41-54']
    c14: ['.github/workflows/web.yml:36-46']
    c15: ['.github/workflows/codeql.yml:3-8', '.github/workflows/codeql.yml:25']
    f1: ['pyproject.toml:1-37']
    f2: ['web/vite.config.ts:6-31']
    f3: ['pyproject.toml:39-49']
    f4: ['.github/workflows/python.yml:1-6']
approved-by: human
approved-at: '2026-11-19T00:10:31+00:00'
---

# Repository root capabilities

This map shows what the repository root lets a maintainer do, grouped by the job each file serves. It covers installing the tool, building the dashboard, keeping the code healthy and checking every change. It also shows the one check that is set up but never run, which a maintainer may want to wire in.

## What the diagram shows

- Installing the package gives anyone the console command named ai-usage-cost. `pyproject.toml:30`
- The extras for charts, SQL browsing, alerts and the text interface are optional, so they are chosen at install time. `pyproject.toml:16` `pyproject.toml:19`
- The wheel contains only the Python package folder, and the dashboard build writes into that folder, so the built dashboard ships inside the wheel. `pyproject.toml:37` `web/vite.config.ts:15`
- The build script runs the type checker before Vite, so a type error stops the bundle. `web/package.json:8`
- The development server forwards every API request to the Python server for hot reload against live data. `web/vite.config.ts:21` `web/vite.config.ts:22`
- Component tests run in a simulated browser and a setup file cleans up after each test. `web/vite.config.ts:28` `web/src/test-setup.ts:7`
- Ruff checks the rule families E, F, I, UP and B with a line length of 100. `pyproject.toml:40` `pyproject.toml:44`
- Mypy runs with the pydantic plugin and the dashboard type checker runs in strict mode. `pyproject.toml:48` `web/tsconfig.json:19`
- Pylint must score at least 9.0. `pyproject.toml:113`
- ESLint applies the React hooks rules and ignores the built dashboard. `web/eslint.config.js:21` `web/eslint.config.js:8`
- The pre-commit file runs ruff, ruff format, pylint and ESLint, and keeps mypy as a manual stage. `.pre-commit-config.yaml:19` `.pre-commit-config.yaml:30`
- Bandit is configured to skip the tests, the virtual environment and the web folder. No step of the Python workflow or the pre-commit file runs it. `pyproject.toml:120` `.github/workflows/python.yml:53`
- The Python workflow tests on Ubuntu and Windows with Python 3.11, 3.12 and 3.13. `.github/workflows/python.yml:22` `.github/workflows/python.yml:23`
- The web workflow runs lint, type check, test and build. `.github/workflows/web.yml:37` `.github/workflows/web.yml:46`
- CodeQL analyses Python and TypeScript on pull requests, pushes and a weekly schedule. `.github/workflows/codeql.yml:25` `.github/workflows/codeql.yml:8`

## Capability and related functionality

- The map realises the build and quality capability of the repository root, the same capability as in [[LocalTokenomics root wiring]], seen as a list of jobs rather than as a flow.
- It serves the maintainer. The files it groups are explained in [[localtokenomics root Overview]] and [[localtokenomics root Operations]], and the settings behind them in [[Repository root configuration]].
- The one dashed box is a gap worth a decision: the security lint setting exists but nothing runs it. It is also recorded in [[localtokenomics root Security]] and in the specification of this chunk.
- The concepts behind the jobs are in [[Repository root concepts]], and the folders they touch in [[Repository folder layout]].

## The diagram

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `pyproject.toml:29` | Console command |
> | `pyproject.toml:36` | Wheel contents |
> | `web/vite.config.ts:14` | Dashboard build output |
> | `web/vite.config.ts:27` | Test runner settings |
> | `pyproject.toml:119` | Security lint configuration |
> | `.github/workflows/python.yml:19` | Python test matrix |
> | `.github/workflows/web.yml:19` | Web checks |
> | `.github/workflows/codeql.yml:18` | CodeQL analysis |
