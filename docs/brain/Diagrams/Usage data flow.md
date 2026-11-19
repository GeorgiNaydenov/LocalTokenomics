---
title: Usage data flow
aliases: []
tags: [dfd, diagram, mermaid]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/*]
verified-against: 1445ea834ab7
sources: [docs/brain/architecture/diagrams/dfd-usage-data-flow.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost
authored: true
node_citations:
  dfd-usage-data-flow:
    e1: ['src/ai_usage_cost/sources/base.py:117-129']
    e2: ['src/ai_usage_cost/cli.py:71-105']
    e3: ['src/ai_usage_cost/cli.py:344-354']
    p1: ['src/ai_usage_cost/store.py:190-305']
    p2: ['src/ai_usage_cost/pipeline.py:166-245']
    p3: ['src/ai_usage_cost/pipeline.py:305-349']
    p4: ['src/ai_usage_cost/cli.py:71-105']
    p5: ['src/ai_usage_cost/privacy.py:86-101']
    p6: ['src/ai_usage_cost/store.py:568-606']
    d1: ['src/ai_usage_cost/store.py:140-151']
    d2: ['src/ai_usage_cost/pricing.py:285-287']
    d3: ['src/ai_usage_cost/privacy.py:60-68']
approved-by: human
approved-at: '2026-11-19T06:39:06+00:00'
---

# Usage data flow

This view shows where usage data comes from, where it is kept and who can see it. Logs flow in, prices and settings are read from local files, and the report goes back to the person. It lets a privacy reviewer check that text from a session is only released when the person allows it.

## What the diagram shows

- Source databases are opened read only, so the tool never changes the logs of another tool. `src/ai_usage_cost/sources/base.py:123`
- Ingest records requests, spans and a fingerprint of each file in the store. `src/ai_usage_cost/store.py:281`
- The privacy settings tell ingest which projects to leave out and how long to keep trace rows. `src/ai_usage_cost/pipeline.py:183`
- The rate table is read from a local file and joined to each request. `src/ai_usage_cost/pricing.py:22`
- The settings file sits in the home folder next to the store. `src/ai_usage_cost/privacy.py:12`
- The report goes back to the person as a table, as JSON or as an API reply. `src/ai_usage_cost/cli.py:105` `src/ai_usage_cost/cli.py:96`
- A rating or a forget request writes a row to the store. `src/ai_usage_cost/store.py:568` `src/ai_usage_cost/store.py:595`
- Span text is refused while metadata only is on, and redacted when it is released. `src/ai_usage_cost/privacy.py:87` `src/ai_usage_cost/privacy.py:98`
- The alert command is the one flow that sends data out of the machine, to the targets the person names. `src/ai_usage_cost/cli.py:349`

## Capability and related functionality

- Realises the privacy stance described in [[Ai usage cost Security]].
- The stores D1 to D3 correspond to the tables in [[Ai usage cost Data Model]].
- The order of the same steps over time is [[Scan pipeline from logs to report]].
- The HTTP routes behind the person's requests are in [[Ai usage cost API]].

## The diagram

%% generated:diagram-dfd-usage-data-flow start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    e1["External: AI coding tool logs and databases"]:::extsys
    e2(["Person: reads the report, rates sessions"]):::person
    e3["External: notification target"]:::extsys
    subgraph tb["Trust boundary: the owner's machine"]
        p1("1.0 Ingest changed log files"):::proc
        p2("2.0 Price every request"):::proc
        p3("3.0 Build the report"):::proc
        p4("4.0 Present report and alerts"):::proc
        p5("5.0 Release span text with redaction"):::sec
        p6("6.0 Record a rating or forget a session"):::proc
        d1[("D1 usage.db store")]:::store
        d2[("D2 rates.json")]:::store
        d3[("D3 config.json privacy settings")]:::store
    end

    e1 -->|"log records, read only"| p1
    d3 -->|"excluded projects, retention days"| p1
    p1 -->|"requests, spans, file fingerprints"| d1
    d1 -->|"requests, session flags"| p2
    d2 -->|"rate rows, prefixes, as-of date"| p2
    p2 -->|"priced events, warnings"| p3
    p3 -->|"report: totals, buckets, sessions"| p4
    e2 -->|"filters, commands"| p4
    p4 -->|"report as table, JSON, PNG or API reply"| e2
    p4 -->|"spend alert text"| e3
    e2 -->|"rating, forget request"| p6
    p6 -->|"outcome row, exclusion row"| d1
    e2 -->|"span id"| p5
    d1 -->|"record offset and content path"| p5
    d3 -->|"metadata only flag, size limit"| p5
    e1 -->|"raw record text"| p5
    p5 -->|"redacted text or refusal"| e2

    subgraph Legend
        direction LR
        zlegend_a("1.0 Process"):::proc
        zlegend_b("Security control"):::sec
        zlegend_c[("D1 Data store")]:::store
        zlegend_d(["Person"]):::person
        zlegend_e["External system, not controlled"]:::extsys
        zlegend_a ~~~ zlegend_b ~~~ zlegend_c ~~~ zlegend_d ~~~ zlegend_e
    end

    classDef proc fill:#dae8fc,stroke:#222222,color:#222222
    classDef sec fill:#e1d5e7,stroke:#222222,color:#222222
    classDef store fill:#d5e8d4,stroke:#222222,color:#222222
    classDef person fill:#fff2cc,stroke:#222222,color:#222222
    classDef extsys fill:#f5f5f5,stroke:#666666,stroke-dasharray:5 5,color:#222222
    style tb fill:none,stroke:#9673a6,stroke-dasharray:5 5
```
%% generated:diagram-dfd-usage-data-flow end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `src/ai_usage_cost/store.py:190` | Process 1.0 |
> | `src/ai_usage_cost/pipeline.py:166` | Process 2.0 |
> | `src/ai_usage_cost/aggregate.py:675` | Process 3.0 |
> | `src/ai_usage_cost/cli.py:299` | The outbound notification |
> | `src/ai_usage_cost/privacy.py:86` | Process 5.0 |
> | `src/ai_usage_cost/store.py:568` | Process 6.0 |
