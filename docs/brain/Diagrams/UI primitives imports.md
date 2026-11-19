---
title: UI primitives imports
aliases: []
tags: [diagram, mermaid, module-dependency]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/components/ui/*]
sources: [docs/brain/architecture/diagrams/ui-primitives-imports.mmd]
chunk: ch-localtokenomics-web-src-components-ui
authored: true
node_citations:
  ui-primitives-imports:
    dialog: ['web/src/components/ui/dialog.tsx:50-82']
    button: ['web/src/components/ui/button.tsx:40-61']
    toggleGroup: ['web/src/components/ui/toggle-group.tsx:18-47']
    toggle: ['web/src/components/ui/toggle.tsx:30-44']
    chart: ['web/src/components/ui/chart.tsx:39-79']
    sonnerFile: ['web/src/components/ui/sonner.tsx:12-37']
    others: ['web/src/components/ui/badge.tsx:28-45', 'web/src/components/ui/tabs.tsx:8-25', 'web/src/components/ui/collapsible.tsx:3-7']
    cn: ['web/src/components/ui/skeleton.tsx:1-1']
    theme: ['web/src/components/ui/sonner.tsx:10-10']
    radix: ['web/src/components/ui/button.tsx:4-4', 'web/src/components/ui/dialog.tsx:6-6', 'web/src/components/ui/tabs.tsx:6-6']
    cva: ['web/src/components/ui/button.tsx:2-2', 'web/src/components/ui/badge.tsx:2-2', 'web/src/components/ui/alert.tsx:2-2']
    lucide: ['web/src/components/ui/dialog.tsx:5-5']
    recharts: ['web/src/components/ui/chart.tsx:3-3']
    sonnerLib: ['web/src/components/ui/sonner.tsx:8-8']
---

# UI primitives imports

This graph shows what the basic interface parts import. It makes clear that they depend only on a few libraries and one class name helper, never on the dashboard components built from them. A developer can therefore change a primitive without a risk of a circular dependency.

## What the diagram shows

The dialog imports the button for its footer close action, and the toggle group imports the toggle variants. These are the only two imports between files of this folder. `web/src/components/ui/dialog.tsx:8-8` `web/src/components/ui/toggle-group.tsx:6-6`

Nearly every file imports the class name helper from the design system folder. `web/src/components/ui/button.tsx:3-3` `web/src/components/ui/chart.tsx:2-2` `web/src/components/ui/skeleton.tsx:1-1`

Most files build on one Radix part, and the button, badge and alert declare their variants with class-variance-authority. `web/src/components/ui/button.tsx:4-4` `web/src/components/ui/dialog.tsx:6-6` `web/src/components/ui/tabs.tsx:6-6` `web/src/components/ui/button.tsx:2-2` `web/src/components/ui/badge.tsx:2-2` `web/src/components/ui/alert.tsx:2-2`

The dialog and the toast host import icons from lucide-react. `web/src/components/ui/dialog.tsx:5-5` `web/src/components/ui/sonner.tsx:7-7`

The chart file imports recharts, and the toast host imports the sonner library and the theme hook of the web source. `web/src/components/ui/chart.tsx:3-3` `web/src/components/ui/sonner.tsx:8-8` `web/src/components/ui/sonner.tsx:10-10`

No file of this folder imports a file of the shared components folder, so there is no cycle between the two.

## Capability and related functionality

The graph realises the file level view of the primitives layer. The folder level view is [[Web ui UI components Diagrams]], and the grouped view is [[UI primitives C4]]. The components above this layer have their own import graph in [[Shared components imports]].


## UI primitives imports

%% generated:diagram-ui-primitives-imports start (do not edit; run brain docs generate) %%
```mermaid
flowchart TD
    subgraph Own["Files of this folder"]
        dialog["dialog.tsx"]:::module
        button["button.tsx"]:::module
        toggleGroup["toggle-group.tsx"]:::module
        toggle["toggle.tsx"]:::module
        chart["chart.tsx"]:::module
        sonnerFile["sonner.tsx"]:::module
        others["Other 19 primitives"]:::module
    end
    cn["design-system/cn"]:::external
    theme["theme"]:::external
    radix["radix-ui"]:::external
    cva["class-variance-authority"]:::external
    lucide["lucide-react"]:::external
    recharts["recharts"]:::external
    sonnerLib["sonner"]:::external

    dialog --> button
    toggleGroup --> toggle
    dialog --> cn
    button --> cn
    toggle --> cn
    toggleGroup --> cn
    chart --> cn
    others --> cn
    button --> radix
    toggle --> radix
    toggleGroup --> radix
    dialog --> radix
    others --> radix
    button --> cva
    toggle --> cva
    others --> cva
    dialog --> lucide
    sonnerFile --> lucide
    others --> lucide
    chart --> recharts
    sonnerFile --> sonnerLib
    sonnerFile --> theme

    subgraph Legend
        direction LR
        zlegend_a["Module: one file or a named group"]:::module
        zlegend_b["Outside this folder"]:::external
        zlegend_c["Red arrow: import cycle, none found here"]:::cycle
        zlegend_a ~~~ zlegend_b ~~~ zlegend_c
    end

    classDef module fill:#dae8fc,stroke:#222222,color:#222222
    classDef external fill:#f5f5f5,stroke:#666666,color:#222222,stroke-dasharray:5 3
    classDef cycle fill:#f8cecc,stroke:#b85450,color:#222222
```
%% generated:diagram-ui-primitives-imports end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/src/components/ui/dialog.tsx:8-8` | Dialog imports the button |
> | `web/src/components/ui/toggle-group.tsx:6-6` | Toggle group imports the toggle variants |
> | `web/src/components/ui/button.tsx:3-3` | Class name helper |
> | `web/src/components/ui/button.tsx:2-2` | Variants |
> | `web/src/components/ui/chart.tsx:3-3` | recharts import |
> | `web/src/components/ui/sonner.tsx:10-10` | Theme hook import |
