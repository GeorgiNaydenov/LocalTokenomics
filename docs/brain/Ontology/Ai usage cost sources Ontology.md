---
title: Ai usage cost sources Ontology
aliases: []
tags: [overview, reference]
area: ontology
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: []
chunk: ch-localtokenomics-src-ai-usage-cost-sources
generated: true
---

# Ai usage cost sources Ontology

This is the part of the project's knowledge graph that the code in Ai usage cost sources defines. It shows what the code knows about, and how those things are linked to each other and to the rest of the project.

## What it contains

29 terms, of which 0 belong to other chunks and appear only so that links have somewhere to land.

| Kind | Count |
|---|---|
| class | 2 |
| rule | 7 |
| system | 1 |
| use-case | 2 |

## Relations

| Relation | Count |
|---|---|
| none yet | 0 |

## The graph

```mermaid
flowchart LR
    n0["A reader is found by its SOURCE va<br/>rule"]
    n1["Ai usage cost sources<br/>system"]
    n2["Discover AI tool usage from local <br/>use-case"]
    n3["Experimental readers carry a flag<br/>rule"]
    n4["Muse Code control folders are skip<br/>rule"]
    n5["Read a tools SQLite store without <br/>use-case"]
    n6["Readers only read<br/>rule"]
    n7["Repeated Codex token totals are no<br/>rule"]
    n8["Source<br/>class"]
    n9["Spec<br/>class"]
    n10["Synthetic Claude Code records are <br/>rule"]
    n11["Unparsable lines are skipped and c<br/>rule"]
    classDef k_class fill:#dae8fc,stroke:#222222,color:#222222
    class n8,n9 k_class
    classDef k_rule fill:#e1d5e7,stroke:#222222,color:#222222
    class n0,n3,n4,n6,n7,n10,n11 k_rule
    classDef k_system fill:#dae8fc,stroke:#222222,color:#222222
    class n1 k_system
    classDef k_usecase fill:#fff2cc,stroke:#222222,color:#222222
    class n2,n5 k_usecase
```

The full slice is in `ch-localtokenomics-src-ai-usage-cost-sources.jsonld` beside this note. Project terms are the primary labels; ArchiMate, DDD, schema.org and Dublin Core terms annotate them.
