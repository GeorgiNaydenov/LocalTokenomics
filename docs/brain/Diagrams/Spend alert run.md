---
title: Spend alert run
aliases: []
tags: [activity, diagram, mermaid]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/*]
verified-against: 1445ea834ab7
sources: [docs/brain/architecture/diagrams/spend-alert-run.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost
authored: true
node_citations:
  spend-alert-run:
    start: ['src/ai_usage_cost/cli.py:298-319']
    d_opts: ['src/ai_usage_cost/cli.py:320-326']
    d_extra: ['src/ai_usage_cost/cli.py:327', 'src/ai_usage_cost/cli.py:48-56']
    win: ['src/ai_usage_cost/cli.py:329-330']
    analyse: ['src/ai_usage_cost/cli.py:331-332']
    d_rise: ['src/ai_usage_cost/cli.py:333-334']
    prev: ['src/ai_usage_cost/cli.py:335-337']
    decide: ['src/ai_usage_cost/cli.py:257-282', 'src/ai_usage_cost/cli.py:339-340']
    d_fire: ['src/ai_usage_cost/cli.py:282', 'src/ai_usage_cost/cli.py:341-342']
    add: ['src/ai_usage_cost/cli.py:344-346']
    d_add: ['src/ai_usage_cost/cli.py:346-348']
    send: ['src/ai_usage_cost/cli.py:349-352']
    d_sent: ['src/ai_usage_cost/cli.py:349-354']
    bad: ['src/ai_usage_cost/cli.py:320-326']
    noextra: ['src/ai_usage_cost/cli.py:52-56']
    quiet: ['src/ai_usage_cost/cli.py:341-342']
    failed: ['src/ai_usage_cost/cli.py:346-348', 'src/ai_usage_cost/cli.py:353-354']
    done: ['src/ai_usage_cost/cli.py:349-352']
approved-by: human
approved-at: '2026-11-19T06:39:06+00:00'
---

# Spend alert run

This view walks through one run of the spend alert, from the options the person types to the message that reaches their phone or chat. It shows which mistakes stop the run early and when the run ends quietly because spend stayed under the limit. It helps anyone who schedules the alert understand why it did or did not fire.

## What the diagram shows

- The window length must be at least one day, and exactly one of the two thresholds must be given, or the command stops with a parameter error. `src/ai_usage_cost/cli.py:320-326`
- The notification library is an optional extra; without it the command prints the install hint and exits with code 2. `src/ai_usage_cost/cli.py:327` `src/ai_usage_cost/cli.py:48-56`
- The window ends today and starts the given number of days back, counting today. `src/ai_usage_cost/cli.py:329-330`
- The run analyses the store and builds the report of that window. `src/ai_usage_cost/cli.py:331-332`
- With the rise threshold, a second report covers the window of the same length just before. `src/ai_usage_cost/cli.py:333-337`
- The decision compares the window total with the total threshold, or the rise over the earlier window with the rise threshold, and fires only when the amount is strictly above it. `src/ai_usage_cost/cli.py:257-282`
- The message also names the tokens, requests and sessions, and says which cost is unknown rather than zero: unpriced models and sessions without token counts. `src/ai_usage_cost/cli.py:273-295`
- The message is always printed; when the decision does not fire, nothing is sent. `src/ai_usage_cost/cli.py:340-342`
- Each target address is added in turn, and a rejected address or a failed delivery ends the run with code 1. `src/ai_usage_cost/cli.py:344-354`

## Capability and related functionality

- Realises the use case be alerted when spend rises, one of the goals in [[Usage cost goals]].
- The two windows are drawn on a calendar in [[Alert comparison windows]], and the refusals beside the other commands in [[Usage cost refusals]].
- The analysis step is drawn in [[Scan pipeline from logs to report]], and the commands are described in [[Ai usage cost Workflows]].

## Spend alert run

%% generated:diagram-spend-alert-run start (do not edit; run brain docs generate) %%
```mermaid
flowchart TD
    subgraph lane_person["Person"]
        start(("Start: runs alert with --to, a threshold and --days")):::startNode
    end
    subgraph lane_cli["alert command"]
        d_opts{"days at least 1 and exactly one of over, rise-over?"}:::decision
        d_extra{"apprise installed?"}:::decision
        win("Window: today and the days before it"):::action
        d_rise{"rise-over given?"}:::decision
        prev("Report the window of the same length before it"):::action
        decide("alert_decision, then print its message"):::action
        d_fire{"amount above the threshold?"}:::decision
        add("Add every --to target"):::action
        d_add{"every target accepted?"}:::decision
        d_sent{"notify delivered?"}:::decision
    end
    subgraph lane_pipe["pipeline"]
        analyse("analyze, then report_of for the window"):::action
    end
    subgraph lane_apprise["Apprise"]
        send("Send title and message"):::action
    end
    bad(("Exit: bad parameter")):::fail
    noextra(("Exit code 2: extra missing")):::fail
    quiet(("End: nothing sent")):::endNode
    failed(("Exit code 1: target rejected or not delivered")):::fail
    done(("End: alert sent")):::endNode

    start --> d_opts
    d_opts -->|no| bad
    d_opts -->|yes| d_extra
    d_extra -->|no| noextra
    d_extra -->|yes| win --> analyse --> d_rise
    d_rise -->|yes| prev --> decide
    d_rise -->|no| decide
    decide --> d_fire
    d_fire -->|no| quiet
    d_fire -->|yes| add --> d_add
    d_add -->|no| failed
    d_add -->|yes| send --> d_sent
    d_sent -->|no| failed
    d_sent -->|yes| done

    subgraph Legend
        direction LR
        zlegend_a(("Start or end")):::startNode
        zlegend_b("Action"):::action
        zlegend_c{"Decision, every arrow labelled"}:::decision
        zlegend_d(("Exit that fails")):::fail
        zlegend_e["Lane: a titled box names who does the step. No fork or join: the run has no parallel branch"]:::lanekey
        zlegend_a ~~~ zlegend_b ~~~ zlegend_c ~~~ zlegend_d ~~~ zlegend_e
    end

    classDef startNode fill:#fff2cc,stroke:#222222,color:#222222
    classDef endNode fill:#d5e8d4,stroke:#222222,color:#222222
    classDef action fill:#dae8fc,stroke:#222222,color:#222222
    classDef decision fill:#ffffff,stroke:#222222,color:#222222
    classDef fail fill:#f8cecc,stroke:#222222,color:#222222
    classDef lanekey fill:#f5f5f5,stroke:#222222,color:#222222
```
%% generated:diagram-spend-alert-run end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `src/ai_usage_cost/cli.py:298-354` | The alert command |
> | `src/ai_usage_cost/cli.py:251-295` | The decision and the excluded cost line |
> | `src/ai_usage_cost/cli.py:48-56` | The optional extra check |
