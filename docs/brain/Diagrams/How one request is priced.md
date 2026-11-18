---
title: How one request is priced
aliases: []
tags:
- diagram
- flowchart
- mermaid
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers:
- src/ai_usage_cost/*
sources:
- docs/brain/architecture/diagrams/flow-price-one-request.mmd
chunk: ch-localtokenomics-src-ai-usage-cost
authored: true
node_citations:
  flow-price-one-request:
    start:
    - src/ai_usage_cost/pricing.py:429-432
    d1:
    - src/ai_usage_cost/pricing.py:420-421
    x1:
    - src/ai_usage_cost/pricing.py:420-421
    d2:
    - src/ai_usage_cost/pricing.py:422-423
    x2:
    - src/ai_usage_cost/pricing.py:433-434
    d3:
    - src/ai_usage_cost/pricing.py:424-425
    x3:
    - src/ai_usage_cost/pricing.py:424-425
    s1:
    - src/ai_usage_cost/pricing.py:446-475
    - src/ai_usage_cost/pricing.py:507-515
    d4:
    - src/ai_usage_cost/pricing.py:519
    d5:
    - src/ai_usage_cost/pricing.py:520-522
    s3:
    - src/ai_usage_cost/pricing.py:522
    d6:
    - src/ai_usage_cost/pricing.py:523
    s4:
    - src/ai_usage_cost/pricing.py:523-524
    s5:
    - src/ai_usage_cost/pricing.py:525-526
    d7:
    - src/ai_usage_cost/pricing.py:528
    s6:
    - src/ai_usage_cost/pricing.py:528-529
    s7:
    - src/ai_usage_cost/pricing.py:533-551
    x4:
    - src/ai_usage_cost/pricing.py:554-562
---

# How one request is priced

This view lays out how the tool decides the price of one request. It shows the early exits where a request is left unpriced and the order in which the date, the size, the service tier and the time of day change the rate. Anyone checking a number on a report can follow the same steps.

## What the diagram shows

- A request with no token counts leaves the flow as unavailable. `src/ai_usage_cost/pricing.py:420`
- A free provider leaves the flow as free with a zero breakdown. `src/ai_usage_cost/pricing.py:422`
- A model with no rate row leaves the flow as unpriced. `src/ai_usage_cost/pricing.py:424`
- The price fields of the first period that covers the UTC date replace the row's own. `src/ai_usage_cost/pricing.py:505`
- The last band whose minimum is at or under the request's total input is selected. `src/ai_usage_cost/pricing.py:508`
- A tier other than standard uses the row's variant for that tier when one exists. `src/ai_usage_cost/pricing.py:520`
- Without a variant a batch request gets the batch factor on every price. `src/ai_usage_cost/pricing.py:523`
- Any other tier is flagged as unpriced for that tier and keeps the standard price. `src/ai_usage_cost/pricing.py:526`
- A peak window that covers the UTC weekday and hour replaces the price. `src/ai_usage_cost/pricing.py:528`
- Each cache price is the set's own figure, else the row's published ratio, else the provider multiplier. `src/ai_usage_cost/pricing.py:478`
- The result is a cost breakdown that also keeps a no cache baseline. `src/ai_usage_cost/pricing.py:559`

## Capability and related functionality

- Realises the pricing rule behind every cost figure in [[Ai usage cost Overview]].
- The three early exits are the states drawn in [[Cost state of a request]].
- The run that calls this step for every request is [[Scan pipeline from logs to report]].
- The rate table fields it reads are listed in [[Ai usage cost Data Model]].

## The diagram

%% generated:diagram-flow-price-one-request start (do not edit; run brain docs generate) %%
```mermaid
flowchart TD
    start(["Request to price"]):::startNode
    d1{"Token counts logged?"}:::decision
    x1(["unavailable: no cost, tokens not counted"]):::fail
    d2{"Provider marked free?"}:::decision
    x2(["free: zero cost breakdown"]):::ok
    d3{"Rate row found for the model?"}:::decision
    x3(["unpriced: tokens counted, cost excluded"]):::fail
    s1["Apply the period for the UTC date, then the band for total input"]:::step
    d4{"Tier is standard?"}:::decision
    d5{"Row has a variant for the tier?"}:::decision
    s3["Use the variant price"]:::step
    d6{"Tier is batch?"}:::decision
    s4["Apply the batch factor to every price"]:::step
    s5["Flag tier unpriced, keep the standard price"]:::step
    d7{"Peak window covers the UTC time?"}:::decision
    s6["Use the peak price"]:::step
    s7["Resolve the three cache prices"]:::step
    x4(["priced: cost breakdown returned"]):::ok

    start --> d1
    d1 -->|no| x1
    d1 -->|yes| d2
    d2 -->|yes| x2
    d2 -->|no| d3
    d3 -->|no| x3
    d3 -->|yes| s1
    s1 --> d4
    d4 -->|yes| d7
    d4 -->|no| d5
    d5 -->|yes| s3
    d5 -->|no| d6
    s3 --> d7
    d6 -->|yes| s4
    d6 -->|no| s5
    s4 --> d7
    s5 --> d7
    d7 -->|yes| s6
    d7 -->|no| s7
    s6 --> s7
    s7 --> x4

    subgraph Legend
        direction LR
        zlegend_a(["Start"]):::startNode
        zlegend_b["Step"]:::step
        zlegend_c{"Decision"}:::decision
        zlegend_d(["Exit that succeeds"]):::ok
        zlegend_e(["Exit that fails to price"]):::fail
        zlegend_a ~~~ zlegend_b ~~~ zlegend_c ~~~ zlegend_d ~~~ zlegend_e
    end

    classDef startNode fill:#fff2cc,stroke:#222222,color:#222222
    classDef step fill:#dae8fc,stroke:#222222,color:#222222
    classDef decision fill:#ffffff,stroke:#222222,color:#222222
    classDef ok fill:#d5e8d4,stroke:#222222,color:#222222
    classDef fail fill:#f8cecc,stroke:#222222,color:#222222
```
%% generated:diagram-flow-price-one-request end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `src/ai_usage_cost/pricing.py:495` | Period, band, tier, peak and cache price resolution |
> | `src/ai_usage_cost/pricing.py:429` | The early exits and the call to cost of |
> | `src/ai_usage_cost/pricing.py:446` | How a period replaces the row's prices |
> | `src/ai_usage_cost/pricing.py:478` | The three step cache price rule |
