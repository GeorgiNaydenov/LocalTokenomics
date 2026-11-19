---
title: Reader data lineage
aliases: []
tags: [data-lineage, diagram, mermaid]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [src/ai_usage_cost/sources/**]
sources: [docs/brain/architecture/diagrams/src-lineage.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost-sources
authored: true
use-cases: [UC-13]
node_citations:
  src-lineage:
    tools: ['src/ai_usage_cost/sources/base.py:26', 'src/ai_usage_cost/sources/claude_code.py:34-37']
    roots_in: ['src/ai_usage_cost/sources/base.py:22', 'src/ai_usage_cost/sources/base.py:43-44', 'src/ai_usage_cost/sources/base.py:47-49']
    logs: ['src/ai_usage_cost/sources/claude_code.py:672-678', 'src/ai_usage_cost/sources/base.py:132-133']
    tasks: ['src/ai_usage_cost/sources/cline.py:139-149', 'src/ai_usage_cost/sources/cline.py:409-431']
    dbs: ['src/ai_usage_cost/sources/base.py:117-129', 'src/ai_usage_cost/sources/opencode.py:337']
    pick: ['src/ai_usage_cost/sources/base.py:47-49', 'src/ai_usage_cost/store.py:219']
    listing: ['src/ai_usage_cost/sources/base.py:23', 'src/ai_usage_cost/store.py:219-220']
    parse: ['src/ai_usage_cost/sources/base.py:24', 'src/ai_usage_cost/store.py:255']
    spans: ['src/ai_usage_cost/sources/base.py:27', 'src/ai_usage_cost/sources/claude_code.py:681', 'src/ai_usage_cost/sources/codex.py:954', 'src/ai_usage_cost/sources/qwen_code.py:172', 'src/ai_usage_cost/sources/antigravity.py:306', 'src/ai_usage_cost/store.py:261-263']
    reg: ['src/ai_usage_cost/sources/__init__.py:11-27']
    store: ['src/ai_usage_cost/store.py:219-262', 'src/ai_usage_cost/pipeline.py:178-186']
---

# Reader data lineage

This diagram follows the data from the files AI coding tools leave on a machine to the records the rest of the product uses. It shows where each data set is only read, where it is turned into something new and where warnings travel. A reader of the diagram can tell at once that no tool file is ever changed.

## What the diagram shows

- The tools write JSON line logs, JSON task files and SQLite stores. The readers only read them. `src/ai_usage_cost/sources/claude_code.py:677` `src/ai_usage_cost/sources/cline.py:424` `src/ai_usage_cost/sources/base.py:123`
- Root paths come from each reader's default roots or from a root the user passes, and only roots that exist are kept. `src/ai_usage_cost/sources/base.py:47` `src/ai_usage_cost/sources/base.py:49`
- For every kept root the reader's files function lists the files to read. `src/ai_usage_cost/store.py:220`
- The ingest loop calls the reader's parse function for each file and passes it a warnings list. `src/ai_usage_cost/store.py:255`
- Four readers also provide a spans function, which reads the same log again to build span records. `src/ai_usage_cost/sources/claude_code.py:681` `src/ai_usage_cost/sources/codex.py:954` `src/ai_usage_cost/sources/qwen_code.py:172` `src/ai_usage_cost/sources/antigravity.py:306`
- The JSON line helpers count lines that fail to parse and add one warning per file, and the SQLite helper turns a database error into a warning. `src/ai_usage_cost/sources/base.py:84` `src/ai_usage_cost/sources/base.py:128`
- Usage events, span records and warnings leave the chunk to the store, which receives the registered sources. `src/ai_usage_cost/pipeline.py:180`
- The client labels of every reader are merged into one map for the report. `src/ai_usage_cost/sources/__init__.py:26`

## Capability and related functionality

- The diagram realises the discovery capability: usage data is found and read in place, never copied or edited. [[Ai usage cost sources Overview]] explains the readers in prose, and [[Ai usage cost sources Workflows]] walks through a scan. The sibling views are [[Readers concepts]], [[Reader types]], [[Reader data lineage]], [[Reader module imports]], [[Reader glossary map]], [[Readers component view]] and [[Readers data flow]].
- The fuller data flow, with trust boundaries and the store, is in [[Readers data flow]]. The privacy rules that this lineage follows are in [[Ai usage cost sources Security]].

## The diagram

%% generated:diagram-src-lineage start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    tools(["AI coding tools<br/>write logs on this machine"]):::external
    roots_in(["Root paths<br/>per machine defaults or the root option"]):::external
    logs[("JSONL session logs<br/>claude-code, codex, gemini-cli, jan")]:::store
    tasks[("JSON task files<br/>cline, roo-code, kilo-code-legacy")]:::store
    dbs[("SQLite stores<br/>opencode, cursor, dyad, ollama-app")]:::store
    pick["Pick roots<br/>present_roots keeps roots that exist"]:::process
    listing["List files<br/>files(root) per reader"]:::process
    parse["Read and map<br/>parse(path, warnings)"]:::process
    spans["Build spans<br/>spans(path, warnings), four readers"]:::process
    reg["Registry<br/>registry(), client_labels()"]:::process
    store(["Usage store and report<br/>store.py, pipeline.py, other chunks"]):::external
    tools -->|records and rows| logs
    tools -->|records and rows| tasks
    tools -->|records and rows| dbs
    roots_in -->|root paths| pick
    pick -->|existing roots| listing
    logs -->|file names| listing
    tasks -->|file names| listing
    dbs -->|file names| listing
    listing -->|file paths| parse
    logs -->|raw records| parse
    tasks -->|raw records| parse
    dbs -->|read only rows| parse
    logs -->|raw records| spans
    parse -->|usage events| store
    parse -.->|warnings| store
    spans -->|span records| store
    reg -->|sources and client labels| store
    subgraph Legend
        direction LR
        zlegend_a(["Outside source or sink"]):::external
        zlegend_b[("Data store: a tool's files")]:::store
        zlegend_c["Process: a step of a reader"]:::process
        zlegend_d["Arrow is named after the data, not the action"]:::process
        zlegend_e["Dashed arrow: a side output"]:::process
        zlegend_a ~~~ zlegend_b ~~~ zlegend_c ~~~ zlegend_d ~~~ zlegend_e
    end
    classDef external fill:#eeeeee,stroke:#222222,stroke-dasharray:5 3,color:#111111
    classDef store fill:#d5e8d4,stroke:#222222,color:#111111
    classDef process fill:#dae8fc,stroke:#222222,color:#111111
```
%% generated:diagram-src-lineage end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `src/ai_usage_cost/sources/base.py:47` | Root selection |
> | `src/ai_usage_cost/sources/base.py:117` | Read only database access |
> | `src/ai_usage_cost/store.py:220` | Ingest loop that lists files |
> | `src/ai_usage_cost/store.py:255` | Full parse of a file |
> | `src/ai_usage_cost/sources/__init__.py:23` | Client label merge |
