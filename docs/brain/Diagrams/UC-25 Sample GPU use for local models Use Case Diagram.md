---
title: UC-25 Sample GPU use for local models Use Case Diagram
aliases: []
tags: [diagram, mermaid, use-case-diagram]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: []
sources: [docs/brain/architecture/diagrams/use-case-uc-25.mmd]
node_citations:
  use-case-uc-25:
    UC-25 Sample GPU use for local models: ['src/ai_usage_cost/cli.py:200', 'src/ai_usage_cost/collect.py:85',
      'src/ai_usage_cost/collect.py:275']
use-cases: [UC-25]
---

# UC-25 Sample GPU use for local models Use Case Diagram

The actors that take part in UC-25 Sample GPU use for local models, drawn from the specification.

## Use case diagram

%% generated:diagram-use-case-uc-25 start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    a1["Person using the tool"]:::person
    uc_25(["UC-25 Sample GPU use for local models"]):::system
    a1 --> uc_25
    subgraph Legend
        direction LR
        zlegend_a["Actor: a person or system that takes part"]:::person
        zlegend_b(["Use case: a goal the application serves"]):::system
        zlegend_a ~~~ zlegend_b
    end
    classDef person fill:#fff2cc,stroke:#d6b656,color:#142233
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-use-case-uc-25 end %%

%% generated:node-citations-use-case-uc-25 start (do not edit; run brain docs generate) %%
### Node citations

- UC-25 Sample GPU use for local models: `src/ai_usage_cost/cli.py:200`, `src/ai_usage_cost/collect.py:85`, `src/ai_usage_cost/collect.py:275`
%% generated:node-citations-use-case-uc-25 end %%
