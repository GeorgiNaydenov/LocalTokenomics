---
title: UC-16 Export a usage and cost chart as a PNG image Use Case Diagram
aliases: []
tags: [diagram, mermaid, use-case-diagram]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: []
sources: [docs/brain/architecture/diagrams/use-case-uc-16.mmd]
node_citations:
  use-case-uc-16:
    UC-16 Export a usage and cost chart as a PNG image: ['src/ai_usage_cost/cli.py:186',
      'src/ai_usage_cost/cli.py:192', 'src/ai_usage_cost/render/png.py:26']
use-cases: [UC-16]
---

# UC-16 Export a usage and cost chart as a PNG image Use Case Diagram

The actors that take part in UC-16 Export a usage and cost chart as a PNG image, drawn from the specification.

## Use case diagram

%% generated:diagram-use-case-uc-16 start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    a1["CLI user"]:::person
    uc_16(["UC-16 Export a usage and cost chart as a PNG image"]):::system
    a1 --> uc_16
    subgraph Legend
        direction LR
        zlegend_a["Actor: a person or system that takes part"]:::person
        zlegend_b(["Use case: a goal the application serves"]):::system
        zlegend_a ~~~ zlegend_b
    end
    classDef person fill:#fff2cc,stroke:#d6b656,color:#142233
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-use-case-uc-16 end %%

%% generated:node-citations-use-case-uc-16 start (do not edit; run brain docs generate) %%
### Node citations

- UC-16 Export a usage and cost chart as a PNG image: `src/ai_usage_cost/cli.py:186`, `src/ai_usage_cost/cli.py:192`, `src/ai_usage_cost/render/png.py:26`
%% generated:node-citations-use-case-uc-16 end %%
