---
title: localtokenomics root Overview
aliases: []
tags: [module, overview]
area: application
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/*]
verified-against: 696b7c3b3902
chunk: ch-localtokenomics-root
approved-by: human
approved-at: '2026-11-18T19:00:53+00:00'
---

# localtokenomics root Overview

What localtokenomics root is made of and how it connects to the rest of the code.

## How it works

localtokenomics root holds 75 source files and 15505 lines, with 188 tests that live in it or import its files. The most depended-on files are `web/src/design-system/cn.ts`, `web/src/api.ts`, `web/src/format.ts`. It depends on no other chunk. No other chunk depends on it.

The purpose column quotes each file's own header comment where it has one. Every file is cited by its full line range, and every public name by the line that declares it.

## What the root holds

The root of the repository ties two projects into one package. The Python package `ai-usage-cost` reads the usage logs and prices them, and the web folder holds the React dashboard that shows the result. The package metadata names the project, its version and the one console command it installs. `pyproject.toml:1-4` `pyproject.toml:29-30`

The README describes the product as a local, read-only tool that works offline, needs no API key and uploads nothing. `README.md:9-28` Python 3.11 or newer is required. `pyproject.toml:6`

The package has five required libraries: pydantic, typer, rich, fastapi and uvicorn. `pyproject.toml:7-13` Everything else is an optional extra, so a plain install stays small. The extras are png charts, a SQL browser, alerts and a text interface, plus a dev group of test and lint tools. `pyproject.toml:15-27`

The wheel is built with hatchling and ships only `src/ai_usage_cost`. `pyproject.toml:32-37` The dashboard build writes into that package folder, so a built dashboard travels inside the wheel. `web/vite.config.ts:14-17`

## The web build configuration

The file web/vite.config.ts configures Vite for the dashboard. The base path is relative, so the built pages load from whichever URL the Python server mounts them on. `web/vite.config.ts:7` The React and Tailwind plugins are enabled. `web/vite.config.ts:8` The alias `@` points at the dashboard source folder, and web/tsconfig.json repeats the same alias for the type checker, so imports resolve the same way in both tools. `web/vite.config.ts:9-13` `web/tsconfig.json:28-33`

A production build empties and rewrites `src/ai_usage_cost/web/dist`. `web/vite.config.ts:14-17` The README says the built bundle is committed, which is why the serve command works for people who never install Node.js. `README.md:653-658`

In development the Vite server listens on port 5173 and forwards every API request to the Python server at the local address on port 8420. `web/vite.config.ts:18-26` This lets the dashboard be edited with hot reload against live data. The README names the same address as the dashboard URL of the serve command. `README.md:150`

The same file configures the test runner: tests run in jsdom, and a setup file is loaded first. `web/vite.config.ts:27-30` That setup file unmounts rendered components after each test. `web/src/test-setup.ts:6-8`

## Scripts and quality gates

The web scripts are `dev`, `build`, `preview`, `typecheck`, `lint` and `test`. The build runs the type checker before Vite, so a type error stops the bundle. `web/package.json:6-13` The type checker runs in strict mode and flags unused locals and parameters. `web/tsconfig.json:19-22` Dependency versions in web/package.json are exact, with no ranges. `web/package.json:14-45`

ESLint uses the recommended JavaScript and TypeScript rules for TypeScript files, adds the React hooks rules, and warns when a component file exports something that is not a component. `web/eslint.config.js:9-23` It ignores both the local dist folder and the committed bundle. `web/eslint.config.js:8`

Python quality is set in `pyproject.toml`. Ruff checks the rule families E, F, I, UP and B with a line length of 100. `pyproject.toml:39-44` Mypy runs with the pydantic plugin. `pyproject.toml:46-49` Pylint must score at least 9.0. `pyproject.toml:112-113` Bandit skips the tests and the web folder. `pyproject.toml:119-120`

The pre-commit file runs ruff and ruff format on every commit, pylint on Python files, and ESLint when a web TypeScript file changes. Mypy is a manual stage only. `.pre-commit-config.yaml:1-33`

## What a reader must know

The chunk name says the root has few files, but the generated file table below lists every file under the web folder, because the chunk owns the glob web/*. Those files belong to later chunks in the plan; this note explains only the root files named above.

The dashboard bundle under `src/ai_usage_cost/web/dist` is build output. Edit the dashboard source and rebuild; the config rewrites that folder on each build. `web/vite.config.ts:14-17`

## Reference

%% generated:chunk-files start (do not edit; run brain docs generate) %%
### Files

| File | Purpose | Lines | Imports | Imported by | Code |
|---|---|---|---|---|---|
| `web/eslint.config.js` | - | 25 | 0 | 0 | [[web/eslint.config.js]] `web/eslint.config.js:1-25` |
| `web/src/App.tsx` | - | 357 | 15 | 1 | [[web/src/App.tsx]] `web/src/App.tsx:1-357` |
| `web/src/ContextTab.tsx` | - | 227 | 9 | 1 | [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:1-227` |
| `web/src/EconomicsTab.tsx` | - | 770 | 15 | 2 | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:1-770` |
| `web/src/FilterRail.tsx` | - | 506 | 13 | 1 | [[web/src/FilterRail.tsx]] `web/src/FilterRail.tsx:1-506` |
| `web/src/Header.tsx` | - | 137 | 6 | 1 | [[web/src/Header.tsx]] `web/src/Header.tsx:1-137` |
| `web/src/Overview.tsx` | - | 917 | 13 | 1 | [[web/src/Overview.tsx]] `web/src/Overview.tsx:1-917` |
| `web/src/Pricing.tsx` | - | 632 | 13 | 2 | [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:1-632` |
| `web/src/SessionWorkspace.tsx` | - | 626 | 20 | 4 | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:1-626` |
| `web/src/Sessions.tsx` | - | 382 | 14 | 1 | [[web/src/Sessions.tsx]] `web/src/Sessions.tsx:1-382` |
| `web/src/Sources.tsx` | - | 249 | 10 | 1 | [[web/src/Sources.tsx]] `web/src/Sources.tsx:1-249` |
| `web/src/TraceTab.tsx` | - | 1025 | 16 | 2 | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:1-1025` |
| `web/src/api.ts` | - | 595 | 0 | 27 | [[web/src/api.ts]] `web/src/api.ts:1-595` |
| `web/src/components/chart-hover.tsx` | - | 121 | 1 | 2 | [[web/src/components/chart-hover.tsx]] `web/src/components/chart-hover.tsx:1-121` |
| `web/src/components/chart-time.tsx` | - | 184 | 3 | 2 | [[web/src/components/chart-time.tsx]] `web/src/components/chart-time.tsx:1-184` |
| `web/src/components/columns.tsx` | - | 95 | 2 | 2 | [[web/src/components/columns.tsx]] `web/src/components/columns.tsx:1-95` |
| `web/src/components/detail.tsx` | - | 80 | 2 | 7 | [[web/src/components/detail.tsx]] `web/src/components/detail.tsx:1-80` |
| `web/src/components/filters.tsx` | - | 269 | 7 | 9 | [[web/src/components/filters.tsx]] `web/src/components/filters.tsx:1-269` |
| `web/src/components/metric-info.tsx` | - | 205 | 2 | 7 | [[web/src/components/metric-info.tsx]] `web/src/components/metric-info.tsx:1-205` |
| `web/src/components/panel.tsx` | - | 69 | 1 | 13 | [[web/src/components/panel.tsx]] `web/src/components/panel.tsx:1-69` |
| `web/src/components/rank.ts` | - | 19 | 1 | 3 | [[web/src/components/rank.ts]] `web/src/components/rank.ts:1-19` |
| `web/src/components/series.ts` | - | 29 | 0 | 10 | [[web/src/components/series.ts]] `web/src/components/series.ts:1-29` |
| `web/src/components/session.tsx` | - | 205 | 5 | 3 | [[web/src/components/session.tsx]] `web/src/components/session.tsx:1-205` |
| `web/src/components/source-card.tsx` | - | 121 | 5 | 5 | [[web/src/components/source-card.tsx]] `web/src/components/source-card.tsx:1-121` |
| `web/src/components/sparkline.tsx` | - | 145 | 2 | 5 | [[web/src/components/sparkline.tsx]] `web/src/components/sparkline.tsx:1-145` |
| `web/src/components/stat.tsx` | - | 164 | 2 | 15 | [[web/src/components/stat.tsx]] `web/src/components/stat.tsx:1-164` |
| `web/src/components/states.tsx` | - | 338 | 10 | 15 | [[web/src/components/states.tsx]] `web/src/components/states.tsx:1-338` |
| `web/src/components/status.tsx` | - | 454 | 4 | 19 | [[web/src/components/status.tsx]] `web/src/components/status.tsx:1-454` |
| `web/src/components/trace.tsx` | - | 435 | 6 | 4 | [[web/src/components/trace.tsx]] `web/src/components/trace.tsx:1-435` |
| `web/src/components/ui/accordion.tsx` | - | 65 | 1 | 1 | [[web/src/components/ui/accordion.tsx]] `web/src/components/ui/accordion.tsx:1-65` |
| `web/src/components/ui/alert.tsx` | - | 65 | 1 | 1 | [[web/src/components/ui/alert.tsx]] `web/src/components/ui/alert.tsx:1-65` |
| `web/src/components/ui/badge.tsx` | - | 47 | 1 | 6 | [[web/src/components/ui/badge.tsx]] `web/src/components/ui/badge.tsx:1-47` |
| `web/src/components/ui/button.tsx` | - | 63 | 1 | 14 | [[web/src/components/ui/button.tsx]] `web/src/components/ui/button.tsx:1-63` |
| `web/src/components/ui/chart.tsx` | - | 371 | 1 | 1 | [[web/src/components/ui/chart.tsx]] `web/src/components/ui/chart.tsx:1-371` |
| `web/src/components/ui/checkbox.tsx` | - | 31 | 1 | 2 | [[web/src/components/ui/checkbox.tsx]] `web/src/components/ui/checkbox.tsx:1-31` |
| `web/src/components/ui/collapsible.tsx` | - | 31 | 0 | 1 | [[web/src/components/ui/collapsible.tsx]] `web/src/components/ui/collapsible.tsx:1-31` |
| `web/src/components/ui/dialog.tsx` | - | 158 | 2 | 1 | [[web/src/components/ui/dialog.tsx]] `web/src/components/ui/dialog.tsx:1-158` |
| `web/src/components/ui/dropdown-menu.tsx` | - | 254 | 1 | 2 | [[web/src/components/ui/dropdown-menu.tsx]] `web/src/components/ui/dropdown-menu.tsx:1-254` |
| `web/src/components/ui/input.tsx` | - | 20 | 1 | 3 | [[web/src/components/ui/input.tsx]] `web/src/components/ui/input.tsx:1-20` |
| `web/src/components/ui/label.tsx` | - | 21 | 1 | 5 | [[web/src/components/ui/label.tsx]] `web/src/components/ui/label.tsx:1-21` |
| `web/src/components/ui/popover.tsx` | - | 86 | 1 | 2 | [[web/src/components/ui/popover.tsx]] `web/src/components/ui/popover.tsx:1-86` |
| `web/src/components/ui/progress.tsx` | - | 28 | 1 | 1 | [[web/src/components/ui/progress.tsx]] `web/src/components/ui/progress.tsx:1-28` |
| `web/src/components/ui/select.tsx` | - | 187 | 1 | 2 | [[web/src/components/ui/select.tsx]] `web/src/components/ui/select.tsx:1-187` |
| `web/src/components/ui/separator.tsx` | - | 25 | 1 | 5 | [[web/src/components/ui/separator.tsx]] `web/src/components/ui/separator.tsx:1-25` |
| `web/src/components/ui/sheet.tsx` | - | 140 | 1 | 4 | [[web/src/components/ui/sheet.tsx]] `web/src/components/ui/sheet.tsx:1-140` |
| `web/src/components/ui/skeleton.tsx` | - | 13 | 1 | 2 | [[web/src/components/ui/skeleton.tsx]] `web/src/components/ui/skeleton.tsx:1-13` |
| `web/src/components/ui/sonner.tsx` | - | 39 | 1 | 1 | [[web/src/components/ui/sonner.tsx]] `web/src/components/ui/sonner.tsx:1-39` |
| `web/src/components/ui/switch.tsx` | - | 34 | 1 | 3 | [[web/src/components/ui/switch.tsx]] `web/src/components/ui/switch.tsx:1-34` |
| `web/src/components/ui/table.tsx` | - | 113 | 1 | 7 | [[web/src/components/ui/table.tsx]] `web/src/components/ui/table.tsx:1-113` |
| `web/src/components/ui/tabs.tsx` | - | 90 | 1 | 2 | [[web/src/components/ui/tabs.tsx]] `web/src/components/ui/tabs.tsx:1-90` |
| `web/src/components/ui/textarea.tsx` | - | 19 | 1 | 1 | [[web/src/components/ui/textarea.tsx]] `web/src/components/ui/textarea.tsx:1-19` |
| `web/src/components/ui/toggle-group.tsx` | - | 81 | 2 | 6 | [[web/src/components/ui/toggle-group.tsx]] `web/src/components/ui/toggle-group.tsx:1-81` |
| `web/src/components/ui/toggle.tsx` | - | 46 | 1 | 2 | [[web/src/components/ui/toggle.tsx]] `web/src/components/ui/toggle.tsx:1-46` |
| `web/src/components/ui/tooltip.tsx` | - | 56 | 1 | 10 | [[web/src/components/ui/tooltip.tsx]] `web/src/components/ui/tooltip.tsx:1-56` |
| `web/src/components/use-media-query.ts` | - | 18 | 0 | 4 | [[web/src/components/use-media-query.ts]] `web/src/components/use-media-query.ts:1-18` |
| `web/src/components/workspace-panel.ts` | - | 73 | 0 | 1 | [[web/src/components/workspace-panel.ts]] `web/src/components/workspace-panel.ts:1-73` |
| `web/src/design-system/cn.ts` | - | 6 | 0 | 45 | [[web/src/design-system/cn.ts]] `web/src/design-system/cn.ts:1-6` |
| `web/src/format.ts` | - | 197 | 1 | 21 | [[web/src/format.ts]] `web/src/format.ts:1-197` |
| `web/src/main.tsx` | - | 13 | 2 | 0 | [[web/src/main.tsx]] `web/src/main.tsx:1-13` |
| `web/src/pricing-format.ts` | - | 181 | 2 | 2 | [[web/src/pricing-format.ts]] `web/src/pricing-format.ts:1-181` |
| `web/src/pricing-notes.ts` | - | 68 | 2 | 5 | [[web/src/pricing-notes.ts]] `web/src/pricing-notes.ts:1-68` |
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
| `web/src/test-setup.ts` | - | 8 | 0 | 0 | [[web/src/test-setup.ts]] `web/src/test-setup.ts:1-8` |
| `web/src/theme.ts` | - | 69 | 0 | 4 | [[web/src/theme.ts]] `web/src/theme.ts:1-69` |
| `web/src/turn-insights.ts` | - | 162 | 1 | 2 | [[web/src/turn-insights.ts]] `web/src/turn-insights.ts:1-162` |
| `web/vite.config.ts` | - | 31 | 0 | 0 | [[web/vite.config.ts]] `web/vite.config.ts:1-31` |
%% generated:chunk-files end %%

%% generated:chunk-interface start (do not edit; run brain docs generate) %%
### Public interface

| Name | Kind | File | Code |
|---|---|---|---|
| `cn` | function | `web/src/design-system/cn.ts` | [[web/src/design-system/cn.ts]] `web/src/design-system/cn.ts:4` |
| `TokenUsage` | interface | `web/src/api.ts` | [[web/src/api.ts]] `web/src/api.ts:1` |
| `CostBreakdown` | interface | `web/src/api.ts` | [[web/src/api.ts]] `web/src/api.ts:13` |
| `Bucket` | interface | `web/src/api.ts` | [[web/src/api.ts]] `web/src/api.ts:27` |
| `Totals` | interface | `web/src/api.ts` | [[web/src/api.ts]] `web/src/api.ts:39` |
| `SeriesPoint` | interface | `web/src/api.ts` | [[web/src/api.ts]] `web/src/api.ts:50` |
| `CostState` | type | `web/src/api.ts` | [[web/src/api.ts]] `web/src/api.ts:61` |
| `Provenance` | type | `web/src/api.ts` | [[web/src/api.ts]] `web/src/api.ts:63` |
| `RawScalar` | type | `web/src/api.ts` | [[web/src/api.ts]] `web/src/api.ts:65` |
| `SpanKind` | type | `web/src/api.ts` | [[web/src/api.ts]] `web/src/api.ts:67` |
| `SpanStatus` | type | `web/src/api.ts` | [[web/src/api.ts]] `web/src/api.ts:80` |
| `OutcomeLabel` | type | `web/src/api.ts` | [[web/src/api.ts]] `web/src/api.ts:82` |
| `Span` | interface | `web/src/api.ts` | [[web/src/api.ts]] `web/src/api.ts:84` |
| `formatMoney` | function | `web/src/format.ts` | [[web/src/format.ts]] `web/src/format.ts:20` |
| `formatMoneyExact` | function | `web/src/format.ts` | [[web/src/format.ts]] `web/src/format.ts:25` |
| `formatMoneyShort` | function | `web/src/format.ts` | [[web/src/format.ts]] `web/src/format.ts:37` |
| `formatTokens` | function | `web/src/format.ts` | [[web/src/format.ts]] `web/src/format.ts:56` |
| `plural` | function | `web/src/format.ts` | [[web/src/format.ts]] `web/src/format.ts:71` |
| `formatCount` | function | `web/src/format.ts` | [[web/src/format.ts]] `web/src/format.ts:75` |
| `sessionDisplayName` | function | `web/src/format.ts` | [[web/src/format.ts]] `web/src/format.ts:80` |
| `formatExact` | function | `web/src/format.ts` | [[web/src/format.ts]] `web/src/format.ts:85` |
| `formatDuration` | function | `web/src/format.ts` | [[web/src/format.ts]] `web/src/format.ts:89` |
| `formatPercent` | function | `web/src/format.ts` | [[web/src/format.ts]] `web/src/format.ts:101` |
| `formatDay` | function | `web/src/format.ts` | [[web/src/format.ts]] `web/src/format.ts:106` |
| `formatDayShort` | function | `web/src/format.ts` | [[web/src/format.ts]] `web/src/format.ts:119` |
| `Unavailable` | function | `web/src/components/status.tsx` | [[web/src/components/status.tsx]] `web/src/components/status.tsx:77` |
| `PartialMarker` | function | `web/src/components/status.tsx` | [[web/src/components/status.tsx]] `web/src/components/status.tsx:96` |
| `CostStateBadge` | function | `web/src/components/status.tsx` | [[web/src/components/status.tsx]] `web/src/components/status.tsx:149` |
| `EstimatedBadge` | function | `web/src/components/status.tsx` | [[web/src/components/status.tsx]] `web/src/components/status.tsx:171` |
| `ExperimentalBadge` | function | `web/src/components/status.tsx` | [[web/src/components/status.tsx]] `web/src/components/status.tsx:175` |
| `CostBadges` | function | `web/src/components/status.tsx` | [[web/src/components/status.tsx]] `web/src/components/status.tsx:180` |
| `ProvenanceBadge` | function | `web/src/components/status.tsx` | [[web/src/components/status.tsx]] `web/src/components/status.tsx:197` |
| `OutcomeBadge` | function | `web/src/components/status.tsx` | [[web/src/components/status.tsx]] `web/src/components/status.tsx:220` |
| `Meter` | function | `web/src/components/status.tsx` | [[web/src/components/status.tsx]] `web/src/components/status.tsx:238` |
| `BucketSegment` | interface | `web/src/components/status.tsx` | [[web/src/components/status.tsx]] `web/src/components/status.tsx:279` |
| `BucketBar` | function | `web/src/components/status.tsx` | [[web/src/components/status.tsx]] `web/src/components/status.tsx:286` |
| `Legend` | function | `web/src/components/status.tsx` | [[web/src/components/status.tsx]] `web/src/components/status.tsx:324` |
| `NumberTicker` | function | `web/src/components/stat.tsx` | [[web/src/components/stat.tsx]] `web/src/components/stat.tsx:14` |
| `StatLabel` | function | `web/src/components/stat.tsx` | [[web/src/components/stat.tsx]] `web/src/components/stat.tsx:49` |
| `Stat` | function | `web/src/components/stat.tsx` | [[web/src/components/stat.tsx]] `web/src/components/stat.tsx:61` |
| `StatGrid` | function | `web/src/components/stat.tsx` | [[web/src/components/stat.tsx]] `web/src/components/stat.tsx:157` |
| `SortDirection` | type | `web/src/components/states.tsx` | [[web/src/components/states.tsx]] `web/src/components/states.tsx:19` |
| `ariaSort` | function | `web/src/components/states.tsx` | [[web/src/components/states.tsx]] `web/src/components/states.tsx:21` |
| `SortButton` | function | `web/src/components/states.tsx` | [[web/src/components/states.tsx]] `web/src/components/states.tsx:29` |
| `EmptyState` | function | `web/src/components/states.tsx` | [[web/src/components/states.tsx]] `web/src/components/states.tsx:68` |
| `ErrorState` | function | `web/src/components/states.tsx` | [[web/src/components/states.tsx]] `web/src/components/states.tsx:98` |
| `PanelSkeleton` | function | `web/src/components/states.tsx` | [[web/src/components/states.tsx]] `web/src/components/states.tsx:123` |
| `DisclosurePanel` | function | `web/src/components/states.tsx` | [[web/src/components/states.tsx]] `web/src/components/states.tsx:136` |
| `WarningsList` | function | `web/src/components/states.tsx` | [[web/src/components/states.tsx]] `web/src/components/states.tsx:247` |
| `OfflineCard` | function | `web/src/components/states.tsx` | [[web/src/components/states.tsx]] `web/src/components/states.tsx:280` |
| `StatSkeleton` | function | `web/src/components/states.tsx` | [[web/src/components/states.tsx]] `web/src/components/states.tsx:330` |
| `Panel` | function | `web/src/components/panel.tsx` | [[web/src/components/panel.tsx]] `web/src/components/panel.tsx:5` |
| `PanelHeader` | function | `web/src/components/panel.tsx` | [[web/src/components/panel.tsx]] `web/src/components/panel.tsx:15` |
| `PanelBody` | function | `web/src/components/panel.tsx` | [[web/src/components/panel.tsx]] `web/src/components/panel.tsx:55` |
| `PanelNote` | function | `web/src/components/panel.tsx` | [[web/src/components/panel.tsx]] `web/src/components/panel.tsx:59` |
| `SERIES_SLOTS` | const | `web/src/components/series.ts` | [[web/src/components/series.ts]] `web/src/components/series.ts:1` |
| `seriesColor` | function | `web/src/components/series.ts` | [[web/src/components/series.ts]] `web/src/components/series.ts:3` |
| `TokenBucket` | interface | `web/src/components/series.ts` | [[web/src/components/series.ts]] `web/src/components/series.ts:7` |
| `TOKEN_BUCKETS` | const | `web/src/components/series.ts` | [[web/src/components/series.ts]] `web/src/components/series.ts:14` |
| `SearchField` | function | `web/src/components/filters.tsx` | [[web/src/components/filters.tsx]] `web/src/components/filters.tsx:18` |
| `FacetOption` | interface | `web/src/components/filters.tsx` | [[web/src/components/filters.tsx]] `web/src/components/filters.tsx:56` |
| `FacetGroup` | function | `web/src/components/filters.tsx` | [[web/src/components/filters.tsx]] `web/src/components/filters.tsx:63` |
| `ChipRow` | function | `web/src/components/filters.tsx` | [[web/src/components/filters.tsx]] `web/src/components/filters.tsx:120` |
| `DateRange` | function | `web/src/components/filters.tsx` | [[web/src/components/filters.tsx]] `web/src/components/filters.tsx:156` |
| `SortSelect` | function | `web/src/components/filters.tsx` | [[web/src/components/filters.tsx]] `web/src/components/filters.tsx:195` |
| `ActiveFilter` | interface | `web/src/components/filters.tsx` | [[web/src/components/filters.tsx]] `web/src/components/filters.tsx:224` |
| `FilterChips` | function | `web/src/components/filters.tsx` | [[web/src/components/filters.tsx]] `web/src/components/filters.tsx:231` |
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
| `Section` | function | `web/src/components/detail.tsx` | [[web/src/components/detail.tsx]] `web/src/components/detail.tsx:6` |

124 more public names are omitted; see the cited files.
%% generated:chunk-interface end %%
