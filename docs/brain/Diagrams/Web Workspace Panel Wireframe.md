---
title: Web Workspace Panel Wireframe
aliases: []
tags: [diagram, drawio, wireframe]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
sources: [docs/brain/architecture/drawio/drawio-web-workspace-panel.drawio]
chunk: ch-localtokenomics-web-src
authored: true
node_citations:
  drawio-web-workspace-panel:
    'ws': ['web/src/SessionWorkspace.tsx:433-445']
    'w-handle': ['web/src/SessionWorkspace.tsx:433-445']
    'w-eyebrow': ['web/src/SessionWorkspace.tsx:433-445']
    'w-full': ['web/src/SessionWorkspace.tsx:433-445']
    'w-close': ['web/src/SessionWorkspace.tsx:433-445']
    'w-name': ['web/src/SessionWorkspace.tsx:433-445']
    'w-outcome': ['web/src/SessionWorkspace.tsx:433-445']
    'w-t1': ['web/src/SessionWorkspace.tsx:433-445']
    'w-t2': ['web/src/SessionWorkspace.tsx:433-445']
    'w-t3': ['web/src/SessionWorkspace.tsx:433-445']
    'w-t4': ['web/src/SessionWorkspace.tsx:433-445']
    'w-body': ['web/src/SessionWorkspace.tsx:433-445']
---

# Web Workspace Panel Wireframe

This wireframe shows the panel that opens beside the views when a reader picks a session. It shows the header, the rating form, the four tabs and the area they fill. On a small screen the same panel opens as a sheet.

## What the diagram shows

- The header shows the eyebrow, the name and the subtitle, with fullscreen and close buttons when docked `web/src/SessionWorkspace.tsx:500-511` `web/src/SessionWorkspace.tsx:521-521` `web/src/SessionWorkspace.tsx:527-527`.
- The outcome control sits under the header `web/src/SessionWorkspace.tsx:533-533`.
- The tab list carries Summary, Trace, Economics and Context `web/src/SessionWorkspace.tsx:541-551`.
- Docked, the panel is an aside with a resize handle; otherwise it is a sheet from the right `web/src/SessionWorkspace.tsx:600-624`.

## Capability and related functionality

The panel is [[Session Workspace Screen]], its tab states are in [[Web Workspace State Chart]], and it opens from [[Sessions Screen]].

## Web Workspace Panel Wireframe

![[docs/brain/architecture/rendered/drawio-web-workspace-panel.svg]]

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/SessionWorkspace.tsx:500-511` | The header shows the eyebrow, the name and the subtitle, with fullscreen and close buttons when docked |
> | `web/src/SessionWorkspace.tsx:521-521` | The header shows the eyebrow, the name and the subtitle, with fullscreen and close buttons when docked |
> | `web/src/SessionWorkspace.tsx:527-527` | The header shows the eyebrow, the name and the subtitle, with fullscreen and close buttons when docked |
> | `web/src/SessionWorkspace.tsx:533-533` | The outcome control sits under the header |
> | `web/src/SessionWorkspace.tsx:541-551` | The tab list carries Summary, Trace, Economics and Context |
> | `web/src/SessionWorkspace.tsx:600-624` | Docked, the panel is an aside with a resize handle; otherwise it is a sheet from the right |
