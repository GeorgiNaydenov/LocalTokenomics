---
title: Web Package Tree
aliases: []
tags: [diagram, mermaid, package-tree]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
sources: [docs/brain/architecture/diagrams/web-folders.mmd]
chunk: ch-localtokenomics-web-src
authored: true
node_citations:
  web-folders:
    web: ['web/index.html:7-7']
    idx: ['web/index.html:7-7']
    src: ['web/src/main.tsx:3-3']
    main: ['web/src/main.tsx:7-12']
    screens: ['web/src/App.tsx:4-11']
    helpers: ['web/src/App.tsx:3-3', 'web/src/App.tsx:12-12']
    comps: ['web/src/App.tsx:15-15']
    ui: ['web/src/Header.tsx:6-6']
    ds: ['web/src/main.tsx:5-5']
    proto: ['web/src/prototype/main.tsx:1-1']
    pmain: ['web/src/prototype/main.tsx:1-1']
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Web Package Tree

This tree shows how the dashboard's files are laid out on disk. It helps a developer see which folder belongs to this part of the documentation and which belong to its neighbours. The two entry points show where the page and the prototype start.

## What the diagram shows

- The page starts at the entry file, which mounts App with the theme stylesheet `web/src/main.tsx:3-7`.
- App imports the screen components and the helpers that sit beside it in the same folder `web/src/App.tsx:3-12`.
- Shared components and the design system are imported through the at sign alias `web/src/App.tsx:14-18`.
- The theme is applied before the page loads by a script in the HTML file `web/index.html:11-11`.

## Capability and related functionality

This chunk owns the files directly in web/src and in the design system. The folders web/src/components, web/src/components/ui and web/src/prototype belong to their own chunks, described in [[Web UI components Overview]], [[Web ui UI components Overview]] and [[Web prototype Overview]]. The composition of the screens is [[Web Component Composition]].

## Web Package Tree

%% generated:diagram-web-folders start (do not edit; run brain docs generate) %%
```mermaid
flowchart TD
    web["web"]:::folder --> src["web/src"]:::folder
    web --> idx(["index.html"]):::entry
    src --> main(["main.tsx"]):::entry
    src --> screens["screen components: App, Header, FilterRail, Overview, Sessions, Sources, Pricing, SessionWorkspace and three tabs"]:::folder
    src --> helpers["helpers: api, format, pricing-format, pricing-notes, turn-insights, theme"]:::folder
    src --> comps["web/src/components"]:::folder
    comps --> ui["web/src/components/ui"]:::folder
    src --> ds["web/src/design-system"]:::folder
    src --> proto["web/src/prototype"]:::folder
    proto --> pmain(["prototype main.tsx"]):::entry
    subgraph Legend
        direction LR
        zl1["Box: a folder or a group of files"]:::folder
        zl2(["Stadium: an entry point"]):::entry
        zl3["Arrow reads: contains"]:::folder
    end
    classDef folder fill:#dae8fc,stroke:#222222,color:#142233
    classDef entry fill:#fff2cc,stroke:#222222,color:#222222
```
%% generated:diagram-web-folders end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/main.tsx:3-7` | The page starts at the entry file, which mounts App with the theme stylesheet |
> | `web/src/App.tsx:3-12` | App imports the screen components and the helpers that sit beside it in the same folder |
> | `web/src/App.tsx:14-18` | Shared components and the design system are imported through the at sign alias |
> | `web/index.html:11-11` | The theme is applied before the page loads by a script in the HTML file |
