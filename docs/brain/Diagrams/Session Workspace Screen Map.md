---
title: Session Workspace Screen Map
aliases: []
tags: [diagram, drawio, screen-map]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
sources: [docs/brain/architecture/drawio/drawio-screen-session-workspace.drawio, docs/brain/architecture/drawio/drawio-screen-session-workspace-header.drawio,
  docs/brain/architecture/drawio/drawio-screen-session-workspace-outcome.drawio, docs/brain/architecture/drawio/drawio-screen-session-workspace-tabs.drawio,
  docs/brain/architecture/drawio/drawio-screen-session-workspace-panel.drawio, docs/brain/architecture/drawio/drawio-screen-session-workspace-other.drawio]
chunk: ch-localtokenomics-web-src
authored: true
screen-note: Session Workspace Screen
node_citations:
  drawio-screen-session-workspace:
    el-1: ['web/src/SessionWorkspace.tsx:502-502']
    el-2: ['web/src/SessionWorkspace.tsx:518-523']
    el-3: ['web/src/SessionWorkspace.tsx:527-527']
    el-4: ['web/src/SessionWorkspace.tsx:306-312']
    el-5: ['web/src/SessionWorkspace.tsx:321-321']
    el-6: ['web/src/SessionWorkspace.tsx:330-330']
    el-7: ['web/src/SessionWorkspace.tsx:333-333']
    el-8: ['web/src/SessionWorkspace.tsx:342-346']
    el-9: ['web/src/SessionWorkspace.tsx:352-356']
    el-10: ['web/src/SessionWorkspace.tsx:547-547']
    el-11: ['web/src/SessionWorkspace.tsx:555-555']
    el-12: ['web/src/SessionWorkspace.tsx:134-134']
    el-13: ['web/src/SessionWorkspace.tsx:387-387']
    el-14: ['web/src/SessionWorkspace.tsx:389-389']
    el-15: ['web/src/SessionWorkspace.tsx:613-613']
    el-16: ['web/src/SessionWorkspace.tsx:620-620']
    badge-1: ['web/src/SessionWorkspace.tsx:502-502']
    badge-2: ['web/src/SessionWorkspace.tsx:518-523']
    badge-3: ['web/src/SessionWorkspace.tsx:527-527']
    badge-4: ['web/src/SessionWorkspace.tsx:306-312']
    badge-5: ['web/src/SessionWorkspace.tsx:321-321']
    badge-6: ['web/src/SessionWorkspace.tsx:330-330']
    badge-7: ['web/src/SessionWorkspace.tsx:333-333']
    badge-8: ['web/src/SessionWorkspace.tsx:342-346']
    badge-9: ['web/src/SessionWorkspace.tsx:352-356']
    badge-10: ['web/src/SessionWorkspace.tsx:547-547']
    badge-11: ['web/src/SessionWorkspace.tsx:555-555']
    badge-12: ['web/src/SessionWorkspace.tsx:134-134']
    badge-13: ['web/src/SessionWorkspace.tsx:387-387']
    badge-14: ['web/src/SessionWorkspace.tsx:389-389']
    badge-15: ['web/src/SessionWorkspace.tsx:613-613']
    badge-16: ['web/src/SessionWorkspace.tsx:620-620']
    region-1: ['web/src/SessionWorkspace.tsx:502-502', 'web/src/SessionWorkspace.tsx:518-523',
      'web/src/SessionWorkspace.tsx:527-527']
    region-2: ['web/src/SessionWorkspace.tsx:306-312', 'web/src/SessionWorkspace.tsx:321-321',
      'web/src/SessionWorkspace.tsx:330-330', 'web/src/SessionWorkspace.tsx:333-333',
      'web/src/SessionWorkspace.tsx:342-346', 'web/src/SessionWorkspace.tsx:352-356']
    region-3: ['web/src/SessionWorkspace.tsx:134-134', 'web/src/SessionWorkspace.tsx:387-387',
      'web/src/SessionWorkspace.tsx:389-389', 'web/src/SessionWorkspace.tsx:547-547',
      'web/src/SessionWorkspace.tsx:555-555']
    region-4: ['web/src/SessionWorkspace.tsx:613-613', 'web/src/SessionWorkspace.tsx:620-620']
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Session Workspace Screen Map

This map shows the panel a reader works in once they open one session. It lets them rate the outcome, keep notes and move between the four views of that session. It also shows how each tab waits for its data and what it shows when the server does not answer.

## What the diagram shows

- The header shows the session name and subtitle, and in docked mode the fullscreen and close buttons `web/src/SessionWorkspace.tsx:497-532`.
- Under it sits the outcome control: a toggle group, an info glyph, the notes and tags button, a status line and the two fields `web/src/SessionWorkspace.tsx:303-362`.
- Four tabs follow; only the tabs the reader has opened fetch their data `web/src/SessionWorkspace.tsx:447` `web/src/SessionWorkspace.tsx:471-474` `web/src/SessionWorkspace.tsx:536-596`.
- A loading or failed tab shows a placeholder through one shared wrapper `web/src/SessionWorkspace.tsx:379-394`.
- Docked, the panel is an aside with a resize handle; otherwise it is a sheet `web/src/SessionWorkspace.tsx:600-625`.

## Capability and related functionality

The workspace is opened from [[Sessions Screen]] and hosts [[Trace Tab Screen]], [[Economics Tab Screen]] and [[Context Tab Screen]]. Its loading states are drawn in [[Web Workspace State Chart]] and the outcome form in [[Web Outcome Form Wireframe]]. Rating a session is a use case in [[Web Specification]].

## Session Workspace Screen screen map

![[docs/brain/architecture/rendered/drawio-screen-session-workspace.svg]]

> [!example]- Code references
> | Badge | Element | Code |
> |---|---|---|
> | 1 | `<h2` session name | `web/src/SessionWorkspace.tsx:502-502` |
> | 2 | `<Button` Fullscreen | `web/src/SessionWorkspace.tsx:518-523` |
> | 3 | `<Button` Close session | `web/src/SessionWorkspace.tsx:527-527` |
> | 4 | `<ToggleGroup` successful, partial, failed, abandoned, unrated | `web/src/SessionWorkspace.tsx:306-312` |
> | 5 | `<MetricInfo` rating meanings | `web/src/SessionWorkspace.tsx:321-321` |
> | 6 | `<Button` Notes and tags | `web/src/SessionWorkspace.tsx:330-330` |
> | 7 | `<span` status | `web/src/SessionWorkspace.tsx:333-333` |
> | 8 | `<Textarea` Notes | `web/src/SessionWorkspace.tsx:342-346` |
> | 9 | `<Input` Tags, comma separated | `web/src/SessionWorkspace.tsx:352-356` |
> | 10 | `<TabsTrigger` Summary, Trace, Economics, Context | `web/src/SessionWorkspace.tsx:547-547` |
> | 11 | `<SummaryTab` Summary | `web/src/SessionWorkspace.tsx:555-555` |
> | 12 | `if (!tokens) {` empty section | `web/src/SessionWorkspace.tsx:134-134` |
> | 13 | `case 'loading':` loading section | `web/src/SessionWorkspace.tsx:387-387` |
> | 14 | `case 'error':` error section | `web/src/SessionWorkspace.tsx:389-389` |
> | 15 | `<ResizeHandle` resize | `web/src/SessionWorkspace.tsx:613-613` |
> | 16 | `<Sheet` workspace sheet | `web/src/SessionWorkspace.tsx:620-620` |


## header

![[docs/brain/architecture/rendered/drawio-screen-session-workspace-header.svg]]


## outcome

![[docs/brain/architecture/rendered/drawio-screen-session-workspace-outcome.svg]]


## tabs

![[docs/brain/architecture/rendered/drawio-screen-session-workspace-tabs.svg]]


## panel

![[docs/brain/architecture/rendered/drawio-screen-session-workspace-panel.svg]]


## Other

![[docs/brain/architecture/rendered/drawio-screen-session-workspace-other.svg]]
