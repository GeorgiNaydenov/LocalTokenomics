---
title: LocalTokenomics root wiring
aliases: []
tags: [c4, diagram, mermaid]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/*]
sources: [docs/brain/architecture/diagrams/c4-localtokenomics-root-wiring.mmd]
chunk: ch-localtokenomics-root
authored: true
node_citations:
  c4-localtokenomics-root-wiring:
    dev: ['web/package.json:6-13']
    pkg: ['pyproject.toml:29-37']
    vite: ['web/vite.config.ts:6-31']
    lint: ['web/eslint.config.js:7-25']
    dist: ['web/vite.config.ts:14-17']
    ci: ['pyproject.toml:1-4', '.github/workflows/python.yml:3-6', '.github/workflows/web.yml:3-6']
    api: ['web/vite.config.ts:18-26']
---

# LocalTokenomics root wiring

This view shows how the top level files of the project fit together. It explains how the dashboard is built, where the finished files end up, and which automatic checks guard both halves. A maintainer can use it to see what to change, and what to run, before touching the dashboard or the package.

## What the diagram shows

The maintainer edits the dashboard source and runs the build script from the web folder. `web/package.json:6-13`

The build configuration writes the finished dashboard into a folder inside the Python package. `web/vite.config.ts:14-17`

The package metadata builds the installable wheel from that same package folder, so the finished dashboard is shipped with it. `pyproject.toml:32-37`

During development the dashboard dev server forwards every request that starts with `/api` to the Python server on port 8420. `web/vite.config.ts:18-26`

The dashboard lint rules apply to the dashboard TypeScript files and skip the built folder. `web/eslint.config.js:8-11`

The Python workflow runs on a pull request and a push to the main branch. It runs ruff, pylint, mypy and pytest. `.github/workflows/python.yml:3-6` `.github/workflows/python.yml:41-54`

The web workflow runs on the same triggers and runs lint, type check, test and build. `.github/workflows/web.yml:3-6` `.github/workflows/web.yml:36-46`

## Capability and related functionality

The diagram realises the build and quality capability of the repository root. It serves the maintainer, not the person who only installs the tool. The files it shows are explained in [[localtokenomics root Overview]] and [[localtokenomics root Operations]], and the dashboard tests are in [[localtokenomics root Tests]]. The generated module map for the same chunk is in [[localtokenomics root Diagrams]].

## LocalTokenomics root wiring

%% generated:diagram-c4-localtokenomics-root-wiring start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    dev(["Maintainer<br/>person"]):::person
    subgraph sys["LocalTokenomics repository root"]
        pkg["pyproject.toml<br/>ai-usage-cost package<br/>Python, hatchling"]:::system
        vite["web/vite.config.ts<br/>dashboard build and dev server<br/>Vite, React, Tailwind"]:::system
        lint["web/eslint.config.js<br/>dashboard lint rules<br/>ESLint"]:::system
        dist["src/ai_usage_cost/web/dist<br/>built dashboard bundle<br/>static files"]:::system
    end
    ci["GitHub workflows<br/>run by a schedule or a pull request<br/>python, web, codeql"]:::run
    api["Python server<br/>127.0.0.1:8420<br/>serves /api"]:::external
    dev -->|"edits web/src, runs npm build"| vite
    vite -->|"writes bundle"| dist
    pkg -->|"ships wheel with"| dist
    vite -.->|"dev proxy of /api"| api
    ci -->|"runs lint, typecheck, test, build"| lint
    ci -->|"runs ruff, pylint, mypy, pytest"| pkg
    subgraph Legend
        direction LR
        zl_a(["Person"]):::person
        zl_b["Part of this system"]:::system
        zl_c["Run by a schedule or a pull request"]:::run
        zl_d["System with its own source folder"]:::external
        zl_e["Solid arrow: required call or output"]:::system
        zl_f["Dashed arrow: development only"]:::system
        zl_a ~~~ zl_b ~~~ zl_c ~~~ zl_d ~~~ zl_e ~~~ zl_f
    end
    classDef person fill:#fff2cc,stroke:#222222,color:#111111
    classDef system fill:#dae8fc,stroke:#222222,color:#111111
    classDef run fill:#ffe6cc,stroke:#222222,color:#111111
    classDef external fill:#eeeeee,stroke:#222222,stroke-dasharray:5 3,color:#111111
```
%% generated:diagram-c4-localtokenomics-root-wiring end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/vite.config.ts:14-17` | Build output folder inside the Python package |
> | `web/vite.config.ts:18-26` | Dev server port and the `/api` proxy |
> | `web/eslint.config.js:7-25` | Lint rules and ignored folders |
> | `web/package.json:6-13` | Dashboard scripts the maintainer and the web workflow run |
> | `pyproject.toml:29-37` | Console script and wheel contents |
> | `.github/workflows/python.yml:3-54` | Python checks |
> | `.github/workflows/web.yml:3-46` | Web checks |
