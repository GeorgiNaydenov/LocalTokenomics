---
title: Usage cost goals
aliases: []
tags: [diagram, mermaid, use-case-diagram]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/*]
verified-against: 1445ea834ab7
sources: [docs/brain/architecture/diagrams/usage-cost-goals.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost
authored: true
node_citations:
  usage-cost-goals:
    person: ['src/ai_usage_cost/cli.py:24-27']
    logs: ['src/ai_usage_cost/store.py:218-220']
    notify: ['src/ai_usage_cost/cli.py:344-354']
    uc1: ['src/ai_usage_cost/cli.py:71-105']
    uc2: ['src/ai_usage_cost/cli.py:108-137']
    uc3: ['src/ai_usage_cost/cli.py:175-196']
    uc4: ['src/ai_usage_cost/cli.py:298-354']
    uc5: ['src/ai_usage_cost/api.py:320-359']
    uc6: ['src/ai_usage_cost/api.py:361-368']
    uc7: ['src/ai_usage_cost/api.py:370-382']
    uc8: ['src/ai_usage_cost/cli.py:140-172']
    uc9: ['src/ai_usage_cost/cli.py:199-225']
    uc10: ['src/ai_usage_cost/cli.py:228-248']
    uc11: ['src/ai_usage_cost/cli.py:357-376']
approved-by: human
approved-at: '2026-11-19T06:39:06+00:00'
---

# Usage cost goals

This view lists what a person can get done with the tool and which outside parties take part. Every goal starts from the same step: reading the logs that AI coding tools already keep and pricing them. Seeing the goals together helps decide where a change will be felt.

## What the diagram shows

- There is one human actor and no login: every command is run by the person who owns the machine. `src/ai_usage_cost/cli.py:24-27`
- Seeing the cost means scanning the logs, pricing them and printing a breakdown, and the command exits with code 1 when no usage is found. `src/ai_usage_cost/cli.py:87-105`
- The dashboard, the export, the alert and the terminal browser all start by running the same analysis, which is why they include the first goal. `src/ai_usage_cost/cli.py:125` `src/ai_usage_cost/cli.py:184-185` `src/ai_usage_cost/cli.py:331-332` `src/ai_usage_cost/cli.py:369-370`
- The demo command writes synthetic logs and then serves the dashboard over them with a separate store. `src/ai_usage_cost/cli.py:159-172`
- Inspecting, rating and forgetting a session, and reading the text of one span, are steps inside the dashboard served by session routes. `src/ai_usage_cost/api.py:320-382`
- The alert sends its message to each notification address the person passes. `src/ai_usage_cost/cli.py:344-354`
- The GPU sampler and the SQL browser work on the store directly and do not price anything. `src/ai_usage_cost/cli.py:211-225` `src/ai_usage_cost/cli.py:235-248`

## Capability and related functionality

- Each goal is a use case in the specification note of this chunk, [[Ai usage cost Specification]], with its cited main flow.
- The routes behind the dashboard goals are drawn in [[Usage cost HTTP routes]], and the alert run in [[Spend alert run]].
- The shared first step is drawn in [[Scan pipeline from logs to report]].

## Usage cost goals

%% generated:diagram-usage-cost-goals start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    person(["Person using the tool"]):::actor
    logs(["AI coding tool logs"]):::external
    notify(["Notification target"]):::external

    subgraph sys["ai usage cost"]
        direction TB
        uc1("See what my AI usage would cost"):::usecase
        uc2("Explore spend in the dashboard"):::usecase
        uc3("Export a report as a file"):::usecase
        uc4("Be alerted when spend rises"):::usecase
        uc5("Inspect and rate one session"):::usecase
        uc6("Forget a session"):::usecase
        uc7("Read the text of one span"):::usecase
        uc8("Try the tool with demo data"):::usecase
        uc9("Sample GPU use for local models"):::usecase
        uc10("Query the store with SQL"):::usecase
        uc11("Browse sessions in the terminal"):::usecase
    end

    person --- uc1
    person --- uc2
    person --- uc3
    person --- uc4
    person --- uc8
    person --- uc9
    person --- uc10
    person --- uc11
    uc1 --- logs
    uc4 --- notify
    uc2 -.->|include| uc1
    uc3 -.->|include| uc1
    uc4 -.->|include| uc1
    uc11 -.->|include| uc1
    uc8 -.->|include| uc2
    uc5 -.->|extend| uc2
    uc6 -.->|extend| uc2
    uc7 -.->|extend| uc5

    subgraph Legend
        direction LR
        zlegend_a(["Actor"]):::actor
        zlegend_b("Use case"):::usecase
        zlegend_c["System boundary: the outer box"]:::boundary
        zlegend_d(["Outside system"]):::external
        zlegend_e["include: always runs the other goal"]:::boundary
        zlegend_f["extend: an optional step of the other goal"]:::boundary
        zlegend_a ~~~ zlegend_b ~~~ zlegend_c ~~~ zlegend_d ~~~ zlegend_e ~~~ zlegend_f
    end

    classDef actor fill:#fff2cc,stroke:#222222,color:#222222
    classDef usecase fill:#dae8fc,stroke:#222222,color:#222222
    classDef external fill:#f5f5f5,stroke:#666666,color:#222222,stroke-dasharray:4 3
    classDef boundary fill:#ffffff,stroke:#222222,color:#222222
```
%% generated:diagram-usage-cost-goals end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `src/ai_usage_cost/cli.py:71-376` | The eight commands behind the goals |
> | `src/ai_usage_cost/api.py:320-382` | The session routes behind the dashboard goals |
