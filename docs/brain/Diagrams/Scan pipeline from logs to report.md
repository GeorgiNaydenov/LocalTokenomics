---
title: Scan pipeline from logs to report
aliases: []
tags: [diagram, mermaid, sequence]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/*]
verified-against: 1445ea834ab7
sources: [docs/brain/architecture/diagrams/seq-scan-pipeline.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost
authored: true
approved-by: human
approved-at: '2026-11-19T06:39:06+00:00'
---

# Scan pipeline from logs to report

This view follows one scan from the command a person types to the report that appears on screen. It shows which parts of the tool do the work and in what order. A reader can see why a repeated scan is fast and where a warning about rates comes from.

## What the diagram shows

- The person starts a scan from the command line, which asks the pipeline for an analysis. `src/ai_usage_cost/cli.py:87`
- The pipeline loads the privacy settings and opens the store. `src/ai_usage_cost/pipeline.py:175` `src/ai_usage_cost/pipeline.py:176`
- Opening the store applies every migration the store has not seen yet. `src/ai_usage_cost/store.py:147`
- Ingest visits the files under each source root that exists. `src/ai_usage_cost/store.py:219`
- A file whose modification time, size and parser version are unchanged is skipped. `src/ai_usage_cost/store.py:230`
- A file that only grew is read from where the last scan stopped when its source allows it. `src/ai_usage_cost/store.py:252`
- Any other changed or new file is parsed again in full. `src/ai_usage_cost/store.py:255`
- A request is stored once per fingerprint, and a later record with more output replaces the earlier one. `src/ai_usage_cost/store.py:356`
- The pipeline then loads the stored requests, the file counts and the session flags. `src/ai_usage_cost/pipeline.py:186`
- It loads the rate table and prices each request. `src/ai_usage_cost/pipeline.py:192` `src/ai_usage_cost/pipeline.py:198`
- Warnings are added for models without a rate. `src/ai_usage_cost/pipeline.py:212`
- The command line turns the analysis into a report limited by date and client. `src/ai_usage_cost/cli.py:88` `src/ai_usage_cost/pipeline.py:305`
- When the report holds no requests the command prints a notice and exits with code 1. `src/ai_usage_cost/cli.py:104`
- Otherwise the command prints the tables. `src/ai_usage_cost/cli.py:105`

## Capability and related functionality

- Realises the scan capability described in [[Ai usage cost Workflows]], the command that most people run first.
- The same run seen as data movement is [[Usage data flow]], and as a business process it is [[Scan and report process]].
- The pricing step is opened up in [[How one request is priced]], and the states a priced request can end in are in [[Cost state of a request]].
- The HTTP routes that reuse this pipeline are listed in [[Ai usage cost API]].

## The diagram

%% generated:diagram-seq-scan-pipeline start (do not edit; run brain docs generate) %%
```mermaid
sequenceDiagram
    autonumber
    box rgb(255,242,204) Person
        actor U as Person
    end
    box rgb(218,232,252) This system
        participant C as Command line
        participant A as Pipeline
        participant X as Source parsers
        participant R as Rate table
        participant G as Report builder
    end
    box rgb(213,232,212) Data
        participant S as Store
    end
    U->>+C: ai-usage-cost scan
    C->>+A: analyze with db, roots, rates and rebuild
    A->>+S: open_store, migrate to the latest version
    S-->>-A: connection
    A->>+S: ingest with privacy exclusions
    loop each file under each present root
        alt size, mtime and parser version unchanged
            S->>S: skip the file
        else changed or new
            S->>+X: parse, or parse_resume when the file only grew
            X-->>-S: events, spans and warnings
            S->>S: insert requests, keep the largest output
        end
    end
    S-->>-A: ingest summary
    Note over A,S: Rule: a request is stored once per fingerprint, and a later record with more output replaces the earlier one
    A->>+S: load requests, file counts, session flags
    S-->>-A: events, counts, flags
    A->>+R: load the rate table
    R-->>-A: rows, prefixes, as of date
    loop each event
        A->>R: price_event
        R-->>A: cost breakdown and state
    end
    A-->>-C: Analysis with warnings
    C->>+G: report_of with since, until and filters
    G-->>-C: Report
    alt the report has no requests
        C-->>U: No usage found, exit code 1
    else requests found
        C-->>-U: terminal tables or JSON
    end
    Note over U,S: Legend: yellow is a person, blue is this system, green is data, a solid arrow is a call, a dashed arrow is a reply, a bar on a lifeline is a participant working, a framed block is a loop or a branch, a note is a rule
```
%% generated:diagram-seq-scan-pipeline end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `src/ai_usage_cost/cli.py:72` | The scan command |
> | `src/ai_usage_cost/pipeline.py:166` | Analysis: ingest, load, price, warn |
> | `src/ai_usage_cost/store.py:190` | Incremental ingest with skip and resume |
> | `src/ai_usage_cost/pricing.py:429` | Pricing of one request |
> | `src/ai_usage_cost/pipeline.py:305` | Filtering and report building |
