---
title: Web prototype Overview
aliases: []
tags: [module, overview]
area: application
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/prototype/**]
verified-against: e5313fbd7062
chunk: ch-localtokenomics-web-src-prototype
---

# Web prototype Overview

What Web prototype is made of and how it connects to the rest of the code.

## How it works

Web prototype holds 10 source files and 3215 lines. The most depended-on files are `web/src/prototype/data.ts`, `web/src/prototype/Gallery.tsx`, `web/src/prototype/OverviewScreen.tsx`. It uses Web Overview, Web UI components Overview, Web ui UI components Overview. No other chunk depends on it.

The purpose column quotes each file's own header comment where it has one. Every file is cited by its full line range, and every public name by the line that declares it.

## Status: prototype only

Everything in this chunk is a design reference, not part of the shipped product. The folder holds a second browser app that mirrors the four dashboard screens against invented numbers, plus a page that shows the design system parts. The repository's own migration guide calls the folder "reference screens + mock data" with the status "read only" `web/src/design-system/MIGRATION.md:63-63`, and tells a porter not to import from it but to "copy the composition, not the module" `web/src/design-system/MIGRATION.md:38-40`.

The shipped dashboard is a different entry point. Its page loads the main entry script `web/index.html:26-26`, which renders `App` `web/src/main.tsx:7-13`. `App` fetches real metadata, rates and reports from the local API `web/src/App.tsx:168-169` `web/src/App.tsx:186-186` and switches between the Overview, Sessions, Sources and Pricing views `web/src/App.tsx:331-338`. The prototype has its own page that loads `web/src/prototype/main.tsx` `web/prototype.html:25-25`.

The production build does not include the prototype. The Vite configuration names no extra build input, and writes to the Python package folder `web/vite.config.ts:14-17`. The migration guide states that `prototype.html` is "deliberately excluded" from the production build `web/src/design-system/MIGRATION.md:419-421`, and that `npm run dev` serves the app at the root and the prototype at `/prototype.html` `web/src/design-system/MIGRATION.md:413-417`. During development the dev server proxies `/api` to a local port `web/vite.config.ts:18-26`, but nothing in the prototype calls the API.

## How the prototype is assembled

The entry script mounts `Prototype` in strict mode and loads the shared theme stylesheet `web/src/prototype/main.tsx:1-11`. The HTML page sets the light or dark theme before first paint from a stored preference or the system setting `web/prototype.html:7-21`.

`Prototype` is the shell. It keeps the active tab, whether the mobile filter drawer is open and a scanning flag in local state `web/src/prototype/Prototype.tsx:21-24`. The tabs are the four screens plus a fifth called "Design system" `web/src/prototype/Prototype.tsx:14-18`. The header shows the product name and a theme toggle `web/src/prototype/Prototype.tsx:34-96`. A tab other than the gallery renders `Screens`, and the gallery tab renders `Gallery` `web/src/prototype/Prototype.tsx:98-107`.

Two header elements are staged. The "Rescan logs" button only flips the scanning flag for 900 milliseconds and reads no logs `web/src/prototype/Prototype.tsx:26-29`. The text "scanned 2 min ago" is a fixed string `web/src/prototype/Prototype.tsx:80-82`.

`Screens` holds the filter state and the open session, draws the filter rail, the chip row and the active screen `web/src/prototype/Screens.tsx:266-378`. The four screen names are declared once `web/src/prototype/Screens.tsx:41-48`. The screen is chosen by a plain conditional `web/src/prototype/Screens.tsx:360-368`.

## What is faked

All figures come from `data.ts`. The reference date is a fixed day in September 2026 `web/src/prototype/data.ts:3-3`, and the 30 day axis is computed from a fixed start `web/src/prototype/data.ts:5-7`. Daily series are shaped by a sine and cosine function with a weekend dip `web/src/prototype/data.ts:9-13`. Headline totals such as cost, requests, sessions and the rate date are literal numbers `web/src/prototype/data.ts:617-632`. The session list is a few hand written sessions padded with scaled copies until it reaches 184 rows `web/src/prototype/data.ts:698-742`.

The data file takes only its type names from the real API module `web/src/prototype/data.ts:1-1`. The migration guide describes the file as mirroring "a subset" of the real data shapes `web/src/design-system/MIGRATION.md:53-53`.

Several behaviours look live but are not:

- The filter rail edits state and produces chips `web/src/prototype/Screens.tsx:277-340`, but the screens are rendered without any filter value `web/src/prototype/Screens.tsx:360-368`, so filtering changes nothing on screen.
- The session drawer splits a session's cost across the four token buckets with fixed weights `web/src/prototype/Screens.tsx:50-69`. The real app has its own economics tab, and the migration guide calls the drawer only a "partial" reference `web/src/design-system/MIGRATION.md:81-81`.
- The drawer's "Reprice this model" block prints a rate override with zero prices for the chosen model `web/src/prototype/Screens.tsx:253-257`.

## The screens and their shipped counterparts

The migration guide pairs each prototype file with the shipped file it is the reference for `web/src/design-system/MIGRATION.md:78-84`.

| Prototype file | What it shows | Shipped counterpart named by the guide |
|---|---|---|
| `web/src/prototype/OverviewScreen.tsx` | Detected sources, KPI row, cost over time, cost by model, token mix, cache savings, cost by project `web/src/prototype/OverviewScreen.tsx:370-386` | `web/src/Overview.tsx` |
| `web/src/prototype/SessionsScreen.tsx` | Sortable session table, capped at a row limit, with a card layout on phones `web/src/prototype/SessionsScreen.tsx:82-103` | `web/src/Sessions.tsx` |
| `web/src/prototype/SourcesScreen.tsx` | Readers that found logs, readers that found nothing, scan warnings `web/src/prototype/SourcesScreen.tsx:8-95` | `web/src/Sources.tsx` |
| `web/src/prototype/PricingScreen.tsx` | Rate table, provider multipliers, models with tokens and no rate `web/src/prototype/PricingScreen.tsx:208-218` | `web/src/Pricing.tsx` |
| `web/src/prototype/Rail.tsx` | Filter rail, a fixed column on wide screens and a slide-in sheet on narrow ones `web/src/prototype/Rail.tsx:245-276` | `web/src/FilterRail.tsx` |
| `web/src/prototype/Prototype.tsx` and `Screens.tsx` | Header, chip row, session drawer | `web/src/Header.tsx`, `web/src/App.tsx`, `web/src/SessionWorkspace.tsx` |

The session table sorts a copy of all sessions and then shows only the first `SESSION_LIMIT` rows `web/src/prototype/SessionsScreen.tsx:87-96`, and the limit is 120 `web/src/prototype/data.ts:744-744`. The pricing screen computes cache prices from a provider rule or a default multiplier and marks a model free when both prices are zero `web/src/prototype/PricingScreen.tsx:33-44`. Models with no spend are hidden until a reveal count is raised `web/src/prototype/PricingScreen.tsx:46-52`. The sources screen hides readers that found nothing inside a collapsed panel `web/src/prototype/SourcesScreen.tsx:51-80`.

## Parts that exist only in the prototype

The "Design system" tab is a component gallery. It is one long page of sections for colour tokens, typography, actions, inputs, data display, feedback, domain components and trace components `web/src/prototype/Gallery.tsx:173-173` `web/src/prototype/Gallery.tsx:226-226` `web/src/prototype/Gallery.tsx:249-249` `web/src/prototype/Gallery.tsx:346-346` `web/src/prototype/Gallery.tsx:424-424` `web/src/prototype/Gallery.tsx:477-477` `web/src/prototype/Gallery.tsx:547-547` `web/src/prototype/Gallery.tsx:621-621`. The shipped app has no counterpart.

`CapabilityGrid`, the "What can be known here" block of the session drawer `web/src/prototype/Screens.tsx:212-214`, is used by the prototype and the gallery `web/src/prototype/Gallery.tsx:647-647`. The migration guide records that the shipped app does not use it and shows capabilities as a row of provenance badges and the Sources matrix instead `web/src/design-system/MIGRATION.md:365-365`.

## Documentation that disagrees with the code

The design system README says the shipping dashboard "still runs on the older `src/ds/` CSS system" `web/src/design-system/README.md:142-147`. The shipped entry point already imports the new theme stylesheet `web/src/main.tsx:5-5`, and the old CSS folder no longer exists in the web source tree. The code wins: the shipped dashboard uses the same design system the prototype shows. The README and the migration guide's step list read as older than the code, and this chunk does not change them.

## Reference

%% generated:chunk-files start (do not edit; run brain docs generate) %%
### Files

| File | Purpose | Lines | Imports | Imported by | Code |
|---|---|---|---|---|---|
| `web/src/prototype/Gallery.tsx` | - | 659 | 30 | 1 | [[web/src/prototype/Gallery.tsx]] `web/src/prototype/Gallery.tsx:1-659` |
| `web/src/prototype/OverviewScreen.tsx` | - | 386 | 10 | 1 | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:1-386` |
| `web/src/prototype/PricingScreen.tsx` | - | 218 | 9 | 1 | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:1-218` |
| `web/src/prototype/Prototype.tsx` | - | 112 | 9 | 1 | [[web/src/prototype/Prototype.tsx]] `web/src/prototype/Prototype.tsx:1-112` |
| `web/src/prototype/Rail.tsx` | - | 276 | 12 | 1 | [[web/src/prototype/Rail.tsx]] `web/src/prototype/Rail.tsx:1-276` |
| `web/src/prototype/Screens.tsx` | - | 378 | 15 | 1 | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:1-378` |
| `web/src/prototype/SessionsScreen.tsx` | - | 249 | 11 | 1 | [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:1-249` |
| `web/src/prototype/SourcesScreen.tsx` | - | 95 | 6 | 1 | [[web/src/prototype/SourcesScreen.tsx]] `web/src/prototype/SourcesScreen.tsx:1-95` |
| `web/src/prototype/data.ts` | - | 831 | 1 | 8 | [[web/src/prototype/data.ts]] `web/src/prototype/data.ts:1-831` |
| `web/src/prototype/main.tsx` | - | 11 | 1 | 0 | [[web/src/prototype/main.tsx]] `web/src/prototype/main.tsx:1-11` |
%% generated:chunk-files end %%

%% generated:chunk-interface start (do not edit; run brain docs generate) %%
### Public interface

| Name | Kind | File | Code |
|---|---|---|---|
| `TODAY` | const | `web/src/prototype/data.ts` | [[web/src/prototype/data.ts]] `web/src/prototype/data.ts:3` |
| `DAYS` | const | `web/src/prototype/data.ts` | [[web/src/prototype/data.ts]] `web/src/prototype/data.ts:5` |
| `ModelInfo` | interface | `web/src/prototype/data.ts` | [[web/src/prototype/data.ts]] `web/src/prototype/data.ts:15` |
| `MODELS` | const | `web/src/prototype/data.ts` | [[web/src/prototype/data.ts]] `web/src/prototype/data.ts:29` |
| `PRICED_MODELS` | const | `web/src/prototype/data.ts` | [[web/src/prototype/data.ts]] `web/src/prototype/data.ts:123` |
| `SeriesPoint` | interface | `web/src/prototype/data.ts` | [[web/src/prototype/data.ts]] `web/src/prototype/data.ts:125` |
| `SERIES` | const | `web/src/prototype/data.ts` | [[web/src/prototype/data.ts]] `web/src/prototype/data.ts:136` |
| `CLIENTS` | const | `web/src/prototype/data.ts` | [[web/src/prototype/data.ts]] `web/src/prototype/data.ts:152` |
| `PROJECTS` | const | `web/src/prototype/data.ts` | [[web/src/prototype/data.ts]] `web/src/prototype/data.ts:161` |
| `PrototypeSession` | interface | `web/src/prototype/data.ts` | [[web/src/prototype/data.ts]] `web/src/prototype/data.ts:170` |
| `SourceRecord` | interface | `web/src/prototype/data.ts` | [[web/src/prototype/data.ts]] `web/src/prototype/data.ts:419` |
| `SOURCES` | const | `web/src/prototype/data.ts` | [[web/src/prototype/data.ts]] `web/src/prototype/data.ts:435` |
| `Gallery` | function | `web/src/prototype/Gallery.tsx` | [[web/src/prototype/Gallery.tsx]] `web/src/prototype/Gallery.tsx:161` |
| `OverviewScreen` | function | `web/src/prototype/OverviewScreen.tsx` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:370` |
| `PricingScreen` | function | `web/src/prototype/PricingScreen.tsx` | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:208` |
| `Prototype` | function | `web/src/prototype/Prototype.tsx` | [[web/src/prototype/Prototype.tsx]] `web/src/prototype/Prototype.tsx:20` |
| `FilterState` | interface | `web/src/prototype/Rail.tsx` | [[web/src/prototype/Rail.tsx]] `web/src/prototype/Rail.tsx:30` |
| `INITIAL_FILTERS` | const | `web/src/prototype/Rail.tsx` | [[web/src/prototype/Rail.tsx]] `web/src/prototype/Rail.tsx:46` |
| `isDirty` | function | `web/src/prototype/Rail.tsx` | [[web/src/prototype/Rail.tsx]] `web/src/prototype/Rail.tsx:62` |
| `RailContent` | function | `web/src/prototype/Rail.tsx` | [[web/src/prototype/Rail.tsx]] `web/src/prototype/Rail.tsx:80` |
| `FilterRail` | function | `web/src/prototype/Rail.tsx` | [[web/src/prototype/Rail.tsx]] `web/src/prototype/Rail.tsx:245` |
| `ScreenId` | type | `web/src/prototype/Screens.tsx` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:41` |
| `SCREEN_LABELS` | const | `web/src/prototype/Screens.tsx` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:43` |
| `Screens` | function | `web/src/prototype/Screens.tsx` | [[web/src/prototype/Screens.tsx]] `web/src/prototype/Screens.tsx:266` |
| `SessionsScreen` | function | `web/src/prototype/SessionsScreen.tsx` | [[web/src/prototype/SessionsScreen.tsx]] `web/src/prototype/SessionsScreen.tsx:82` |
| `SourcesScreen` | function | `web/src/prototype/SourcesScreen.tsx` | [[web/src/prototype/SourcesScreen.tsx]] `web/src/prototype/SourcesScreen.tsx:8` |
%% generated:chunk-interface end %%
