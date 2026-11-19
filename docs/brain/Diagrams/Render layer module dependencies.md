---
title: Render layer module dependencies
aliases: []
tags: [diagram, mermaid, module-dependency]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/render/**]
verified-against: 15259010c74a
sources: [docs/brain/architecture/diagrams/render-imports.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost-render
authored: true
node_citations:
  render-imports:
    cli: ['src/ai_usage_cost/cli.py:17-22']
    terminal: ['src/ai_usage_cost/render/terminal.py:3-7']
    png: ['src/ai_usage_cost/render/png.py:7-13']
    aggregate: ['src/ai_usage_cost/aggregate.py:11-13']
    models: ['src/ai_usage_cost/aggregate.py:11-11']
    pricing: ['src/ai_usage_cost/aggregate.py:12-12']
    sourcesbase: ['src/ai_usage_cost/aggregate.py:13-13']
    rich: ['src/ai_usage_cost/render/terminal.py:3-5']
    mpl: ['src/ai_usage_cost/render/png.py:7-11']
approved-by: human
approved-at: '2026-11-19T06:47:07+00:00'
---

# Render layer module dependencies

This view shows what the render files import. They depend on the report code and on two third party libraries, and no file outside the layer imports them except the command line. A maintainer can change how output looks without touching how cost is computed.

## What the diagram shows

The command line module imports the terminal renderer at the top of the file `src/ai_usage_cost/cli.py:22-22`, and imports the picture writer inside the export command, so only that command loads it `src/ai_usage_cost/cli.py:190-190`. It also imports the report type `src/ai_usage_cost/cli.py:17-17`.

The terminal renderer imports the report and bucket types from the report module and three parts of the rich library `src/ai_usage_cost/render/terminal.py:3-7`.

The picture writer imports the report type and the matplotlib library `src/ai_usage_cost/render/png.py:7-13`.

The report module imports the shared models, the pricing matcher and a helper from the sources base `src/ai_usage_cost/aggregate.py:11-13`. It does not import the render layer.

No cycle exists between these files. The generated folder view in [[Ai usage cost render Diagrams]] shows a loop only because the command line module and the report module sit in the parent folder of the render folder.

## Capability and related functionality

The capability is a clear boundary: the layer sits between the command line and the report code. The component view is [[Render layer components]] and the one page summary is [[Render layer mind map]].

## Render layer module dependencies

%% generated:diagram-render-imports start (do not edit; run brain docs generate) %%
```mermaid
flowchart TD
    subgraph cmd["Command line layer"]
        cli["cli.py"]:::mod
    end
    subgraph render["Render layer"]
        terminal["render/terminal.py"]:::mod
        png["render/png.py"]:::mod
    end
    subgraph report["Report layer"]
        aggregate["aggregate.py"]:::mod
        models["models.py"]:::mod
        pricing["pricing.py"]:::mod
        sourcesbase["sources/base.py"]:::mod
    end
    rich["rich"]:::external
    mpl["matplotlib"]:::external

    cli --> terminal
    cli -.-> png
    cli --> aggregate
    terminal --> aggregate
    png --> aggregate
    terminal --> rich
    png --> mpl
    aggregate --> models
    aggregate --> pricing
    aggregate --> sourcesbase

    subgraph Legend
        direction LR
        zl1["Box: a module, an arrow from A to B means A imports B"]:::mod
        zl2["Dashed arrow: an import inside a function, run only when that command runs"]:::mod
        zl3["Grey dashed box: a third party package"]:::external
        zl4["Red arrow: a cycle. None exists between these files"]:::mod
        zl1 ~~~ zl2
        zl2 ~~~ zl3
        zl3 ~~~ zl4
    end

    classDef mod fill:#dae8fc,stroke:#222222,color:#111111
    classDef external fill:#e6e6e6,stroke:#222222,stroke-dasharray:5 3,color:#111111
```
%% generated:diagram-render-imports end %%

%% generated:node-citations-render-imports start (do not edit; run brain docs generate) %%
### Node citations

- cli: `src/ai_usage_cost/cli.py:17-22`
- terminal: `src/ai_usage_cost/render/terminal.py:3-7`
- png: `src/ai_usage_cost/render/png.py:7-13`
- aggregate: `src/ai_usage_cost/aggregate.py:11-13`
- models: `src/ai_usage_cost/aggregate.py:11-11`
- pricing: `src/ai_usage_cost/aggregate.py:12-12`
- sourcesbase: `src/ai_usage_cost/aggregate.py:13-13`
- rich: `src/ai_usage_cost/render/terminal.py:3-5`
- mpl: `src/ai_usage_cost/render/png.py:7-11`
%% generated:node-citations-render-imports end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `src/ai_usage_cost/cli.py:17-22` | Command line imports |
> | `src/ai_usage_cost/cli.py:190-190` | Import inside the export command |
> | `src/ai_usage_cost/render/terminal.py:3-7` | Terminal renderer imports |
> | `src/ai_usage_cost/render/png.py:7-13` | Picture writer imports |
> | `src/ai_usage_cost/aggregate.py:11-13` | Report module imports |
