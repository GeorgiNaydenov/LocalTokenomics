---
title: Scan and report process
aliases: []
tags:
- bpmn
- diagram
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers:
- src/ai_usage_cost/*
sources:
- docs/brain/architecture/bpmn/bpmn-scan-and-report.bpmn
chunk: ch-localtokenomics-src-ai-usage-cost
authored: true
process-source: code-flow
node_citations:
  bpmn-scan-and-report:
    s1:
    - src/ai_usage_cost/cli.py:72
    u1:
    - src/ai_usage_cost/cli.py:71-87
    u2:
    - src/ai_usage_cost/cli.py:105
    e1:
    - src/ai_usage_cost/cli.py:105
    s2:
    - src/ai_usage_cost/cli.py:87
    t1:
    - src/ai_usage_cost/pipeline.py:175-176
    t2:
    - src/ai_usage_cost/store.py:218-220
    g1:
    - src/ai_usage_cost/store.py:229-231
    t3:
    - src/ai_usage_cost/store.py:252-271
    g2:
    - src/ai_usage_cost/store.py:229-231
    t4:
    - src/ai_usage_cost/pipeline.py:186-199
    t5:
    - src/ai_usage_cost/pipeline.py:212-239
    t6:
    - src/ai_usage_cost/pipeline.py:305-349
    g3:
    - src/ai_usage_cost/cli.py:98
    t7:
    - src/ai_usage_cost/cli.py:105
    e2:
    - src/ai_usage_cost/cli.py:105
    e3:
    - src/ai_usage_cost/cli.py:98-104
---

# Scan and report process

This view shows the scan as a business process between a person and the tool. The person asks to see their spend, and the tool does the reading, pricing and adding up. It also shows the one case where nothing is produced, which helps when explaining an empty result.

## What the diagram shows

- The person starts the process by running the scan command or opening the dashboard. `src/ai_usage_cost/cli.py:72`
- The tool loads the privacy settings and opens the store. `src/ai_usage_cost/pipeline.py:175` `src/ai_usage_cost/pipeline.py:176`
- It finds the log files under each source root. `src/ai_usage_cost/store.py:220`
- A file that has not changed is skipped. `src/ai_usage_cost/store.py:230`
- A changed file is parsed and its requests are stored. `src/ai_usage_cost/store.py:255` `src/ai_usage_cost/store.py:271`
- The stored requests are loaded and each one is priced. `src/ai_usage_cost/pipeline.py:186` `src/ai_usage_cost/pipeline.py:198`
- Warnings are added for unpriced and estimated models and for old rates. `src/ai_usage_cost/pipeline.py:212` `src/ai_usage_cost/pipeline.py:235`
- The requests are filtered and grouped into a report. `src/ai_usage_cost/pipeline.py:335`
- With no requests the command ends with exit code 1. `src/ai_usage_cost/cli.py:98` `src/ai_usage_cost/cli.py:104`
- With requests the report is returned and the person reads it. `src/ai_usage_cost/cli.py:105`

## Capability and related functionality

- Realises the scan capability described in [[Ai usage cost Workflows]].
- The technical order of the same process is [[Scan pipeline from logs to report]], and the data it moves is [[Usage data flow]].
- The pricing step inside the process is opened up in [[How one request is priced]].

## The diagram

![Scan and report process](../architecture/rendered/bpmn-scan-and-report.svg)

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `src/ai_usage_cost/cli.py:72` | The command that starts the process |
> | `src/ai_usage_cost/pipeline.py:166` | Settings, store, ingest, pricing and warnings |
> | `src/ai_usage_cost/store.py:190` | The file loop with its skip decision |
> | `src/ai_usage_cost/pipeline.py:305` | Filtering and grouping |
