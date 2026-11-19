---
title: UC-20 Be alerted when spend rises Use Case Diagram
aliases: []
tags: [diagram, mermaid, use-case-diagram]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: []
sources: [docs/brain/architecture/diagrams/use-case-uc-20.mmd]
node_citations:
  use-case-uc-20:
    UC-20 Be alerted when spend rises: ['src/ai_usage_cost/cli.py:299', 'src/ai_usage_cost/cli.py:323',
      'src/ai_usage_cost/cli.py:335']
use-cases: [UC-20]
---

# UC-20 Be alerted when spend rises Use Case Diagram

The actors that take part in UC-20 Be alerted when spend rises, drawn from the specification.

## Use case diagram

%% generated:diagram-use-case-uc-20 start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    a1["Person using the tool"]:::person
    a2["Notification target"]:::person
    uc_20(["UC-20 Be alerted when spend rises"]):::system
    a1 --> uc_20
    a2 --> uc_20
    subgraph Legend
        direction LR
        zlegend_a["Actor: a person or system that takes part"]:::person
        zlegend_b(["Use case: a goal the application serves"]):::system
        zlegend_a ~~~ zlegend_b
    end
    classDef person fill:#fff2cc,stroke:#d6b656,color:#142233
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-use-case-uc-20 end %%

%% generated:node-citations-use-case-uc-20 start (do not edit; run brain docs generate) %%
### Node citations

- UC-20 Be alerted when spend rises: `src/ai_usage_cost/cli.py:299`, `src/ai_usage_cost/cli.py:323`, `src/ai_usage_cost/cli.py:335`
%% generated:node-citations-use-case-uc-20 end %%
