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

48 terms, of which 1 belong to other chunks and appear only so that links have somewhere to land.

| Kind | Count |
|---|---|
| actor | 2 |
| nfr | 2 |
| open-question | 3 |
| risk | 4 |
| rule | 21 |
| state-machine | 4 |
| system | 4 |
| use-case | 7 |

## Relations

| Relation | Count |
|---|---|
| uses | 12 |
| mentions | 4 |

## The graph

```mermaid
flowchart LR
    n0["Dashboard reader<br/>actor"]
    n1["Maintainer<br/>actor"]
    n2["Rebuild the dashboard bundle<br/>use-case"]
    n3["Compare a dashboard screen with it<br/>use-case"]
    n4["Dashboard developer<br/>actor"]
    n5["Develop the dashboard against live<br/>use-case"]
    n6["A production build replaces the co<br/>rule"]
    n7["A type error stops the dashboard b<br/>rule"]
    n8["Check list prices<br/>use-case"]
    n9["Inspect one session<br/>use-case"]
    n10["Rate a session outcome<br/>use-case"]
    n11["Read usage and cost for a period<br/>use-case"]
    n12["Automatic rescan every five minute<br/>rule"]
    n13["Cache price derivation<br/>rule"]
    n14["CostState lifecycle<br/>state-machine"]
    n15["Do not import from the prototype f<br/>rule"]
    n16["Keyboard and screen reader access <br/>nfr"]
    n17["Lint skips build output<br/>rule"]
    n18["Most shared components have no tes<br/>risk"]
    n19["Outcome notes are saved only when <br/>rule"]
    n20["Popover timing depends on a pollin<br/>risk"]
    n21["Prototype figures are invented<br/>rule"]
    n22["Prototype filters do not filter th<br/>rule"]
    n23["Prototype rescan is staged<br/>rule"]
    n24["Prototype session table shows at m<br/>rule"]
    n25["Prototype splits session cost acro<br/>rule"]
    n26["Question 3꞉ Does the DELETE sessio<br/>open-question"]
    n27["Question 4꞉ Is deleteSession reach<br/>open-question"]
    n28["Rate age notice thresholds<br/>rule"]
    n29["Rate row state<br/>rule"]
    n30["RateState lifecycle<br/>state-machine"]
    n31["Reduced motion is respected<br/>nfr"]
    n32["Reported cost divergence threshold<br/>rule"]
    n33["Risk 1꞉ The dashboard client can w<br/>risk"]
    n34["Risk 2꞉ Most files in this chunk h<br/>risk"]
    n35["Session table row limit<br/>rule"]
    n36["SpanKind lifecycle<br/>state-machine"]
    n37["SpanStatus lifecycle<br/>state-machine"]
    n38["Sub cent money keeps four decimals<br/>rule"]
    n39["The prototype is excluded from the<br/>rule"]
    n8 -->|uses| n0
    n3 -->|uses| n4
    n3 -->|mentions| n4
    n5 -->|uses| n1
    n9 -->|uses| n0
    n10 -->|uses| n0
    n11 -->|uses| n0
    n2 -->|uses| n1
    n2 -->|uses| n7
    n2 -->|uses| n6
    classDef k_actor fill:#fff2cc,stroke:#222222,color:#222222
    class n0,n1,n4 k_actor
    classDef k_nfr fill:#e1d5e7,stroke:#222222,color:#222222
    class n16,n31 k_nfr
    classDef k_openquestion fill:#f5f5f5,stroke:#222222,color:#222222
    class n26,n27 k_openquestion
    classDef k_risk fill:#f8cecc,stroke:#222222,color:#222222
    class n18,n20,n33,n34 k_risk
    classDef k_rule fill:#e1d5e7,stroke:#222222,color:#222222
    class n6,n7,n12,n13,n15,n17,n19,n21,n22,n23,n24,n25,n28,n29,n32,n35,n38,n39 k_rule
    classDef k_statemachine fill:#ffe6cc,stroke:#222222,color:#222222
    class n14,n30,n36,n37 k_statemachine
    classDef k_usecase fill:#fff2cc,stroke:#222222,color:#222222
    class n2,n3,n5,n8,n9,n10,n11 k_usecase
```

The full slice is in `ch-localtokenomics-root.jsonld` beside this note. Project terms are the primary labels; ArchiMate, DDD, schema.org and Dublin Core terms annotate them.
