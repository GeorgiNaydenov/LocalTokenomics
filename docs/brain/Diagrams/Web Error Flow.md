---
title: Web Error Flow
aliases: []
tags: [diagram, mermaid, error-flow]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
sources: [docs/brain/architecture/diagrams/web-failures.mmd]
chunk: ch-localtokenomics-web-src
authored: true
node_citations:
  web-failures:
    req: ['web/src/api.ts:489-489']
    net: ['web/src/api.ts:491-493']
    unreach: ['web/src/api.ts:494-494']
    ok: ['web/src/api.ts:496-496']
    status: ['web/src/api.ts:497-497']
    json: ['web/src/api.ts:499-499']
    abort: ['web/src/App.tsx:176-176']
    drop: ['web/src/App.tsx:176-176']
    shell: ['web/src/App.tsx:251-251']
    offline: ['web/src/App.tsx:255-259']
    errcard: ['web/src/App.tsx:274-274']
    tab: ['web/src/SessionWorkspace.tsx:389-390']
    save: ['web/src/SessionWorkspace.tsx:298-298']
    'off': ['web/src/TraceTab.tsx:796-796']
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Web Error Flow

This flow shows how a failed request reaches the reader and where it is caught. Every request goes through one helper, so all failures start in the same two shapes. The flow also shows where a failure hides the whole dashboard and where it only touches one panel.

## What the diagram shows

- Every request goes through one helper that turns a thrown fetch into an unreachable error and a non 2xx answer into a status error `web/src/api.ts:489-499`.
- An aborted request also throws inside fetch, and every caller checks the abort signal before showing anything `web/src/App.tsx:176-176` `web/src/SessionWorkspace.tsx:104-104`.
- The shell shows the offline card when the error text names the unreachable server, and the error card otherwise `web/src/App.tsx:251-259` `web/src/App.tsx:271-271`.
- A workspace tab shows the error text in its placeholder `web/src/SessionWorkspace.tsx:389-390`.
- A failed outcome save shows its error in the status line `web/src/SessionWorkspace.tsx:287-287` `web/src/SessionWorkspace.tsx:298-298`.
- A 404 on span text marks the text off instead of failed `web/src/TraceTab.tsx:59-61` `web/src/TraceTab.tsx:796-796`.

## Capability and related functionality

The shell states are in [[Web App Load State Chart]], the tab states in [[Web Workspace State Chart]] and the span text states in [[Web Trace State Chart]]. The risks these gaps create are recorded in [[Web Specification]].

## Web Error Flow

%% generated:diagram-web-failures start (do not edit; run brain docs generate) %%
```mermaid
flowchart TD
    req["Request through getJson"]:::step --> net{"fetch throws?"}:::guard
    net -->|network error or abort| unreach["ApiError: could not reach the server"]:::step
    net -->|response| ok{"response ok?"}:::guard
    ok -->|status not 2xx| status["ApiError: path responded status"]:::step
    ok -->|2xx| json["JSON parsed"]:::step
    unreach --> abort{"signal aborted?"}:::guard
    status --> abort
    abort -->|yes| drop["Ignored silently"]:::step
    abort -->|no, shell request| shell{"text says could not reach?"}:::guard
    shell -->|yes| offline(["Offline card with retry"]):::fail
    shell -->|no| errcard(["Full page error card, no retry"]):::fail
    abort -->|no, workspace tab| tab(["Tab placeholder with error text"]):::fail
    abort -->|no, outcome save| save(["Status line shows save error"]):::fail
    status -->|404 on span text| off(["Span text marked off"]):::fail
    subgraph Legend
        direction LR
        zl1["Step"]:::step
        zl2{"Guard or check"}:::guard
        zl3(["Failure the reader sees"]):::fail
        zl4["Arrow label: the error it carries"]:::step
    end
    classDef step fill:#dae8fc,stroke:#222222,color:#142233
    classDef guard fill:#e1d5e7,stroke:#222222,color:#222222
    classDef fail fill:#f8cecc,stroke:#222222,color:#222222
```
%% generated:diagram-web-failures end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/api.ts:489-499` | Every request goes through one helper that turns a thrown fetch into an unreachable error and a non 2xx answer into a status error |
> | `web/src/App.tsx:176-176` | An aborted request also throws inside fetch, and every caller checks the abort signal before showing anything |
> | `web/src/SessionWorkspace.tsx:104-104` | An aborted request also throws inside fetch, and every caller checks the abort signal before showing anything |
> | `web/src/App.tsx:251-259` | The shell shows the offline card when the error text names the unreachable server, and the error card otherwise |
> | `web/src/App.tsx:271-271` | The shell shows the offline card when the error text names the unreachable server, and the error card otherwise |
> | `web/src/SessionWorkspace.tsx:389-390` | A workspace tab shows the error text in its placeholder |
> | `web/src/SessionWorkspace.tsx:287-287` | A failed outcome save shows its error in the status line |
> | `web/src/SessionWorkspace.tsx:298-298` | A failed outcome save shows its error in the status line |
> | `web/src/TraceTab.tsx:59-61` | A 404 on span text marks the text off instead of failed |
> | `web/src/TraceTab.tsx:796-796` | A 404 on span text marks the text off instead of failed |
