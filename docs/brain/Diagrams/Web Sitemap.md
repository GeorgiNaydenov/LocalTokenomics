---
title: Web Sitemap
aliases: []
tags: [diagram, mermaid, sitemap]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
sources: [docs/brain/architecture/diagrams/web-information-architecture.mmd]
chunk: ch-localtokenomics-web-src
authored: true
node_citations:
  web-information-architecture:
    app: ['web/src/main.tsx:7-12']
    views: ['web/src/Header.tsx:24-24']
    wsp: ['web/src/SessionWorkspace.tsx:72-72']
    ov: ['web/src/Header.tsx:25-25']
    se: ['web/src/Header.tsx:26-26']
    so: ['web/src/Header.tsx:27-27']
    pr: ['web/src/Header.tsx:28-28']
    su: ['web/src/SessionWorkspace.tsx:73-73']
    tr: ['web/src/SessionWorkspace.tsx:74-74']
    ec: ['web/src/SessionWorkspace.tsx:75-75']
    cx: ['web/src/SessionWorkspace.tsx:76-76']
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Web Sitemap

This map shows every page of the dashboard and how the pages are grouped. A reader sees that there are four views and one session panel with four tabs. None of them needs a sign in, because the dashboard runs on the reader's own machine.

## What the diagram shows

- The four views are named in the header tab strip `web/src/Header.tsx:24-24`.
- The workspace has four tabs, Summary, Trace, Economics and Context `web/src/SessionWorkspace.tsx:72-72`.
- The dashboard has no routes: the view and the open session are component state in App `web/src/App.tsx:136-137`.
- All requests go to relative paths under api on the same server `web/src/api.ts:503-503` `web/src/api.ts:539-540`.

## Capability and related functionality

The transitions between these pages are in [[Web Screen Flow]] and the layout of each page in its screen note, starting at [[App Screen]]. The server side of the paths belongs to [[Web API]].

## Web Sitemap

%% generated:diagram-web-information-architecture start (do not edit; run brain docs generate) %%
```mermaid
flowchart TD
    app("LocalTokenomics dashboard"):::section --> views("Views in the header"):::section
    app --> wsp("Session workspace"):::section
    views --> ov["Overview"]:::page
    views --> se["Sessions"]:::page
    views --> so["Sources"]:::page
    views --> pr["Models and pricing"]:::page
    wsp --> su["Summary"]:::page
    wsp --> tr["Trace"]:::page
    wsp --> ec["Economics"]:::page
    wsp --> cx["Context"]:::page
    se -.->|opens| wsp
    ov -.->|links to| so
    subgraph Legend
        direction LR
        zl1("Rounded box: a section"):::section
        zl2["Rectangle: a page or tab"]:::page
        zl3["Dashed line: a cross link. No page needs sign in."]:::page
    end
    classDef section fill:#eeeeee,stroke:#222222,color:#222222
    classDef page fill:#dae8fc,stroke:#222222,color:#142233
```
%% generated:diagram-web-information-architecture end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/Header.tsx:24-24` | The four views are named in the header tab strip |
> | `web/src/SessionWorkspace.tsx:72-72` | The workspace has four tabs, Summary, Trace, Economics and Context |
> | `web/src/App.tsx:136-137` | The dashboard has no routes: the view and the open session are component state in App |
> | `web/src/api.ts:503-503` | All requests go to relative paths under api on the same server |
> | `web/src/api.ts:539-540` | All requests go to relative paths under api on the same server |
