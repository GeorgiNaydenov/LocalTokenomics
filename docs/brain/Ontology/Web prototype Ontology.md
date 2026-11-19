---
title: Web prototype Ontology
aliases: []
tags: [overview, reference]
area: ontology
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: []
chunk: ch-localtokenomics-web-src-prototype
generated: true
---

# Web prototype Ontology

This is the part of the project's knowledge graph that the code in Web prototype defines. It shows what the code knows about, and how those things are linked to each other and to the rest of the project.

## What it contains

12 terms, of which 1 belong to other chunks and appear only so that links have somewhere to land.

| Kind | Count |
|---|---|
| rule | 5 |
| state-machine | 4 |
| system | 1 |
| use-case | 1 |

## Relations

| Relation | Count |
|---|---|
| mentions | 4 |
| uses | 2 |

## The graph

```mermaid
flowchart LR
    n0["Compare a dashboard screen with it<br/>use-case"]
    n1["Dashboard developer<br/>actor"]
    n2["CostState lifecycle<br/>state-machine"]
    n3["Prototype figures are invented<br/>rule"]
    n4["Prototype filters do not filter th<br/>rule"]
    n5["Prototype rescan is staged<br/>rule"]
    n6["Prototype session table shows at m<br/>rule"]
    n7["Prototype splits session cost acro<br/>rule"]
    n8["RateState lifecycle<br/>state-machine"]
    n9["SpanKind lifecycle<br/>state-machine"]
    n10["SpanStatus lifecycle<br/>state-machine"]
    n11["Web prototype<br/>system"]
    n0 -->|uses| n1
    n0 -->|mentions| n1
    classDef k_actor fill:#fff2cc,stroke:#222222,color:#222222
    class n1 k_actor
    classDef k_rule fill:#e1d5e7,stroke:#222222,color:#222222
    class n3,n4,n5,n6,n7 k_rule
    classDef k_statemachine fill:#ffe6cc,stroke:#222222,color:#222222
    class n2,n8,n9,n10 k_statemachine
    classDef k_system fill:#dae8fc,stroke:#222222,color:#222222
    class n11 k_system
    classDef k_usecase fill:#fff2cc,stroke:#222222,color:#222222
    class n0 k_usecase
```

The full slice is in `ch-localtokenomics-web-src-prototype.jsonld` beside this note. Project terms are the primary labels; ArchiMate, DDD, schema.org and Dublin Core terms annotate them.
