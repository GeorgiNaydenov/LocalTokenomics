---
title: Reader glossary map
aliases: []
tags: [diagram, glossary-map, mermaid]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [src/ai_usage_cost/sources/**]
sources: [docs/brain/architecture/diagrams/src-terms.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost-sources
authored: true
use-cases: [UC-13]
node_citations:
  src-terms:
    source: ['src/ai_usage_cost/sources/base.py:17-40']
    root: ['src/ai_usage_cost/sources/base.py:22', 'src/ai_usage_cost/sources/base.py:47-49']
    client: ['src/ai_usage_cost/sources/base.py:21']
    tokendata: ['src/ai_usage_cost/sources/base.py:14']
    event: ['src/ai_usage_cost/models.py:49-72']
    tokens: ['src/ai_usage_cost/models.py:12-22']
    span: ['src/ai_usage_cost/trace.py:55-84']
    caps: ['src/ai_usage_cost/trace.py:104-109']
    prov: ['src/ai_usage_cost/models.py:9']
    exp: ['src/ai_usage_cost/sources/base.py:29-31']
    resume: ['src/ai_usage_cost/sources/base.py:32-40']
    session: ['src/ai_usage_cost/models.py:55']
    tsource: ['src/ai_usage_cost/models.py:65']
---

# Reader glossary map

This map shows the words used for readers and how they relate to each other. It helps a new person and a business reader mean the same thing when they say source, root, event or span. Each term is named exactly as the code names it.

## What the diagram shows

- A Source is the record that describes one reader. It names the files it scans through its default roots and a files function. `src/ai_usage_cost/sources/base.py:18` `src/ai_usage_cost/sources/base.py:22`
- A Source names its clients, which are the tool names shown to people. `src/ai_usage_cost/sources/base.py:21`
- A Source declares token data, which is full or session. `src/ai_usage_cost/sources/base.py:14`
- A Source yields many usage events and may also yield spans. `src/ai_usage_cost/sources/base.py:24` `src/ai_usage_cost/sources/base.py:27`
- A Source declares capabilities, and each capability is labelled with a provenance. `src/ai_usage_cost/sources/base.py:28` `src/ai_usage_cost/trace.py:105`
- A Source may be flagged experimental when its parser was built from the tool's source and synthetic fixtures. `src/ai_usage_cost/sources/base.py:29` `src/ai_usage_cost/sources/base.py:31`
- A Source may declare parse_resume, which reads a grown log again from a byte offset. `src/ai_usage_cost/sources/base.py:40`
- A usage event has token usage only when the reader can see tokens, belongs to a session id and carries a title source. `src/ai_usage_cost/models.py:57` `src/ai_usage_cost/models.py:55` `src/ai_usage_cost/models.py:65`
- A span has token usage only when the log reports it. `src/ai_usage_cost/trace.py:76`

## Capability and related functionality

- The map supports the shared language of the readers package. The glossary entries for reader, root, token data and experimental reader are listed in [[Ai usage cost sources Ontology]]. [[Ai usage cost sources Overview]] explains the readers in prose, and [[Ai usage cost sources Workflows]] walks through a scan. The sibling views are [[Readers concepts]], [[Reader types]], [[Reader data lineage]], [[Reader module imports]], [[Reader glossary map]], [[Readers component view]] and [[Readers data flow]].
- Terms for the cost side of the product, such as priced and unpriced, belong to the pricing chunk, not to this map.

## The diagram

%% generated:diagram-src-terms start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    source("Source<br/>one reader for one tool"):::term
    root("Root<br/>a folder or file a reader scans"):::term
    client("Client<br/>the tool name shown to people"):::term
    tokendata("Token data<br/>full or session"):::term
    event("Usage event<br/>one request or one turn"):::term
    tokens("Token usage<br/>counts by bucket"):::term
    span("Span<br/>one step inside a session"):::term
    caps("Capabilities<br/>what a reader can see"):::term
    prov("Provenance<br/>where a value came from"):::term
    exp("Experimental<br/>not checked on a real session"):::term
    resume("parse_resume<br/>re-read a grown log from an offset"):::term
    session("Session id<br/>groups events of one chat"):::term
    tsource("Title source<br/>tool, summary, prompt or folder"):::term
    source -->|scans| root
    source -->|names| client
    source -->|declares| tokendata
    source -->|yields many| event
    source -->|may yield| span
    source -->|declares| caps
    source -->|may be flagged| exp
    source -->|may declare| resume
    caps -->|labels each value with| prov
    event -->|has none when session only| tokens
    span -->|has none when unknown| tokens
    event -->|belongs to| session
    event -->|has| tsource
    subgraph Legend
        direction LR
        zlegend_a("Term: named as the code names it"):::term
        zlegend_b["Arrow label: the relation, such as has, yields, belongs to"]:::term
        zlegend_a ~~~ zlegend_b
    end
    classDef term fill:#dae8fc,stroke:#222222,color:#111111
```
%% generated:diagram-src-terms end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `src/ai_usage_cost/sources/base.py:18` | Source, root, client, token data, capabilities, experimental and resume |
> | `src/ai_usage_cost/models.py:49` | Usage event, session id and title source |
> | `src/ai_usage_cost/trace.py:55` | Span |
> | `src/ai_usage_cost/models.py:9` | Provenance values |
