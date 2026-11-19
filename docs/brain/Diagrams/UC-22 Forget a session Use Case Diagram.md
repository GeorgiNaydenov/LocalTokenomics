---
title: UC-22 Forget a session Use Case Diagram
aliases: []
tags: [diagram, mermaid, use-case-diagram]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: []
sources: [docs/brain/architecture/diagrams/use-case-uc-22.mmd]
node_citations:
  use-case-uc-22:
    UC-22 Forget a session: ['src/ai_usage_cost/api.py:362', 'src/ai_usage_cost/store.py:597',
      'src/ai_usage_cost/store.py:601']
use-cases: [UC-22]
---

# UC-22 Forget a session Use Case Diagram

The actors that take part in UC-22 Forget a session, drawn from the specification.

## Use case diagram

%% generated:diagram-use-case-uc-22 start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    a1["Person using the tool"]:::person
    uc_22(["UC-22 Forget a session"]):::system
    a1 --> uc_22
    subgraph Legend
        direction LR
        zlegend_a["Actor: a person or system that takes part"]:::person
        zlegend_b(["Use case: a goal the application serves"]):::system
        zlegend_a ~~~ zlegend_b
    end
    classDef person fill:#fff2cc,stroke:#d6b656,color:#142233
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-use-case-uc-22 end %%

%% generated:node-citations-use-case-uc-22 start (do not edit; run brain docs generate) %%
### Node citations

- UC-22 Forget a session: `src/ai_usage_cost/api.py:362`, `src/ai_usage_cost/store.py:597`, `src/ai_usage_cost/store.py:601`
%% generated:node-citations-use-case-uc-22 end %%
