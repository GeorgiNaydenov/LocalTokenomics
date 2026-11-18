---
title: Web Overview
aliases: []
tags: [module, overview]
area: application
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: e5313fbd7062
chunk: ch-localtokenomics-web-src
---

# Web Overview

What Web is made of and how it connects to the rest of the code.

## How it works

Web holds 73 source files and 15449 lines, with 188 tests that live in it or import its files. The most depended-on files are `web/src/design-system/cn.ts`, `web/src/api.ts`, `web/src/format.ts`. It uses Web UI components Overview, Web ui UI components Overview. It is used by Web UI components Overview, Web ui UI components Overview, Web prototype Overview.

The purpose column quotes each file's own header comment where it has one. Every file is cited by its full line range, and every public name by the line that declares it.

## Reference

%% generated:chunk-files start (do not edit; run brain docs generate) %%
### Files

| File | Purpose | Lines | Imports | Imported by | Code |
|---|---|---|---|---|---|
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

## Explanation

### What the dashboard is

The dashboard code is a single page React application that shows token usage and its list price cost for the AI coding tools found on this machine. It mounts one top level component inside a tooltip provider and loads the shared theme stylesheet `web/src/main.tsx:7-13`. The page never reads logs itself. Every figure comes from JSON that the local `ai-usage-cost` server returns `web/src/api.ts:489-500`.

### How data is loaded

All network access goes through one helper, `getJson`. A failed `fetch` becomes an `ApiError` that says the server could not be reached, and a non success status becomes an `ApiError` naming the path and the status `web/src/api.ts:489-500`. Endpoints are relative paths such as `api/meta`, `api/rates` and `api/report`, so the page works under whatever host and port serves it `web/src/api.ts:502-512` `web/src/api.ts:532`.

The report request carries the whole filter state as a query string. Dates, search text, cost states, clients, models, projects and outcomes are added only when set, and the sidechain, traced and error flags are added only when they differ from their default `web/src/api.ts:514-533`. Per session detail has its own paths: trace, economics, context, outcome and span content are read with GET, the outcome is saved with PUT, and a session is removed with DELETE `web/src/api.ts:539-595`.

### State held by the page

The top level component owns the whole page state: the metadata, the rate table, the report, the current query, the selected view, the open session workspace and the loading and error flags `web/src/App.tsx:132-145`. A blank query has no dates, no facets, sidechains included and no outcome, traced or error filter `web/src/App.tsx:23-35`. The four views are overview, sessions, sources and pricing `web/src/api.ts:361`.

On first load the metadata and the rate table are fetched together. When the query has no dates yet, the range is set from the first day in the data up to today `web/src/App.tsx:166-181`. A second effect fetches the report whenever the metadata or the query changes, and cancels the previous request through an abort controller so a slow answer cannot overwrite a newer one `web/src/App.tsx:183-201`. While a new query is in flight the page keeps the old report and dims the counter, because `refetching` is true until the settled query equals the current one `web/src/App.tsx:203` `web/src/App.tsx:322-326`.

Active filters are shown as removable chips built from the query, with client and model ids replaced by their labels where known `web/src/App.tsx:54-127`. Facet toggling adds a value to a list or removes it if present `web/src/App.tsx:43-45` `web/src/App.tsx:151-164`.

### Rescan and automatic refresh

The Rescan button posts to the server, then bumps a reload counter that makes the metadata, rates and report load again `web/src/App.tsx:211-222`. A timer repeats this every five minutes while the tab is visible `web/src/App.tsx:21` `web/src/App.tsx:224-249`. The timer stops when the tab is hidden, and on becoming visible again a rescan runs at once if the last scan is older than five minutes `web/src/App.tsx:235-243`.

### Failure and loading screens

If the error text says the server could not be reached, the page shows an offline card with the command `ai-usage-cost serve` and a retry button `web/src/App.tsx:251-261`. Any other error shows an error state `web/src/App.tsx:271-277`, and the first load shows a loading label `web/src/App.tsx:263-269`. This split keeps a stopped server visibly different from a server that answered with an error.

### The four views and the session workspace

Each view renders only when its data has arrived: overview and sources need the report and the metadata, sessions needs the report, pricing needs the report and the rate table `web/src/App.tsx:330-339`. Choosing a session opens a workspace panel for the row with the matching session id and source `web/src/App.tsx:284-288` `web/src/App.tsx:342-353`.

The workspace has four tabs, Summary, Trace, Economics and Context `web/src/SessionWorkspace.tsx:49` `web/src/SessionWorkspace.tsx:72-77`. The outcome is fetched when the workspace opens, while the other three resources are fetched only after their tab has been requested once `web/src/SessionWorkspace.tsx:447-474`. Each lazy resource moves through idle, loading, ready or error and ignores answers from an aborted request `web/src/SessionWorkspace.tsx:81-111`. On a wide screen the workspace is a docked side panel that can be resized and closed with Escape, and on a narrow screen it becomes a sheet `web/src/SessionWorkspace.tsx:486-493` `web/src/SessionWorkspace.tsx:600-625`.

### Reading the cost correctly

The cost state of a session is one of priced, free, unpriced or unavailable `web/src/api.ts:61`. The summary tab explains each state in words: priced requests use list prices, free means a local runtime counted at zero, unpriced means no rate entry matches so the cost stays out of totals, and unavailable means the client logs no token counts so cost is left blank `web/src/SessionWorkspace.tsx:113-130`. Missing values are shown as unavailable, never as zero, which is also what the capability table says about provenance `web/src/Sources.tsx:28-34`.

When a tool wrote its own cost, the page shows it as a second line, and flags a divergence if the two figures differ by more than five percent or one cent `web/src/pricing-notes.ts:36-39` `web/src/pricing-notes.ts:47-56`. A row priced from a sibling model's rate is marked as estimated `web/src/pricing-notes.ts:65-68`. A notice appears when the rate table is 30 days old and turns to caution at 90 days `web/src/pricing-notes.ts:16-34`.

### Recording an outcome

A person can rate a session as successful, partial, failed, abandoned or unrated, and add notes and tags `web/src/SessionWorkspace.tsx:262-289`. Each change is sent with PUT, tags are split on commas and trimmed `web/src/SessionWorkspace.tsx:255-260`, and notes or tags are saved only when the field loses focus and the text actually changed `web/src/SessionWorkspace.tsx:291-294`. The status line shows saving, the error text, the save time or "not rated yet" `web/src/SessionWorkspace.tsx:296-302`. This is the one place where the dashboard writes data back to the server.

### Sessions, sources and pricing

The sessions table sorts by start time, newest first, and shows at most 120 rows `web/src/Sessions.tsx:48` `web/src/Sessions.tsx:240-253`. Clicking the active column header flips the direction and a new column starts descending `web/src/Sessions.tsx:259-264`. Sessions without a cost sort as minus one, so they fall below priced rows when sorted by cost or tokens `web/src/Sessions.tsx:91-94`.

The sources view lists readers with verified ones first and experimental ones after, and it says when a reader was not detected on this machine `web/src/Sources.tsx:36-39` `web/src/Sources.tsx:41-46`.

The pricing view builds one row per rate. A rate row is free when its merged provider rules say so, priced when buckets matched to it carry spend, and unused otherwise `web/src/Pricing.tsx:119-128`. Spend is joined by model key and only exact or suffix matches count, so an estimated bucket is credited to its parent separately `web/src/Pricing.tsx:90-117`. Cache prices use the published figure when present, otherwise input price times the provider ratio, otherwise nothing `web/src/pricing-format.ts:47-72`. Rows get Preview, Retired or Unverified tags `web/src/pricing-format.ts:149-161`.

### Per turn insights

`turn-insights.ts` computes the facts shown above the economics table. The unattributed row, the spend outside any turn, is kept out of every ranking `web/src/turn-insights.ts:4-8` `web/src/turn-insights.ts:15-17` `web/src/turn-insights.ts:52-61`. Cost concentration is the top three turns as a share of turn cost, and is empty when no turn is priced `web/src/turn-insights.ts:70-82`. The half trend splits turns by order into two halves and compares their cost `web/src/turn-insights.ts:121-140`.

### Formatting and theme

Money is shown in US dollars with two decimals, with four decimals for values under one cent so a tooltip never shows $0.00 for a real cost `web/src/format.ts:19-27`. Token counts are abbreviated with K, M and B, rolled up so 999,999 does not read as 1000K `web/src/format.ts:53-64`. Dates are parsed as plain days so the viewer's time zone never shifts them `web/src/format.ts:105-116`.

The theme is light or dark. It uses the stored choice when present and the system preference otherwise, and a blocked local storage falls back without an error `web/src/theme.ts:5-33`. Changing the theme sets it on the document and notifies subscribers `web/src/theme.ts:42-47` `web/src/theme.ts:56-69`.
