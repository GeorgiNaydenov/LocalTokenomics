---
title: Web Concept Map
aliases: []
tags: [diagram, mermaid, mind-map]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
sources: [docs/brain/architecture/diagrams/web-concepts.mmd]
chunk: ch-localtokenomics-web-src
authored: true
node_citations:
  web-concepts:
    'Screens': ['web/src/Header.tsx:24-24']
    'Overview': ['web/src/Header.tsx:24-24']
    'Sessions': ['web/src/Header.tsx:24-24']
    'Sources': ['web/src/Header.tsx:24-24']
    'Models and pricing': ['web/src/Header.tsx:24-24']
    'Session workspace': ['web/src/SessionWorkspace.tsx:72-72']
    'Data from the server': ['web/src/api.ts:502-511']
    'Meta': ['web/src/api.ts:502-502']
    'Report': ['web/src/api.ts:535-535']
    'Rate table': ['web/src/api.ts:510-510']
    'Trace, economics, context': ['web/src/api.ts:543-555']
    'Filters and query': ['web/src/App.tsx:23-35']
    'Saved views': ['web/src/FilterRail.tsx:145-173']
    'Facets': ['web/src/App.tsx:151-164']
    'Date range': ['web/src/FilterRail.tsx:320-329']
    'Switches': ['web/src/FilterRail.tsx:431-435']
    'Session judgement': ['web/src/SessionWorkspace.tsx:262-262']
    'Outcome rating': ['web/src/SessionWorkspace.tsx:79-79']
    'Notes and tags': ['web/src/SessionWorkspace.tsx:244-248']
    'Web dashboard': ['web/src/main.tsx:7-12']
---

# Web Concept Map

This picture gives a newcomer the main ideas of the dashboard on one page. It groups them into what the reader sees, what comes from the server, how the slice is narrowed and how a session is judged. It is the starting point before reading the screen maps.

## What the diagram shows

- The screens are the four views in the header tab strip plus the session workspace `web/src/Header.tsx:24-24` `web/src/App.tsx:342-342`.
- The data comes from the metadata, rate table and report requests, and from the per session trace, economics and context requests `web/src/api.ts:502-511` `web/src/api.ts:543-555`.
- The query holds search, cost states, clients, models, projects, outcomes and three switches `web/src/App.tsx:23-35`.
- A session is judged with an outcome label plus notes and tags `web/src/SessionWorkspace.tsx:79-79` `web/src/SessionWorkspace.tsx:244-248`.

## Capability and related functionality

The concepts are drawn as related terms in [[Web Glossary Map]], the screens in [[Web Sitemap]] and the files in [[Web Package Tree]]. The notes of the chunk are [[Web Overview]], [[Web Workflows]] and [[Web Data Model]].

## Web Concept Map

%% generated:diagram-web-concepts start (do not edit; run brain docs generate) %%
```mermaid
mindmap
  root((Web dashboard))
    Screens
      Overview
      Sessions
      Sources
      Models and pricing
      Session workspace
    Data from the server
      Meta
      Report
      Rate table
      Trace, economics, context
    Filters and query
      Saved views
      Facets
      Date range
      Switches
    Session judgement
      Outcome rating
      Notes and tags
    Legend
      First level: a main concern of the chunk
      Second level: a concept inside that concern
```
%% generated:diagram-web-concepts end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/Header.tsx:24-24` | The screens are the four views in the header tab strip plus the session workspace |
> | `web/src/App.tsx:342-342` | The screens are the four views in the header tab strip plus the session workspace |
> | `web/src/api.ts:502-511` | The data comes from the metadata, rate table and report requests, and from the per session trace, economics and context requests |
> | `web/src/api.ts:543-555` | The data comes from the metadata, rate table and report requests, and from the per session trace, economics and context requests |
> | `web/src/App.tsx:23-35` | The query holds search, cost states, clients, models, projects, outcomes and three switches |
> | `web/src/SessionWorkspace.tsx:79-79` | A session is judged with an outcome label plus notes and tags |
> | `web/src/SessionWorkspace.tsx:244-248` | A session is judged with an outcome label plus notes and tags |
