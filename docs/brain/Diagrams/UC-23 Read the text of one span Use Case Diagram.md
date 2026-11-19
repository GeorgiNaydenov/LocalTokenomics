---
title: UC-23 Read the text of one span Use Case Diagram
aliases: []
tags: [diagram, mermaid, use-case-diagram]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: []
sources: [docs/brain/architecture/diagrams/use-case-uc-23.mmd]
node_citations:
  use-case-uc-23:
    UC-23 Read the text of one span: ['src/ai_usage_cost/api.py:374', 'src/ai_usage_cost/api.py:376',
      'src/ai_usage_cost/privacy.py:91']
use-cases: [UC-23]
---

# UC-23 Read the text of one span Use Case Diagram

The actors that take part in UC-23 Read the text of one span, drawn from the specification.

## Use case diagram

%% generated:diagram-use-case-uc-23 start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    a1["Person using the tool"]:::person
    uc_23(["UC-23 Read the text of one span"]):::system
    a1 --> uc_23
    subgraph Legend
        direction LR
        zlegend_a["Actor: a person or system that takes part"]:::person
        zlegend_b(["Use case: a goal the application serves"]):::system
        zlegend_a ~~~ zlegend_b
    end
    classDef person fill:#fff2cc,stroke:#d6b656,color:#142233
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-use-case-uc-23 end %%

%% generated:node-citations-use-case-uc-23 start (do not edit; run brain docs generate) %%
### Node citations

- UC-23 Read the text of one span: `src/ai_usage_cost/api.py:374`, `src/ai_usage_cost/api.py:376`, `src/ai_usage_cost/privacy.py:91`
%% generated:node-citations-use-case-uc-23 end %%
