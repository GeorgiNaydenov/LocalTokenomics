---
title: UC-04 Check a change before merge Use Case Diagram
aliases: []
tags: [diagram, mermaid, use-case-diagram]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: []
sources: [docs/brain/architecture/diagrams/use-case-uc-04.mmd]
node_citations:
  use-case-uc-04:
    UC-04 Check a change before merge: ['.github/workflows/python.yml:6', '.github/workflows/python.yml:54',
      '.github/workflows/web.yml:46']
use-cases: [UC-04]
---

# UC-04 Check a change before merge Use Case Diagram

The actors that take part in UC-04 Check a change before merge, drawn from the specification.

## Use case diagram

%% generated:diagram-use-case-uc-04 start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    a1["GitHub workflow runner"]:::person
    uc_04(["UC-04 Check a change before merge"]):::system
    a1 --> uc_04
    subgraph Legend
        direction LR
        zlegend_a["Actor: a person or system that takes part"]:::person
        zlegend_b(["Use case: a goal the application serves"]):::system
        zlegend_a ~~~ zlegend_b
    end
    classDef person fill:#fff2cc,stroke:#d6b656,color:#142233
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-use-case-uc-04 end %%

%% generated:node-citations-use-case-uc-04 start (do not edit; run brain docs generate) %%
### Node citations

- UC-04 Check a change before merge: `.github/workflows/python.yml:6`, `.github/workflows/python.yml:54`, `.github/workflows/web.yml:46`
%% generated:node-citations-use-case-uc-04 end %%
