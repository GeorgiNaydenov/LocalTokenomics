---
title: Context Tab Screen Map
aliases: []
tags: [diagram, drawio, screen-map]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
sources: [docs/brain/architecture/drawio/drawio-screen-context-tab.drawio]
chunk: ch-localtokenomics-web-src
authored: true
screen-note: Context Tab Screen
node_citations:
  drawio-screen-context-tab:
    el-1: ['web/src/ContextTab.tsx:164-164']
    el-2: ['web/src/ContextTab.tsx:192-192']
    el-3: ['web/src/ContextTab.tsx:199-199']
    el-4: ['web/src/ContextTab.tsx:74-74']
    el-5: ['web/src/ContextTab.tsx:42-42']
    el-6: ['web/src/ContextTab.tsx:115-115']
    el-7: ['web/src/ContextTab.tsx:135-139']
    el-8: ['web/src/ContextTab.tsx:149-149']
    el-9: ['web/src/ContextTab.tsx:216-220']
    badge-1: ['web/src/ContextTab.tsx:164-164']
    badge-2: ['web/src/ContextTab.tsx:192-192']
    badge-3: ['web/src/ContextTab.tsx:199-199']
    badge-4: ['web/src/ContextTab.tsx:74-74']
    badge-5: ['web/src/ContextTab.tsx:42-42']
    badge-6: ['web/src/ContextTab.tsx:115-115']
    badge-7: ['web/src/ContextTab.tsx:135-139']
    badge-8: ['web/src/ContextTab.tsx:149-149']
    badge-9: ['web/src/ContextTab.tsx:216-220']
    region-1: ['web/src/ContextTab.tsx:164-164']
    region-2: ['web/src/ContextTab.tsx:192-192', 'web/src/ContextTab.tsx:199-199']
    region-3: ['web/src/ContextTab.tsx:115-115', 'web/src/ContextTab.tsx:135-139',
      'web/src/ContextTab.tsx:149-149', 'web/src/ContextTab.tsx:42-42', 'web/src/ContextTab.tsx:74-74']
    region-4: ['web/src/ContextTab.tsx:216-220']
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Context Tab Screen Map

This map shows how a reader sees how full the model's context window got during one session. It lets them spot calls near the limit, see where the context was compacted and jump to the steps that added the most. It also shows what is drawn when a size is unknown.

## What the diagram shows

- An empty session shows one empty state and nothing else `web/src/ContextTab.tsx:164-171`.
- Otherwise the occupancy chart comes first, with a reader specific note for Claude Code `web/src/ContextTab.tsx:186-207`.
- Each call card shows input tokens, the change since the previous call, an occupancy meter, provenance badges and buttons for the spans that added context `web/src/ContextTab.tsx:81-155`.
- Cards are revealed in batches `web/src/ContextTab.tsx:14` `web/src/ContextTab.tsx:215-224`.

## Capability and related functionality

The tab lives inside [[Session Workspace Screen]], and its added span buttons focus [[Trace Tab Screen]]. Occupancy and provenance are explained in [[Web Glossary Map]].

## Context Tab Screen screen map

![[docs/brain/architecture/rendered/drawio-screen-context-tab.svg]]

> [!example]- Code references
> | Badge | Element | Code |
> |---|---|---|
> | 1 | `snapshots.length === 0` empty section | `web/src/ContextTab.tsx:164-164` |
> | 2 | `<ContextOccupancy` occupancy chart | `web/src/ContextTab.tsx:192-192` |
> | 3 | `props.source === 'claude-code'` info section | `web/src/ContextTab.tsx:199-199` |
> | 4 | `snapshot.compacted_before` info section | `web/src/ContextTab.tsx:74-74` |
> | 5 | `snapshot.occupancy === null` empty section | `web/src/ContextTab.tsx:42-42` |
> | 6 | `<ProvenanceBadge` capacity, occupancy, tokens | `web/src/ContextTab.tsx:115-115` |
> | 7 | `<Button` added span | `web/src/ContextTab.tsx:135-139` |
> | 8 | `snapshot.added_span_ids.length === 0` empty section | `web/src/ContextTab.tsx:149-149` |
> | 9 | `<Button` Show more calls | `web/src/ContextTab.tsx:216-220` |
