---
title: Web Trace State Chart
aliases: []
tags: [diagram, mermaid, state-chart]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
sources: [docs/brain/architecture/diagrams/web-trace-content.mmd]
chunk: ch-localtokenomics-web-src
authored: true
node_citations:
  web-trace-content:
    Closed: ['web/src/TraceTab.tsx:827-827']
    Loading: ['web/src/TraceTab.tsx:46-46']
    Shown: ['web/src/TraceTab.tsx:794-794']
    'Off': ['web/src/TraceTab.tsx:796-796']
    Failed: ['web/src/TraceTab.tsx:796-796']
    Hidden: ['web/src/TraceTab.tsx:789-789']
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Web Trace State Chart

This chart shows what happens when a reader opens the text of one step in a session trace. The text is fetched once and kept, so opening it again is instant. The chart also shows that a failed fetch is kept as well and is not tried again.

## What the diagram shows

- Text toggles the span open; the fetch runs only when nothing is stored for that span `web/src/TraceTab.tsx:786-791`.
- The state is set to loading, then to ready, off for a 404, or error `web/src/TraceTab.tsx:792-797`.
- A 404 is recognised by the text of the error message `web/src/TraceTab.tsx:59-61`.
- The content block is drawn only while the span is open and a state is stored `web/src/TraceTab.tsx:836-837`.

## Capability and related functionality

The chart belongs to [[Trace Tab Screen]]. The workspace level loading is in [[Web Workspace State Chart]], and the failures are collected in [[Web Error Flow]].

## Web Trace State Chart

%% generated:diagram-web-trace-content start (do not edit; run brain docs generate) %%
```mermaid
stateDiagram-v2
    direction LR
    [*] --> Closed: span row drawn
    Closed --> Loading: Text pressed, nothing stored yet
    Loading --> Shown: content arrives
    Loading --> Off: server answers 404
    Loading --> Failed: other error
    Shown --> Hidden: Hide pressed
    Hidden --> Shown: Text pressed, stored content reused
    Off --> Hidden: Hide pressed
    Failed --> Hidden: Hide pressed
    Hidden --> Failed: Text pressed, stored error reused
    note right of Failed
        Not handled: a stored error is never fetched again.
    end note
    note left of Closed
        Legend: the filled dot starts, a rounded box is the state of one span text, an arrow is labelled with its trigger, a note marks a gap.
    end note
```
%% generated:diagram-web-trace-content end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/TraceTab.tsx:786-791` | Text toggles the span open; the fetch runs only when nothing is stored for that span |
> | `web/src/TraceTab.tsx:792-797` | The state is set to loading, then to ready, off for a 404, or error |
> | `web/src/TraceTab.tsx:59-61` | A 404 is recognised by the text of the error message |
> | `web/src/TraceTab.tsx:836-837` | The content block is drawn only while the span is open and a state is stored |
