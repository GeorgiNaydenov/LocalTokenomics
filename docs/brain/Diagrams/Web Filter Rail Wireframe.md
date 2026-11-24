---
title: Web Filter Rail Wireframe
aliases: []
tags: [diagram, drawio, wireframe]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
sources: [docs/brain/architecture/drawio/drawio-web-filter-rail.drawio, docs/brain/architecture/drawio/drawio-web-filter-rail-filter-rail-docked-aside-or-filters-sheet-on-narrow-screens.drawio,
  docs/brain/architecture/drawio/drawio-web-filter-rail-other.drawio]
chunk: ch-localtokenomics-web-src
authored: true
node_citations:
  drawio-web-filter-rail:
    rail: ['web/src/FilterRail.tsx:474-503']
    f-search: ['web/src/FilterRail.tsx:474-503']
    f-views: ['web/src/FilterRail.tsx:474-503']
    f-v1: ['web/src/FilterRail.tsx:474-503']
    f-v2: ['web/src/FilterRail.tsx:474-503']
    f-v3: ['web/src/FilterRail.tsx:474-503']
    f-v4: ['web/src/FilterRail.tsx:474-503']
    f-v5: ['web/src/FilterRail.tsx:474-503']
    f-v6: ['web/src/FilterRail.tsx:474-503']
    f-range: ['web/src/FilterRail.tsx:474-503']
    f-r1: ['web/src/FilterRail.tsx:474-503']
    f-r2: ['web/src/FilterRail.tsx:474-503']
    f-r3: ['web/src/FilterRail.tsx:474-503']
    f-r4: ['web/src/FilterRail.tsx:474-503']
    f-r5: ['web/src/FilterRail.tsx:474-503']
    f-r6: ['web/src/FilterRail.tsx:474-503']
    f-r7: ['web/src/FilterRail.tsx:474-503']
    f-dates: ['web/src/FilterRail.tsx:474-503']
    f-state: ['web/src/FilterRail.tsx:474-503']
    f-outcome: ['web/src/FilterRail.tsx:474-503']
    f-clients: ['web/src/FilterRail.tsx:474-503']
    f-models: ['web/src/FilterRail.tsx:474-503']
    f-projects: ['web/src/FilterRail.tsx:474-503']
    f-s1: ['web/src/FilterRail.tsx:474-503']
    f-s2: ['web/src/FilterRail.tsx:474-503']
    f-s3: ['web/src/FilterRail.tsx:474-503']
    f-clear: ['web/src/FilterRail.tsx:474-503']
    f-undetected: ['web/src/FilterRail.tsx:474-503']
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Web Filter Rail Wireframe

This wireframe shows the panel a reader uses to narrow what the dashboard counts. It lists every control in the order the reader meets it, from search to the switches. The same panel opens as a sheet on a small screen.

## What the diagram shows

- The rail starts with search, saved views and the date range `web/src/FilterRail.tsx:298-332`.
- The saved views are fixed patches plus a top model view when one exists `web/src/FilterRail.tsx:145-173`.
- The range presets run from today to all days `web/src/FilterRail.tsx:56-56`.
- Facet groups for cost state, outcome, clients, models and projects follow, with less recent entries folded away `web/src/FilterRail.tsx:335-335` `web/src/FilterRail.tsx:407-407`.
- Three switches, the reset button and the list of undetected sources close the rail `web/src/FilterRail.tsx:432-450` `web/src/FilterRail.tsx:454-454`.
- The same content renders in a sheet from the left with its own title `web/src/FilterRail.tsx:486-503`.

## Capability and related functionality

The rail is part of [[App Screen]]. The query it edits is drawn in [[Web Concept Map]], and the saved views and switches map to the report filters described in [[Web Workflows]].

## Web Filter Rail Wireframe

![[docs/brain/architecture/rendered/drawio-web-filter-rail.svg]]

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/FilterRail.tsx:298-332` | The rail starts with search, saved views and the date range |
> | `web/src/FilterRail.tsx:145-173` | The saved views are fixed patches plus a top model view when one exists |
> | `web/src/FilterRail.tsx:56-56` | The range presets run from today to all days |
> | `web/src/FilterRail.tsx:335-335` | Facet groups for cost state, outcome, clients, models and projects follow, with less recent entries folded away |
> | `web/src/FilterRail.tsx:407-407` | Facet groups for cost state, outcome, clients, models and projects follow, with less recent entries folded away |
> | `web/src/FilterRail.tsx:432-450` | Three switches, the reset button and the list of undetected sources close the rail |
> | `web/src/FilterRail.tsx:454-454` | Three switches, the reset button and the list of undetected sources close the rail |
> | `web/src/FilterRail.tsx:486-503` | The same content renders in a sheet from the left with its own title |


## Filter rail: docked aside, or Filters sheet on narrow screens

![[docs/brain/architecture/rendered/drawio-web-filter-rail-filter-rail-docked-aside-or-filters-sheet-on-narrow-screens.svg]]


## Other

![[docs/brain/architecture/rendered/drawio-web-filter-rail-other.svg]]
