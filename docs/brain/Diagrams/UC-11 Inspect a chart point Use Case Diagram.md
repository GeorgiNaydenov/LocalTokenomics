---
title: UC-11 Inspect a chart point Use Case Diagram
aliases: []
tags: [diagram, mermaid, use-case-diagram]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: []
sources: [docs/brain/architecture/diagrams/use-case-uc-11.mmd]
node_citations:
  use-case-uc-11:
    UC-11 Inspect a chart point: ['web/src/components/chart-hover.tsx:43', 'web/src/components/chart-hover.tsx:63',
      'web/src/components/chart-hover.tsx:91']
use-cases: [UC-11]
---

# UC-11 Inspect a chart point Use Case Diagram

The actors that take part in UC-11 Inspect a chart point, drawn from the specification.

## Use case diagram

%% generated:diagram-use-case-uc-11 start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    a1["Dashboard reader"]:::person
    uc_11(["UC-11 Inspect a chart point"]):::system
    a1 --> uc_11
    subgraph Legend
        direction LR
        zlegend_a["Actor: a person or system that takes part"]:::person
        zlegend_b(["Use case: a goal the application serves"]):::system
        zlegend_a ~~~ zlegend_b
    end
    classDef person fill:#fff2cc,stroke:#d6b656,color:#142233
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-use-case-uc-11 end %%

%% generated:node-citations-use-case-uc-11 start (do not edit; run brain docs generate) %%
### Node citations

- UC-11 Inspect a chart point: `web/src/components/chart-hover.tsx:43`, `web/src/components/chart-hover.tsx:63`, `web/src/components/chart-hover.tsx:91`
%% generated:node-citations-use-case-uc-11 end %%
