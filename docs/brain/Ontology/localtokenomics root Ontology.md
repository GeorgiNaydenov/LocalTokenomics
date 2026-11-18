---
title: localtokenomics root Ontology
aliases: []
tags: [overview, reference]
area: ontology
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: []
chunk: ch-localtokenomics-root
generated: true
---

# localtokenomics root Ontology

This is the part of the project's knowledge graph that the code in localtokenomics root defines. It shows what the code knows about, and how those things are linked to each other and to the rest of the project.

## What it contains

16 terms, of which 1 belong to other chunks and appear only so that links have somewhere to land.

| Kind | Count |
|---|---|
| actor | 1 |
| rule | 10 |
| system | 1 |
| use-case | 3 |

## Relations

| Relation | Count |
|---|---|
| uses | 8 |
| mentions | 4 |

## The graph

```mermaid
flowchart LR
    n0["Maintainer<br/>actor"]
    n1["Rebuild the dashboard bundle<br/>use-case"]
    n2["Compare a dashboard screen with it<br/>use-case"]
    n3["Dashboard developer<br/>actor"]
    n4["Develop the dashboard against live<br/>use-case"]
    n5["A production build replaces the co<br/>rule"]
    n6["A type error stops the dashboard b<br/>rule"]
    n7["Do not import from the prototype f<br/>rule"]
    n8["Lint skips build output<br/>rule"]
    n9["Prototype figures are invented<br/>rule"]
    n10["Prototype filters do not filter th<br/>rule"]
    n11["Prototype rescan is staged<br/>rule"]
    n12["Prototype session table shows at m<br/>rule"]
    n13["Prototype splits session cost acro<br/>rule"]
    n14["The prototype is excluded from the<br/>rule"]
    n15["Web prototype<br/>system"]
    n2 -->|uses| n3
    n2 -->|mentions| n3
    n4 -->|uses| n0
    n1 -->|uses| n0
    n1 -->|uses| n6
    n1 -->|uses| n5
    classDef k_actor fill:#fff2cc,stroke:#222222,color:#222222
    class n0,n3 k_actor
    classDef k_rule fill:#e1d5e7,stroke:#222222,color:#222222
    class n5,n6,n7,n8,n9,n10,n11,n12,n13,n14 k_rule
    classDef k_system fill:#dae8fc,stroke:#222222,color:#222222
    class n15 k_system
    classDef k_usecase fill:#fff2cc,stroke:#222222,color:#222222
    class n1,n2,n4 k_usecase
```

The full slice is in `ch-localtokenomics-root.jsonld` beside this note. Project terms are the primary labels; ArchiMate, DDD, schema.org and Dublin Core terms annotate them.
