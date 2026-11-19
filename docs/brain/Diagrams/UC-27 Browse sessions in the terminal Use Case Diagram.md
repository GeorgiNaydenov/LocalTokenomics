---
title: UC-27 Browse sessions in the terminal Use Case Diagram
aliases: []
tags: [diagram, mermaid, use-case-diagram]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: []
sources: [docs/brain/architecture/diagrams/use-case-uc-27.mmd]
node_citations:
  use-case-uc-27:
    UC-27 Browse sessions in the terminal: ['src/ai_usage_cost/cli.py:358', 'src/ai_usage_cost/cli.py:371',
      'src/ai_usage_cost/tui.py:119']
use-cases: [UC-27]
---

# UC-27 Browse sessions in the terminal Use Case Diagram

The actors that take part in UC-27 Browse sessions in the terminal, drawn from the specification.

## Use case diagram

%% generated:diagram-use-case-uc-27 start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    a1["Person using the tool"]:::person
    uc_27(["UC-27 Browse sessions in the terminal"]):::system
    a1 --> uc_27
    subgraph Legend
        direction LR
        zlegend_a["Actor: a person or system that takes part"]:::person
        zlegend_b(["Use case: a goal the application serves"]):::system
        zlegend_a ~~~ zlegend_b
    end
    classDef person fill:#fff2cc,stroke:#d6b656,color:#142233
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
```
%% generated:diagram-use-case-uc-27 end %%

%% generated:node-citations-use-case-uc-27 start (do not edit; run brain docs generate) %%
### Node citations

- UC-27 Browse sessions in the terminal: `src/ai_usage_cost/cli.py:358`, `src/ai_usage_cost/cli.py:371`, `src/ai_usage_cost/tui.py:119`
%% generated:node-citations-use-case-uc-27 end %%
