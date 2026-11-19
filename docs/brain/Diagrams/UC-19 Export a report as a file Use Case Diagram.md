---
title: UC-19 Export a report as a file Use Case Diagram
aliases: []
tags: [diagram, mermaid, use-case-diagram]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: []
sources: [docs/brain/architecture/diagrams/use-case-uc-19.mmd]
node_citations:
  use-case-uc-19:
    UC-19 Export a report as a file: ['src/ai_usage_cost/cli.py:176', 'src/ai_usage_cost/cli.py:185',
      'src/ai_usage_cost/cli.py:188']
use-cases: [UC-19]
---

# UC-19 Export a report as a file Use Case Diagram

The actors that take part in UC-19 Export a report as a file, drawn from the specification.

## Use case diagram

%% generated:diagram-use-case-uc-19 start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    a1["Person using the tool"]:::person
    uc_19(["UC-19 Export a report as a file"]):::system
    a1 --> uc_19
    subgraph Legend
        direction LR
        zlegend_a["Actor: a person or system that takes part"]:::person
        zlegend_b(["Use case: a goal the application serves"]):::system
        zlegend_a ~~~ zlegend_b
    end
    classDef person fill:#fff2cc,stroke:#d6b656,color:#142233
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-use-case-uc-19 end %%

%% generated:node-citations-use-case-uc-19 start (do not edit; run brain docs generate) %%
### Node citations

- UC-19 Export a report as a file: `src/ai_usage_cost/cli.py:176`, `src/ai_usage_cost/cli.py:185`, `src/ai_usage_cost/cli.py:188`
%% generated:node-citations-use-case-uc-19 end %%
