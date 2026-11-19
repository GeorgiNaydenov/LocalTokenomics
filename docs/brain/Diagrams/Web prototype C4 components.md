---
title: Web prototype C4 components
aliases: []
tags: [c4, diagram, mermaid]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/prototype/**]
verified-against: f7104a42d355
sources: [docs/brain/architecture/diagrams/web-prototype-c4.mmd]
chunk: ch-localtokenomics-web-src-prototype
authored: true
node_citations:
  web-prototype-c4:
    dev: ['web/src/design-system/MIGRATION.md:38-40']
    page: ['web/prototype.html:25-25', 'web/src/prototype/main.tsx:1-11']
    shell: ['web/src/prototype/Prototype.tsx:20-112']
    screens: ['web/src/prototype/Screens.tsx:266-378']
    rail: ['web/src/prototype/Rail.tsx:245-276']
    four: ['web/src/prototype/Screens.tsx:360-368']
    gallery: ['web/src/prototype/Gallery.tsx:161-173']
    mock: ['web/src/prototype/data.ts:617-632', 'web/src/prototype/data.ts:698-742']
    shared: ['web/src/prototype/Screens.tsx:3-24', 'web/src/App.tsx:14-18']
    shipped: ['web/src/main.tsx:3-13', 'web/index.html:26-26']
    api: ['web/src/App.tsx:168-169', 'web/src/App.tsx:186-186']
approved-by: human
approved-at: '2026-11-19T06:43:08+00:00'
---

# Web prototype C4 components

This view shows the experimental copy of the dashboard that lives beside the real one. It lets a designer or developer try the four screens and the design system against made up numbers, with no usage logs needed. It also shows that the real dashboard is a separate program, so nobody mistakes the mock screens for the product.

## What the diagram shows

A developer opens the prototype page on the development server, and that page loads the prototype entry script `web/prototype.html:25-25` `web/src/prototype/main.tsx:1-11`. The entry script mounts the `Prototype` shell, which holds the tabs, the theme toggle and the header buttons `web/src/prototype/Prototype.tsx:20-112`.

The shell shows either the design system page or the `Screens` component `web/src/prototype/Prototype.tsx:98-107`. `Screens` keeps the filter form state and the open session drawer, and draws the filter rail `web/src/prototype/Screens.tsx:266-378`. The rail is a fixed column on wide windows and a slide-in sheet on narrow ones `web/src/prototype/Rail.tsx:245-276`. `Screens` then renders one of the four reference screens `web/src/prototype/Screens.tsx:360-368`.

The screens and the rail read only from the mock data file. It holds literal totals and a generated list of sessions `web/src/prototype/data.ts:617-632` `web/src/prototype/data.ts:698-742`. No call to the local usage API appears in the prototype folder, so the API is drawn as an external system that the prototype never reaches.

Both the prototype and the shipped dashboard import the same shared components and design system `web/src/prototype/Screens.tsx:3-24` `web/src/App.tsx:14-18`. The shipped dashboard has its own entry script and its own page `web/src/main.tsx:3-13` `web/index.html:26-26`, and it does fetch real data from the API `web/src/App.tsx:168-169` `web/src/App.tsx:186-186`.

A developer porting a screen reads the matching prototype file and copies its layout into the real file. The migration guide says to copy the composition, not the module `web/src/design-system/MIGRATION.md:38-40`. That is the dashed arrow in the diagram.

## Capability and related functionality

The prototype realises one capability: a clickable, data free reference for how the dashboard screens and the design system should look. It serves the people who build the dashboard, not the people who read their costs. The notes around it are [[Web prototype Overview]] for the file by file explanation, [[Web prototype Diagrams]] for the generated import view, and Web Overview and Web UI components Overview for the shipped dashboard and the shared parts it uses.

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `web/prototype.html:25-25` | The prototype page loads its own entry script |
> | `web/src/prototype/main.tsx:1-11` | The entry script mounts the shell |
> | `web/src/prototype/Prototype.tsx:20-112` | The shell, with tabs, theme toggle and staged header buttons |
> | `web/src/prototype/Screens.tsx:266-378` | Filter state, chips, rail, active screen and session drawer |
> | `web/src/prototype/Screens.tsx:360-368` | The choice of one of the four screens |
> | `web/src/prototype/Rail.tsx:245-276` | The filter rail in its two layouts |
> | `web/src/prototype/Gallery.tsx:161-173` | The design system page |
> | `web/src/prototype/data.ts:617-632` | Literal mock totals |
> | `web/src/prototype/data.ts:698-742` | Generated mock sessions |
> | `web/src/App.tsx:14-18` | The shipped app imports the same shared parts |
> | `web/src/App.tsx:168-169` | The shipped app fetches metadata and rates |
> | `web/src/main.tsx:3-13` | The shipped entry script |
> | `web/src/design-system/MIGRATION.md:38-40` | Copy the layout, not the module |

## Web prototype C4 components

%% generated:diagram-web-prototype-c4 start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    dev(["Developer<br/>Person<br/>porting a screen"]):::person
    subgraph proto["Web prototype: web/src/prototype (dev server only, not in the build)"]
        page["prototype.html + main.tsx<br/>Container: entry page<br/>React"]:::system
        shell["Prototype<br/>Component: header, tabs, theme<br/>React"]:::system
        screens["Screens<br/>Component: filters, chips, session drawer<br/>React"]:::system
        rail["FilterRail<br/>Component: filter form<br/>React"]:::system
        four["Overview, Sessions, Sources, Pricing<br/>Component: four reference screens<br/>React"]:::system
        gallery["Gallery<br/>Component: design system page<br/>React"]:::system
        mock[("data.ts<br/>Mock data: invented sessions,<br/>rates and totals<br/>TypeScript")]:::data
    end
    shared["Shared components and design system<br/>web/src/components, web/src/design-system<br/>Used by the prototype and the shipped app"]:::system
    shipped["Shipped dashboard<br/>web/index.html, web/src/main.tsx, App.tsx<br/>Container: real screens"]:::system
    api["Local usage API<br/>External system: never called by the prototype"]:::external

    dev -->|opens /prototype.html| page
    page --> shell
    shell --> screens
    shell --> gallery
    screens --> rail
    screens --> four
    four --> mock
    rail --> mock
    screens --> shared
    gallery --> shared
    shipped --> shared
    shipped -->|fetches reports| api
    dev -.->|copies the layout, not the module| shipped

    subgraph Legend
        direction LR
        zl1(["Person: yellow stadium"]):::person
        zl2["Component or container: blue box, part of this system"]:::system
        zl3[("Data store: green cylinder, mock data only")]:::data
        zl4["External system: grey box, dashed border"]:::external
        zl5["Solid arrow: import or call. Dashed arrow: manual copy by a person"]:::system
        zl1 ~~~ zl2
        zl2 ~~~ zl3
        zl3 ~~~ zl4
        zl4 ~~~ zl5
    end

    classDef person fill:#fff2cc,stroke:#222222,color:#111111
    classDef system fill:#dae8fc,stroke:#222222,color:#111111
    classDef data fill:#d5e8d4,stroke:#222222,color:#111111
    classDef external fill:#e6e6e6,stroke:#222222,stroke-dasharray:5 3,color:#111111
```
%% generated:diagram-web-prototype-c4 end %%
