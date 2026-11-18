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

30 terms, of which 0 belong to other chunks and appear only so that links have somewhere to land.

| Kind | Count |
|---|---|
| class | 2 |
| model | 2 |
| rule | 7 |
| use-case | 2 |

## Relations

| Relation | Count |
|---|---|
| none yet | 0 |

## The graph

```mermaid
flowchart LR
    n0["A reader is found by its SOURCE va<br/>rule"]
    n1["Discover AI tool usage from local <br/>use-case"]
    n2["Experimental readers carry a flag<br/>rule"]
    n3["Muse Code control folders are skip<br/>rule"]
    n4["Read a tools SQLite store without <br/>use-case"]
    n5["Readers only read<br/>rule"]
    n6["Repeated Codex token totals are no<br/>rule"]
    n7["Source<br/>class"]
    n8["Source<br/>model"]
    n9["Spec<br/>class"]
    n10["Spec<br/>model"]
    n11["Synthetic Claude Code records are <br/>rule"]
    n12["Unparsable lines are skipped and c<br/>rule"]
    classDef k_class fill:#dae8fc,stroke:#222222,color:#222222
    class n7,n9 k_class
    classDef k_model fill:#dae8fc,stroke:#222222,color:#222222
    class n8,n10 k_model
    classDef k_rule fill:#e1d5e7,stroke:#222222,color:#222222
    class n0,n2,n3,n5,n6,n11,n12 k_rule
    classDef k_usecase fill:#fff2cc,stroke:#222222,color:#222222
    class n1,n4 k_usecase
```

The full slice is in `ch-localtokenomics-src-ai-usage-cost-sources.jsonld` beside this note. Project terms are the primary labels; ArchiMate, DDD, schema.org and Dublin Core terms annotate them.
