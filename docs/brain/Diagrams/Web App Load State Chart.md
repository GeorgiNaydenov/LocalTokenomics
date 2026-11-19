---
title: Web App Load State Chart
aliases: []
tags: [diagram, mermaid, state-chart]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
sources: [docs/brain/architecture/diagrams/web-app-loading.mmd]
chunk: ch-localtokenomics-web-src
authored: true
node_citations:
  web-app-loading:
    'Loading': ['web/src/App.tsx:263-269']
    'Offline': ['web/src/App.tsx:253-256']
    'ErrorCard': ['web/src/App.tsx:271-274']
    'Ready': ['web/src/App.tsx:290-328']
    'Refetching': ['web/src/App.tsx:203-203']
    'Rescanning': ['web/src/App.tsx:211-222']
---

# Web App Load State Chart

This chart shows what the reader sees while the dashboard starts, refreshes and fails. It explains why the whole page can turn into an error card and how it comes back. It matters because every view depends on these states.

## What the diagram shows

- The page starts in a loading state that ends when the first report has settled `web/src/App.tsx:139-139` `web/src/App.tsx:195-198`.
- A failure whose text says the server cannot be reached shows the offline card, and its retry reloads the metadata `web/src/App.tsx:251-259` `web/src/api.ts:493-494`.
- Any other error shows the error card `web/src/App.tsx:271-271`.
- A query change starts a new report request, and the count line dims while it runs `web/src/App.tsx:186-201` `web/src/App.tsx:203-203`.
- A rescan runs on the button and every five minutes while the page is visible, and a successful one reloads the metadata and clears the error `web/src/App.tsx:211-222` `web/src/App.tsx:226-243` `web/src/App.tsx:172-172`.

## Capability and related functionality

The states belong to [[App Screen]]. The failures are traced further in [[Web Error Flow]], and the session level states are in [[Web Workspace State Chart]].

## Web App Load State Chart

%% generated:diagram-web-app-loading start (do not edit; run brain docs generate) %%
```mermaid
stateDiagram-v2
    direction LR
    [*] --> Loading: page opens
    Loading --> Offline: meta or rates cannot reach the server
    Loading --> ErrorCard: meta or rates fail otherwise
    Loading --> Ready: first report settles
    Ready --> Refetching: query changes
    Refetching --> Ready: report settles
    Refetching --> ErrorCard: report request fails
    Ready --> Rescanning: Rescan logs or five minute timer
    Rescanning --> Ready: refresh done, meta reloaded
    Rescanning --> Offline: refresh cannot reach the server
    Offline --> Ready: Retry and meta loads
    ErrorCard --> Ready: next timed rescan succeeds
    note right of ErrorCard
        Not handled: the card has no retry button, and one failed refetch hides the whole dashboard.
    end note
    note left of Loading
        Legend: the filled dot starts, a rounded box is a UI state, an arrow is labelled with the event or condition in the code, a note marks a gap.
    end note
```
%% generated:diagram-web-app-loading end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/App.tsx:139-139` | The page starts in a loading state that ends when the first report has settled |
> | `web/src/App.tsx:195-198` | The page starts in a loading state that ends when the first report has settled |
> | `web/src/App.tsx:251-259` | A failure whose text says the server cannot be reached shows the offline card, and its retry reloads the metadata |
> | `web/src/api.ts:493-494` | A failure whose text says the server cannot be reached shows the offline card, and its retry reloads the metadata |
> | `web/src/App.tsx:271-271` | Any other error shows the error card |
> | `web/src/App.tsx:186-201` | A query change starts a new report request, and the count line dims while it runs |
> | `web/src/App.tsx:203-203` | A query change starts a new report request, and the count line dims while it runs |
> | `web/src/App.tsx:211-222` | A rescan runs on the button and every five minutes while the page is visible, and a successful one reloads the metadata and clears the error |
> | `web/src/App.tsx:226-243` | A rescan runs on the button and every five minutes while the page is visible, and a successful one reloads the metadata and clears the error |
> | `web/src/App.tsx:172-172` | A rescan runs on the button and every five minutes while the page is visible, and a successful one reloads the metadata and clears the error |
