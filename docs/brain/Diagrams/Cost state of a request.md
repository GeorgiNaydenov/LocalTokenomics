---
title: Cost state of a request
aliases: []
tags: [diagram, mermaid, state]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/*]
verified-against: 1445ea834ab7
sources: [docs/brain/architecture/diagrams/state-request-cost-state.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost
authored: true
approved-by: human
approved-at: '2026-11-19T06:39:06+00:00'
---

# Cost state of a request

Every request ends in exactly one of four cost states, and the state decides whether its cost is counted. This view shows what puts a request into each state and how the states are ranked when a session is shown. It explains why a session can be marked unpriced even when most of its requests have a price.

## What the diagram shows

- The four states are priced, free, unpriced and unavailable. `src/ai_usage_cost/models.py:8`
- A request with no token counts is unavailable, which is not the same as free. `src/ai_usage_cost/pricing.py:421`
- A provider whose rules say free gives the free state and a zero cost breakdown. `src/ai_usage_cost/pricing.py:422` `src/ai_usage_cost/pricing.py:434`
- A request whose model matches no rate row is unpriced, so its tokens are counted but its cost is left out. `src/ai_usage_cost/pricing.py:425`
- Every other request is priced. `src/ai_usage_cost/pricing.py:426`
- A match through a shorter prefix keeps the priced state but sets the estimated flag. `src/ai_usage_cost/pricing.py:313`
- The pipeline raises a warning for each estimated model. `src/ai_usage_cost/pipeline.py:225`
- A session shows the worst state among its requests, ranked priced 0, free 1, unpriced 2 and unavailable 3. `src/ai_usage_cost/aggregate.py:20` `src/ai_usage_cost/aggregate.py:640`

## Capability and related functionality

- Realises the cost honesty rule described in [[Ai usage cost Overview]]: unknown cost is never shown as zero.
- The decision that picks the state is expanded in [[How one request is priced]].
- The fields that carry the state are listed in [[Ai usage cost Data Model]].

## The diagram

%% generated:diagram-state-request-cost-state start (do not edit; run brain docs generate) %%
```mermaid
stateDiagram-v2
    direction LR
    [*] --> Read: request loaded from the store
    Read --> unavailable: tokens are None
    Read --> free: provider rules say free
    Read --> unpriced: no rate row matches the model
    Read --> priced: a rate row matches
    unavailable --> [*]
    free --> [*]
    unpriced --> [*]
    priced --> [*]
    note right of unavailable
        Rank 3, the worst. No token counts, so cost is unknown, not zero.
    end note
    note right of free
        Rank 1. Cost is a zero breakdown.
    end note
    note right of unpriced
        Rank 2. Tokens count, cost is excluded, a warning is raised.
    end note
    note right of priced
        Rank 0, the best. A match by a shorter prefix is flagged estimated and a warning is raised.
    end note
    note left of Read
        Legend: a rounded box is a state, an arrow is a transition labelled with its trigger, the filled dot starts, the ringed dot ends, a note records a rule that holds in that state. A session shows the worst state of its requests.
    end note
```
%% generated:diagram-state-request-cost-state end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `src/ai_usage_cost/pricing.py:417` | The decision of the state |
> | `src/ai_usage_cost/pricing.py:429` | Where the state is used to skip or compute the cost |
> | `src/ai_usage_cost/aggregate.py:570` | The worst-state roll up for a session |
