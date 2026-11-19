---
title: Web Rate Table Wireframe
aliases: []
tags: [diagram, drawio, wireframe]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
sources: [docs/brain/architecture/drawio/drawio-web-rate-table.drawio]
chunk: ch-localtokenomics-web-src
authored: true
node_citations:
  drawio-web-rate-table:
    panel: ['web/src/Pricing.tsx:308-332']
    r-title: ['web/src/Pricing.tsx:308-332']
    r-age: ['web/src/Pricing.tsx:308-332']
    r-table: ['web/src/Pricing.tsx:308-332']
    c1: ['web/src/Pricing.tsx:308-332']
    c2: ['web/src/Pricing.tsx:308-332']
    c3: ['web/src/Pricing.tsx:308-332']
    c4: ['web/src/Pricing.tsx:308-332']
    c5: ['web/src/Pricing.tsx:308-332']
    c6: ['web/src/Pricing.tsx:308-332']
    c7: ['web/src/Pricing.tsx:308-332']
    c8: ['web/src/Pricing.tsx:308-332']
    c9: ['web/src/Pricing.tsx:308-332']
    c10: ['web/src/Pricing.tsx:308-332']
    r-chev: ['web/src/Pricing.tsx:308-332']
    r-model: ['web/src/Pricing.tsx:308-332']
    r-est: ['web/src/Pricing.tsx:308-332']
    r-detail: ['web/src/Pricing.tsx:308-332']
    r-more: ['web/src/Pricing.tsx:308-332']
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Web Rate Table Wireframe

This wireframe shows the table of list prices the dashboard uses. It names every column and shows where a row opens its details. It helps a reader find why a model is priced the way it is.

## What the diagram shows

- The header names the date of the rates and shows an age badge when they are old `web/src/Pricing.tsx:337-350`.
- The columns run from model to spend here `web/src/Pricing.tsx:42-42`.
- The model cell holds the details chevron, the name, the tags, the match string and any estimated lines `web/src/Pricing.tsx:272-304`.
- An open row adds a detail row across all columns `web/src/Pricing.tsx:397-399`.
- Unused rates are hidden behind a show more button `web/src/Pricing.tsx:411-420`.

## Capability and related functionality

The table sits on [[Pricing Screen]]. The rate row state and cache price rules are in [[Web Specification]], and the estimated rate term is in [[Web Glossary Map]].

## Web Rate Table Wireframe

![[docs/brain/architecture/rendered/drawio-web-rate-table.svg]]

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/Pricing.tsx:337-350` | The header names the date of the rates and shows an age badge when they are old |
> | `web/src/Pricing.tsx:42-42` | The columns run from model to spend here |
> | `web/src/Pricing.tsx:272-304` | The model cell holds the details chevron, the name, the tags, the match string and any estimated lines |
> | `web/src/Pricing.tsx:397-399` | An open row adds a detail row across all columns |
> | `web/src/Pricing.tsx:411-420` | Unused rates are hidden behind a show more button |
