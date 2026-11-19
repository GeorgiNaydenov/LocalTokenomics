---
title: Repository root configuration
aliases: []
tags: [config-map, diagram, drawio]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [pyproject.toml, .pre-commit-config.yaml, web/*.ts, web/*.js, web/*.json]
verified-against: cfd43f684f91
sources: [docs/brain/architecture/drawio/drawio-root-settings.drawio]
chunk: ch-localtokenomics-root
authored: true
node_citations:
  drawio-root-settings:
    n1: ['pyproject.toml:1-13', 'pyproject.toml:32-34']
    n2: ['pyproject.toml:39-44']
    n3: ['pyproject.toml:46-49']
    n4: ['pyproject.toml:54-113']
    n5: ['pyproject.toml:51-52']
    n6: ['pyproject.toml:119-120']
    n7: ['web/vite.config.ts:6-31']
    n8: ['web/tsconfig.json:1-39']
    n9: ['web/eslint.config.js:1-25']
    n10: ['web/package.json:6-13']
    n11: ['.pre-commit-config.yaml:1-33']
    n12: ['src/ai_usage_cost/privacy.py:52-57', 'README.md:433-441']
    r1: ['pyproject.toml:32-37']
    r2: ['.github/workflows/python.yml:41-45', '.pre-commit-config.yaml:1-9']
    r3: ['.github/workflows/python.yml:50-51']
    r4: ['.github/workflows/python.yml:47-48', '.pre-commit-config.yaml:21-26']
    r5: ['.github/workflows/python.yml:53-54']
    r6: ['.github/workflows/python.yml:41-54', '.pre-commit-config.yaml:1-33']
    r7: ['web/package.json:7-8', 'web/package.json:12']
    r8: ['web/package.json:8-10']
    r9: ['web/package.json:11', 'web/package.json:11']
    r10: ['.github/workflows/web.yml:33-46']
    r11: ['.pre-commit-config.yaml:1-33']
    r12: ['src/ai_usage_cost/privacy.py:60-69']
approved-by: human
approved-at: '2026-11-19T00:10:31+00:00'
---

# Repository root configuration

This map lists every configuration file at the repository root and the tool that reads it. A maintainer can see which setting to change for a given tool and which settings are optional. It also shows the one settings block that no tool reads, and the one optional file that changes how the dashboard treats private content.

## What the diagram shows

- The project table in the package file names the package, its Python floor and its required libraries. The build system table names hatchling as the builder. `pyproject.toml:6` `pyproject.toml:33`
- The ruff table sets a line length of 100 and the rule families E, F, I, UP and B. `pyproject.toml:40` `pyproject.toml:44`
- The mypy table pins Python 3.11, loads the pydantic plugin and ignores missing imports. `pyproject.toml:47` `pyproject.toml:49`
- The pylint tables load the pydantic introspection list, set a line length of 100, disable checks that ruff already covers and fail under a score of 9.0. `pyproject.toml:58` `pyproject.toml:62` `pyproject.toml:113`
- The pytest table points the runner at the tests folder. `pyproject.toml:52`
- The bandit table excludes three folders. No file in the root chunk calls bandit. `pyproject.toml:120`
- The Vite file sets the base path, the alias, the build output folder, the development server with its API proxy and the test environment. `web/vite.config.ts:7` `web/vite.config.ts:11` `web/vite.config.ts:16` `web/vite.config.ts:28`
- The TypeScript file turns on strict mode, the unused checks and the same alias as Vite. `web/tsconfig.json:19` `web/tsconfig.json:20` `web/tsconfig.json:30`
- The ESLint file sets the rule presets, the React plugins and the ignored folders. `web/eslint.config.js:10` `web/eslint.config.js:8`
- The web package file defines the six scripts that the web workflow and the pre-commit hook call. `web/package.json:10` `.github/workflows/web.yml:40`
- The pre-commit file lists the hooks and marks mypy as manual. `.pre-commit-config.yaml:21` `.pre-commit-config.yaml:19`
- The optional settings file in the user's home folder has five settings, each with a default, and the privacy module reads it. The README lists only four of them, the fifth is accepted but inert and only produces a warning, and a file that fails to load or to validate is ignored as a whole. `src/ai_usage_cost/pipeline.py:242` `README.md:438` `src/ai_usage_cost/privacy.py:12` `src/ai_usage_cost/privacy.py:57` `src/ai_usage_cost/privacy.py:63` `src/ai_usage_cost/privacy.py:67`

## Capability and related functionality

- The map realises the configuration view of the repository root. It answers which file to open for a tool, where the wiring diagram [[LocalTokenomics root wiring]] answers how the tools connect.
- The settings file for private content is described for readers in [[localtokenomics root Security]] and its data model in [[localtokenomics root Data Model]].
- Environment variables are not shown here because no root file reads one. The source readers read them and belong to the sources chunk. Related maps: [[Repository root capabilities]], [[Repository folder layout]] and [[Repository root concepts]].

## The diagram

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `pyproject.toml:1` | Package metadata and required libraries |
> | `pyproject.toml:43` | Ruff rule families |
> | `pyproject.toml:119` | Bandit folder exclusions |
> | `web/vite.config.ts:20` | Development API proxy |
> | `web/tsconfig.json:19` | Strict type checking |
> | `web/eslint.config.js:11` | Files ESLint checks |
> | `.pre-commit-config.yaml:1` | Pre-commit hook list |
> | `src/ai_usage_cost/privacy.py:53` | Default of the first privacy setting |
