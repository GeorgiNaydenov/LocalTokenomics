---
title: Repository folder layout
aliases: []
tags: [diagram, mermaid, package-tree]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [pyproject.toml, README.md, web/index.html, web/prototype.html]
verified-against: cfd43f684f91
sources: [docs/brain/architecture/diagrams/root-folders.mmd]
chunk: ch-localtokenomics-root
authored: true
node_citations:
  root-folders:
    root: ['README.md:620-637']
    pyproject: ['pyproject.toml:1-4']
    readme: ['README.md:5-9']
    src: ['README.md:620']
    web: ['README.md:637']
    tests: ['pyproject.toml:52']
    scripts: ['README.md:636']
    github: ['.github/workflows/python.yml:1-6']
    pkg: ['README.md:620']
    websrc: ['web/tsconfig.json:35-38']
    wpublic: ['README.md:2']
    workflows: ['.github/workflows/python.yml:1-6', '.github/workflows/web.yml:1-6',
      '.github/workflows/codeql.yml:1-8']
    sources: ['README.md:625']
    render: ['README.md:635']
    dist: ['web/vite.config.ts:14-17']
    cli: ['pyproject.toml:29-30', 'src/ai_usage_cost/cli.py:24']
    main: ['web/index.html:26']
    proto: ['web/prototype.html:25']
approved-by: human
approved-at: '2026-11-19T00:10:31+00:00'
---

# Repository folder layout

This tree shows how the repository is laid out on disk and where each run starts. A newcomer can find the Python package, the dashboard source, the tests and the automatic checks in one look. It saves the time otherwise spent opening folders to learn what lives where.

## What the diagram shows

- The README layout lists the package folder with its sources and render folders, the scripts folder and the web folder. `README.md:621` `README.md:625` `README.md:635`
- The scripts folder holds two maintainer tools, and the web folder holds the dashboard source. `README.md:636` `README.md:637`
- The tests folder is the test path of pytest. `pyproject.toml:52`
- The package metadata file declares the package and installs the console command, whose entry point is the app object in the command line module. `pyproject.toml:30` `src/ai_usage_cost/cli.py:24`
- The dashboard page loads its entry file from the source folder, and the prototype page loads a second entry file from the prototype folder. `web/index.html:26` `web/prototype.html:25`
- The public folder of the web project holds the logo used by the README. `README.md:2`
- The build writes the dashboard into a folder named web/dist inside the package folder. `web/vite.config.ts:15`
- The workflows folder holds the Python, Web and CodeQL workflows. `.github/workflows/python.yml:1` `.github/workflows/web.yml:1` `.github/workflows/codeql.yml:1`

## Capability and related functionality

- The tree realises the orientation capability of the repository root: it answers where code lives before a reader opens a folder. Details of the root files are in [[localtokenomics root Overview]].
- The folders under the package have their own chunks, for example [[Ai usage cost sources Overview]] and [[Ai usage cost render Overview]].
- Related maps of the root are [[Repository root concepts]], [[Repository root capabilities]] and [[Repository root configuration]]; the build flow is in [[LocalTokenomics root wiring]].

## The diagram

%% generated:diagram-root-folders start (do not edit; run brain docs generate) %%
```mermaid
flowchart TD
    root["(repository root)"]:::folder
    pyproject["pyproject.toml<br/>package metadata"]:::file
    readme["README.md<br/>product description"]:::file
    src["src/"]:::folder
    web["web/"]:::folder
    tests["tests/"]:::folder
    scripts["scripts/<br/>demo_logs.py, rates_diff.py"]:::folder
    github[".github/"]:::folder
    pkg["src/ai_usage_cost/"]:::folder
    websrc["web/src/"]:::folder
    wpublic["web/public/"]:::folder
    workflows[".github/workflows/<br/>python, web, codeql"]:::folder
    sources["sources/<br/>one module per reader"]:::folder
    render["render/<br/>terminal.py, png.py"]:::folder
    dist["web/dist/ inside the package<br/>built dashboard"]:::folder
    cli(["cli.py<br/>ai-usage-cost command"]):::entry
    main(["main.tsx<br/>dashboard entry"]):::entry
    proto(["prototype/main.tsx<br/>prototype entry"]):::entry
    root --> pyproject
    root --> readme
    root --> src
    root --> web
    root --> tests
    root --> scripts
    root --> github
    src --> pkg
    web --> websrc
    web --> wpublic
    github --> workflows
    pkg --> sources
    pkg --> render
    pkg --> dist
    pkg --> cli
    websrc --> main
    websrc --> proto
    subgraph Legend
        direction LR
        zlegend_a["Folder: a directory, drawn as on disk"]:::folder
        zlegend_b["File: a root file"]:::file
        zlegend_c(["Entry point: where a run starts"]):::entry
        zlegend_d["Arrow: parent contains child"]:::folder
        zlegend_a ~~~ zlegend_b ~~~ zlegend_c ~~~ zlegend_d
    end
    classDef folder fill:#dae8fc,stroke:#222222,color:#111111
    classDef file fill:#ffffff,stroke:#222222,color:#111111
    classDef entry fill:#ffe6cc,stroke:#222222,color:#111111
```
%% generated:diagram-root-folders end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `README.md:621` | Package layout in the README |
> | `pyproject.toml:51` | Tests folder |
> | `pyproject.toml:29` | Console command entry |
> | `web/index.html:26` | Dashboard entry file |
> | `web/prototype.html:25` | Prototype entry file |
> | `web/vite.config.ts:15` | Built dashboard folder |
