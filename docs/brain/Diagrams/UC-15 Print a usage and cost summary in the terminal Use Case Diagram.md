---
title: UC-15 Print a usage and cost summary in the terminal Use Case Diagram
aliases: []
tags: [diagram, mermaid, use-case-diagram]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: []
sources: [docs/brain/architecture/diagrams/use-case-uc-15.mmd]
node_citations:
  use-case-uc-15:
    UC-15 Print a usage and cost summary in the terminal: ['src/ai_usage_cost/cli.py:105',
      'src/ai_usage_cost/render/terminal.py:20', 'src/ai_usage_cost/render/terminal.py:29']
use-cases: [UC-15]
---

# UC-15 Print a usage and cost summary in the terminal Use Case Diagram

The actors that take part in UC-15 Print a usage and cost summary in the terminal, drawn from the specification.

## Use case diagram

%% generated:diagram-use-case-uc-15 start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    a1["CLI user"]:::person
    uc_15(["UC-15 Print a usage and cost summary in the terminal"]):::system
    a1 --> uc_15
    subgraph Legend
        direction LR
        zlegend_a["Actor: a person or system that takes part"]:::person
        zlegend_b(["Use case: a goal the application serves"]):::system
        zlegend_a ~~~ zlegend_b
    end
    classDef person fill:#fff2cc,stroke:#d6b656,color:#142233
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-use-case-uc-15 end %%

%% generated:node-citations-use-case-uc-15 start (do not edit; run brain docs generate) %%
### Node citations

- UC-15 Print a usage and cost summary in the terminal: `src/ai_usage_cost/cli.py:105`, `src/ai_usage_cost/render/terminal.py:20`, `src/ai_usage_cost/render/terminal.py:29`
%% generated:node-citations-use-case-uc-15 end %%
