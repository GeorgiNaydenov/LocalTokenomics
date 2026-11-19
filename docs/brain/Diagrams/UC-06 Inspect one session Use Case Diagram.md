---
title: UC-06 Inspect one session Use Case Diagram
aliases: []
tags: [diagram, mermaid, use-case-diagram]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: []
sources: [docs/brain/architecture/diagrams/use-case-uc-06.mmd]
node_citations:
  use-case-uc-06:
    UC-06 Inspect one session: ['web/src/App.tsx:287', 'web/src/SessionWorkspace.tsx:471',
      'web/src/SessionWorkspace.tsx:472']
use-cases: [UC-06]
---

# UC-06 Inspect one session Use Case Diagram

The actors that take part in UC-06 Inspect one session, drawn from the specification.

## Use case diagram

%% generated:diagram-use-case-uc-06 start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    a1["Dashboard reader"]:::person
    uc_06(["UC-06 Inspect one session"]):::system
    a1 --> uc_06
    subgraph Legend
        direction LR
        zlegend_a["Actor: a person or system that takes part"]:::person
        zlegend_b(["Use case: a goal the application serves"]):::system
        zlegend_a ~~~ zlegend_b
    end
    classDef person fill:#fff2cc,stroke:#d6b656,color:#142233
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-use-case-uc-06 end %%

%% generated:node-citations-use-case-uc-06 start (do not edit; run brain docs generate) %%
### Node citations

- UC-06 Inspect one session: `web/src/App.tsx:287`, `web/src/SessionWorkspace.tsx:471`, `web/src/SessionWorkspace.tsx:472`
%% generated:node-citations-use-case-uc-06 end %%
