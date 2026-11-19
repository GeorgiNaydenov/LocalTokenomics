---
title: UC-17 See what my AI usage would cost Use Case Diagram
aliases: []
tags: [diagram, mermaid, use-case-diagram]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: []
sources: [docs/brain/architecture/diagrams/use-case-uc-17.mmd]
node_citations:
  use-case-uc-17:
    UC-17 See what my AI usage would cost: ['src/ai_usage_cost/cli.py:72', 'src/ai_usage_cost/cli.py:87',
      'src/ai_usage_cost/pipeline.py:175']
use-cases: [UC-17]
---

# UC-17 See what my AI usage would cost Use Case Diagram

The actors that take part in UC-17 See what my AI usage would cost, drawn from the specification.

## Use case diagram

%% generated:diagram-use-case-uc-17 start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    a1["Person using the tool"]:::person
    a2["AI coding tool logs"]:::person
    uc_17(["UC-17 See what my AI usage would cost"]):::system
    a1 --> uc_17
    a2 --> uc_17
    subgraph Legend
        direction LR
        zlegend_a["Actor: a person or system that takes part"]:::person
        zlegend_b(["Use case: a goal the application serves"]):::system
        zlegend_a ~~~ zlegend_b
    end
    classDef person fill:#fff2cc,stroke:#d6b656,color:#142233
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-use-case-uc-17 end %%

%% generated:node-citations-use-case-uc-17 start (do not edit; run brain docs generate) %%
### Node citations

- UC-17 See what my AI usage would cost: `src/ai_usage_cost/cli.py:72`, `src/ai_usage_cost/cli.py:87`, `src/ai_usage_cost/pipeline.py:175`
%% generated:node-citations-use-case-uc-17 end %%
