---
title: Metric info interaction flow
aliases: []
tags: [diagram, mermaid, screen-flow]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/components/*]
sources: [docs/brain/architecture/diagrams/metric-info-interaction.mmd]
chunk: ch-localtokenomics-web-src-components
authored: true
node_citations:
  metric-info-interaction:
    start: ['web/src/components/metric-info.tsx:193-205', 'web/src/components/stat.tsx:101-103']
    d1: ['web/src/components/metric-info.tsx:35-42', 'web/src/components/metric-info.tsx:134-136', 'web/src/components/metric-info.tsx:141-143']
    s1: ['web/src/components/metric-info.tsx:35-42']
    s2: ['web/src/components/metric-info.tsx:134-136']
    s3: ['web/src/components/metric-info.tsx:141-143']
    s4: ['web/src/components/metric-info.tsx:11-13', 'web/src/components/metric-info.tsx:88-94']
    s5: ['web/src/components/metric-info.tsx:134-136']
    s6: ['web/src/components/metric-info.tsx:141-143']
    open: ['web/src/components/metric-info.tsx:151-155']
    d2: ['web/src/components/metric-info.tsx:15-18']
    s7: ['web/src/components/metric-info.tsx:165-165']
    s8: ['web/src/components/metric-info.tsx:168-183']
    d3: ['web/src/components/metric-info.tsx:100-107', 'web/src/components/metric-info.tsx:116-123']
    s9: ['web/src/components/metric-info.tsx:100-107']
    s10: ['web/src/components/metric-info.tsx:141-143']
    s11: ['web/src/components/metric-info.tsx:116-123']
    done: ['web/src/components/metric-info.tsx:162-162']
---

# Metric info interaction flow

This flow shows how a reader gets an explanation for a number or a badge. The box opens by hover, keyboard focus or tap, and it closes without stealing focus. This matters because almost every figure on the dashboard hangs an explanation on this one component.

## What the diagram shows

The info glyph is a small letter i drawn next to a label, and the stat card wraps it in the info box when it has an explanation. `web/src/components/metric-info.tsx:193-205` `web/src/components/stat.tsx:101-103`

One listener on the page records the last pointer position for every info box. `web/src/components/metric-info.tsx:35-42`

Each box checks that position every 100 ms, and when the pointer has stayed on the trigger or on the box for 400 ms it opens. `web/src/components/metric-info.tsx:11-13` `web/src/components/metric-info.tsx:88-94`

Keyboard focus on the trigger opens the box at once, and a click or tap toggles it. `web/src/components/metric-info.tsx:134-136` `web/src/components/metric-info.tsx:141-143`

The box opens on the right of the trigger and moves away from the screen edge when it would not fit. `web/src/components/metric-info.tsx:151-155`

A simple box shows one paragraph, and a metric box shows the meaning and then the formula, computed value, provenance and caveats that were supplied. `web/src/components/metric-info.tsx:165-165` `web/src/components/metric-info.tsx:168-183`

The box closes when the pointer has been outside both the trigger and the box for 250 ms and the trigger is not focused. `web/src/components/metric-info.tsx:100-107`

Any other close request from the popover resets the focus flag and the timer. `web/src/components/metric-info.tsx:116-123`

The box never hands focus back to the trigger when it closes, because the focus handler of the trigger would reopen it at once. `web/src/components/metric-info.tsx:162-162`

A test opens the box by click and checks the text. `web/src/components/metric-info.test.tsx:7-7`

## Capability and related functionality

The flow realises the on demand explanation of metrics and badges. The component is drawn in [[Shared components C4]] and [[Dashboard component composition]]. Its tests are in [[Web UI components Tests]]. Its popover comes from [[Web ui UI components Overview]]. The page level screens that use it are described in [[Web Overview]].


## Metric info interaction flow

%% generated:diagram-metric-info-interaction start (do not edit; run brain docs generate) %%
```mermaid
flowchart TD
    start(["Reader sees an info glyph or an explained badge"]):::startNode
    d1{"How does the reader reach it?"}:::decision
    s1["Pointer rests on the trigger or the box"]:::step
    s2["Keyboard focus lands on the trigger"]:::step
    s3["Reader clicks or taps the trigger"]:::step
    s4["A 100 ms poll counts 400 ms of pointer time"]:::step
    s5["Box opens at once"]:::step
    s6["Box toggles open or closed"]:::step
    open["Box is open on the right of the trigger"]:::step
    d2{"Which content kind?"}:::decision
    s7["One paragraph of text"]:::step
    s8["Meaning, formula, computed value, provenance, caveats, each only when given"]:::step
    d3{"How does it close?"}:::decision
    s9["Pointer outside both for 250 ms and trigger not focused"]:::step
    s10["Reader clicks the trigger again"]:::step
    s11["The popover reports a close request"]:::step
    done(["Box closed, focus is not handed back"]):::ok

    start --> d1
    d1 -->|hover| s1
    d1 -->|keyboard| s2
    d1 -->|click or tap| s3
    s1 --> s4
    s4 --> open
    s2 --> s5
    s5 --> open
    s3 --> s6
    s6 --> open
    open --> d2
    d2 -->|simple| s7
    d2 -->|metric| s8
    s7 --> d3
    s8 --> d3
    d3 -->|pointer leaves| s9
    d3 -->|second click| s10
    d3 -->|other| s11
    s9 --> done
    s10 --> done
    s11 --> done

    subgraph Legend
        direction LR
        zlegend_a(["Start"]):::startNode
        zlegend_b["Step"]:::step
        zlegend_c{"Decision, arrows are labelled"}:::decision
        zlegend_d(["End"]):::ok
        zlegend_a ~~~ zlegend_b ~~~ zlegend_c ~~~ zlegend_d
    end

    classDef startNode fill:#fff2cc,stroke:#222222,color:#222222
    classDef step fill:#dae8fc,stroke:#222222,color:#222222
    classDef decision fill:#ffffff,stroke:#222222,color:#222222
    classDef ok fill:#d5e8d4,stroke:#222222,color:#222222
```
%% generated:diagram-metric-info-interaction end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/components/metric-info.tsx:35-42` | Shared pointer listener |
> | `web/src/components/metric-info.tsx:11-13` | Timing constants |
> | `web/src/components/metric-info.tsx:88-94` | Open after 400 ms |
> | `web/src/components/metric-info.tsx:134-136` | Open on focus |
> | `web/src/components/metric-info.tsx:141-143` | Toggle on click |
> | `web/src/components/metric-info.tsx:151-155` | Popover placement |
> | `web/src/components/metric-info.tsx:100-107` | Close after 250 ms outside |
> | `web/src/components/metric-info.tsx:162-162` | No focus return |
> | `web/src/components/metric-info.test.tsx:7-7` | Click test |
