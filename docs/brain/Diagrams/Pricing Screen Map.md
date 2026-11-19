---
title: Pricing Screen Map
aliases: []
tags: [diagram, drawio, screen-map]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
sources: [docs/brain/architecture/drawio/drawio-screen-pricing.drawio]
chunk: ch-localtokenomics-web-src
authored: true
screen-note: Pricing Screen
node_citations:
  drawio-screen-pricing:
    el-1: ['web/src/Pricing.tsx:428-428']
    el-2: ['web/src/Pricing.tsx:342-342']
    el-3: ['web/src/Pricing.tsx:352-366']
    el-4: ['web/src/Pricing.tsx:277-279']
    el-5: ['web/src/Pricing.tsx:289-289']
    el-6: ['web/src/Pricing.tsx:401-401']
    el-7: ['web/src/Pricing.tsx:413-416']
    el-8: ['web/src/Pricing.tsx:492-492']
    el-9: ['web/src/Pricing.tsx:497-497']
    el-10: ['web/src/Pricing.tsx:543-543']
    el-11: ['web/src/Pricing.tsx:569-569']
    el-12: ['web/src/Pricing.tsx:597-597']
    badge-1: ['web/src/Pricing.tsx:428-428']
    badge-2: ['web/src/Pricing.tsx:342-342']
    badge-3: ['web/src/Pricing.tsx:352-366']
    badge-4: ['web/src/Pricing.tsx:277-279']
    badge-5: ['web/src/Pricing.tsx:289-289']
    badge-6: ['web/src/Pricing.tsx:401-401']
    badge-7: ['web/src/Pricing.tsx:413-416']
    badge-8: ['web/src/Pricing.tsx:492-492']
    badge-9: ['web/src/Pricing.tsx:497-497']
    badge-10: ['web/src/Pricing.tsx:543-543']
    badge-11: ['web/src/Pricing.tsx:569-569']
    badge-12: ['web/src/Pricing.tsx:597-597']
    region-1: ['web/src/Pricing.tsx:428-428']
    region-2: ['web/src/Pricing.tsx:277-279', 'web/src/Pricing.tsx:289-289', 'web/src/Pricing.tsx:342-342', 'web/src/Pricing.tsx:352-366', 'web/src/Pricing.tsx:401-401', 'web/src/Pricing.tsx:413-416']
    region-3: ['web/src/Pricing.tsx:492-492', 'web/src/Pricing.tsx:497-497']
    region-4: ['web/src/Pricing.tsx:543-543', 'web/src/Pricing.tsx:569-569', 'web/src/Pricing.tsx:597-597']
---

# Pricing Screen Map

This map shows where a reader checks the list prices the dashboard uses. It lets them see which models were priced exactly, which were estimated from a sibling and which have no price at all. It also shows how to fix a missing price.

## What the diagram shows

- The view stacks the estimated panel, the rate table and a grid of the multipliers and unpriced panels `web/src/Pricing.tsx:619-631`.
- The rate table lists priced or estimated rows first and reveals unused rows in batches `web/src/Pricing.tsx:327-331` `web/src/Pricing.tsx:411-421`.
- A row expands into a detail row through a chevron button `web/src/Pricing.tsx:277-286` `web/src/Pricing.tsx:397-405`.
- The unpriced panel offers a copyable rate row for the first unknown model `web/src/Pricing.tsx:545-548` `web/src/Pricing.tsx:591-599`.

## Capability and related functionality

The view is reached from the tab strip and the rate age notice of [[App Screen]]. The rate rules, such as cache price derivation and rate row state, are recorded in [[Web Specification]]. The terms are drawn in [[Web Glossary Map]].

## Pricing Screen screen map

![[docs/brain/architecture/rendered/drawio-screen-pricing.svg]]

> [!example]- Code references
> | Badge | Element | Code |
> |---|---|---|
> | 1 | `items.length === 0` empty section | `web/src/Pricing.tsx:428-428` |
> | 2 | `<Badge` rate age | `web/src/Pricing.tsx:342-342` |
> | 3 | `<Table` rates | `web/src/Pricing.tsx:352-366` |
> | 4 | `<button` details | `web/src/Pricing.tsx:277-279` |
> | 5 | `<TagBadge` tags | `web/src/Pricing.tsx:289-289` |
> | 6 | `<RowDetail` detail row | `web/src/Pricing.tsx:401-401` |
> | 7 | `<Button` Show more rates | `web/src/Pricing.tsx:413-416` |
> | 8 | `providersPresent.length === 0` empty section | `web/src/Pricing.tsx:492-492` |
> | 9 | `<ProviderMultipliers` per provider | `web/src/Pricing.tsx:497-497` |
> | 10 | `listed.length === 0 && unknown.length === 0 && idle.length === 0` empty section | `web/src/Pricing.tsx:543-543` |
> | 11 | `<UnpricedBadge` status | `web/src/Pricing.tsx:569-569` |
> | 12 | `<CodeBlock` rates.json snippet | `web/src/Pricing.tsx:597-597` |
