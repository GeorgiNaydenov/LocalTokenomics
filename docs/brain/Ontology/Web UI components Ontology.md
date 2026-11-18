---
title: Web UI components Ontology
aliases: []
tags: [overview, reference]
area: ontology
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: []
chunk: ch-localtokenomics-web-src-components
generated: true
---

# Web UI components Ontology

This is the part of the project's knowledge graph that the code in Web UI components defines. It shows what the code knows about, and how those things are linked to each other and to the rest of the project.

## What it contains

5 terms, of which 0 belong to other chunks and appear only so that links have somewhere to land.

| Kind | Count |
|---|---|
| nfr | 2 |
| open-question | 1 |
| risk | 2 |

## Relations

| Relation | Count |
|---|---|
| none yet | 0 |

## The graph

```mermaid
flowchart LR
    n0["Keyboard and screen reader access <br/>nfr"]
    n1["Most shared components have no tes<br/>risk"]
    n2["Popover timing depends on a pollin<br/>risk"]
    n3["Reduced motion is respected<br/>nfr"]
    n4["Why the Other series limit is twel<br/>open-question"]
    classDef k_nfr fill:#e1d5e7,stroke:#222222,color:#222222
    class n0,n3 k_nfr
    classDef k_openquestion fill:#f5f5f5,stroke:#222222,color:#222222
    class n4 k_openquestion
    classDef k_risk fill:#f8cecc,stroke:#222222,color:#222222
    class n1,n2 k_risk
```

The full slice is in `ch-localtokenomics-web-src-components.jsonld` beside this note. Project terms are the primary labels; ArchiMate, DDD, schema.org and Dublin Core terms annotate them.
