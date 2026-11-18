---
title: localtokenomics root Operations
aliases: []
tags: [operations]
area: operations
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/*]
verified-against: 696b7c3b3902
chunk: ch-localtokenomics-root
approved-by: human
approved-at: '2026-11-18T19:00:53+00:00'
---

# localtokenomics root Operations

Build, packaging, CI and configuration files that belong to the localtokenomics root chunk.

## How it works

5 operational files were found.

## Continuous checks

Three workflows run on every pull request and on pushes to `main`. `.github/workflows/python.yml:3-6` `.github/workflows/web.yml:3-6` `.github/workflows/codeql.yml:3-6` A newer run cancels an older one on the same branch, and each workflow asks only for read access to the repository contents. `.github/workflows/python.yml:8-13`

The Python workflow tests on Ubuntu and Windows with Python 3.11, 3.12 and 3.13, and a failure in one combination does not stop the others. `.github/workflows/python.yml:16-23` Each run installs the dev extras with uv, then runs ruff check, ruff format check, pylint with a floor of 9.0, mypy on `src`, and pytest. `.github/workflows/python.yml:36-54`

The web workflow runs inside the `web` folder on Node 22. It installs with `npm ci` from the lockfile, then lints, type checks, tests and builds. `.github/workflows/web.yml:15-46`

The CodeQL workflow scans Python and JavaScript or TypeScript on the same triggers and also once a week on Monday. `.github/workflows/codeql.yml:7-8` `.github/workflows/codeql.yml:22-25` It is the only workflow with permission to write security events. `.github/workflows/codeql.yml:14-16`

## Packaging and local scripts

`pyproject.toml` declares the build backend, the single console script `ai-usage-cost`, the dependency list and the tool settings. `pyproject.toml:29-37` `web/package.json` declares the dashboard scripts and pins exact versions. `web/package.json:6-45` The local pre-commit hooks mirror the same checks, so most failures show up before a push. `.pre-commit-config.yaml:1-33`

## What a reader must know

The Python and web workflows run the same commands a developer runs locally: `npm run lint`, `npm run typecheck`, `npm test` and `npm run build` map to scripts in `web/package.json`. `.github/workflows/web.yml:36-46` `web/package.json:6-13` Node 22 runs in the workflow and the README asks for Node 20 or newer, so both are supported. `README.md:138-140`

## Reference

%% generated:chunk-ops start (do not edit; run brain docs generate) %%
| File | Lines | Code |
|---|---|---|
| `.github/workflows/codeql.yml` | 40 | `.github/workflows/codeql.yml` `.github/workflows/codeql.yml:1-40` |
| `.github/workflows/python.yml` | 54 | `.github/workflows/python.yml` `.github/workflows/python.yml:1-54` |
| `.github/workflows/web.yml` | 46 | `.github/workflows/web.yml` `.github/workflows/web.yml:1-46` |
| `pyproject.toml` | 120 | [[pyproject.toml]] `pyproject.toml:1-120` |
| `web/package.json` | 46 | [[web/package.json]] `web/package.json:1-46` |
%% generated:chunk-ops end %%
