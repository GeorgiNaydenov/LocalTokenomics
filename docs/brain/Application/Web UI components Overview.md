---
title: Web UI components Overview
aliases: []
tags: [module, overview]
area: application
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/components/*]
verified-against: 4a002de17be5
chunk: ch-localtokenomics-web-src-components
approved-by: human
approved-at: '2026-11-18T19:03:01+00:00'
---

# Web UI components Overview

What Web UI components is made of and how it connects to the rest of the code.

## How it works

Web UI components holds 43 source files and 5107 lines, with 18 tests that live in it or import its files. The most depended-on files are `web/src/components/status.tsx`, `web/src/components/stat.tsx`, `web/src/components/states.tsx`. It uses [[Web Overview]], [[Web ui UI components Overview]]. It is used by [[Web Overview]], [[Web prototype Overview]].

The purpose column quotes each file's own header comment where it has one. Every file is cited by its full line range, and every public name by the line that declares it.

## What this chunk is

This chunk is the set of shared, presentation-only building blocks of the dashboard: stat cards, badges, meters, a stacked daily chart, sparklines, filter controls, a column chooser, session and source cards and a span timeline. The files in the `ui/` subfolder are the lower-level primitives and belong to a separate chunk for the ui folder, which this chunk imports, for example the button and dropdown menu in `web/src/components/columns.tsx:4-12`.

The components do not fetch or price anything. They receive already computed values, labels and colours as props. A session row, for instance, arrives as a summary with model, client, project, started time, request count and pre-formatted token and cost text `web/src/components/session.tsx:101-115`. The rest of the web app, such as `web/src/App.tsx:15-17`, imports these components and decides what data goes in.

## Honest display of missing data

The most repeated rule in the chunk is that a missing number is shown as the word "unavailable" and is never replaced by a zero or a guess.

- A cost state is one of priced, free, unpriced or unavailable. Unpriced rows are described as left out of cost totals, and unavailable rows as having no token counts, so cost is never invented `web/src/components/status.tsx:8-29`.
- `Unavailable` renders the word in the unavailable colour and, when given a hint, makes it an explanation trigger `web/src/components/status.tsx:77-94`.
- The meter, the bucket bar, the meter row and the comparison meter each switch to the unavailable marker when the value is null or the total is not positive, so no empty bar is drawn `web/src/components/status.tsx:253-259` `web/src/components/status.tsx:296-302` `web/src/components/status.tsx:383-387` `web/src/components/status.tsx:422-431`.
- The token cell and the session card do the same for token and cost text that is null `web/src/components/session.tsx:63-69` `web/src/components/session.tsx:192-201`.
- The context occupancy chart draws a call with unknown occupancy as a hatched full-height bar and says in a note that it is unknown, not zero `web/src/components/trace.tsx:136-147` `web/src/components/trace.tsx:203-209`.

## Badges and ranking

`SignalBadge` is the one shape behind the cost state, provenance, outcome, estimated and experimental badges: a coloured dot, a label and an optional explanation popover when a title is given `web/src/components/status.tsx:104-147`. Provenance has five values (measured, derived, estimated, inferred, unavailable) and outcome has five (successful, partial, failed, abandoned, unrated) `web/src/components/status.tsx:31-65`.

`CostBadges` adds an Estimated badge next to the state badge when a priced row used another model's rate. The estimated colour is the inferred purple on purpose, so it is not confused with the amber of an unpriced row `web/src/components/status.tsx:167-195`.

When several rows are rolled up into one, `worstState` and `worstProvenance` pick the least trustworthy value by rank, and an empty list gives unavailable `web/src/components/rank.ts:3-19`.

## Stat cards

`Stat` shows a label, a value, an optional unit and hint, and an optional info popover. When an exact unrounded value is passed, it is appended to the popover so an abbreviated headline never hides the true count `web/src/components/stat.tsx:90-95`. A numeric value with a formatter animates through `NumberTicker`, which uses a cubic ease and skips the animation when the reader prefers reduced motion `web/src/components/stat.tsx:7-47` `web/src/components/stat.tsx:113-117`.

A clickable stat card is a `div` with `role="button"` rather than a native button, because the info trigger inside it is itself interactive and a button cannot contain another one `web/src/components/stat.tsx:132-152`.

## Explanation popovers

`MetricInfo` is the popover that explains a number. Its content is either one plain sentence or a structured block with meaning, formula, computed value, provenance and caveats `web/src/components/metric-info.tsx:15-24` `web/src/components/metric-info.tsx:165-187`.

It opens after the pointer rests on the trigger for 400 ms, closes 250 ms after the pointer leaves both trigger and popover, and checks this every 100 ms from one shared pointer position `web/src/components/metric-info.tsx:11-13` `web/src/components/metric-info.tsx:35-44` `web/src/components/metric-info.tsx:78-111`. Focus opens it too, and a click toggles it `web/src/components/metric-info.tsx:134-144`.

Focus is deliberately not returned to the trigger on close. Otherwise the trigger's focus handler would reopen the popover and it would flicker forever. A regression test covers exactly this `web/src/components/metric-info.tsx:156-162` `web/src/components/metric-info.test.tsx:17-41`.

## Charts

The stacked time chart draws one stacked bar per calendar day. Series are ordered by their total, the first twelve get their own colour and legend entry, and the rest are grouped as "Other (n)" `web/src/components/chart-time.tsx:40-93` `web/src/components/series.ts:1-5`. A dashed line marks the mean per calendar day and a vertical line marks the peak day `web/src/components/chart-time.tsx:147-171`. With no series it renders nothing `web/src/components/chart-time.tsx:95`.

The sparkline draws a small line over a baseline that always includes zero, falls back to a flat line when all values are equal, and clamps every point inside the box `web/src/components/sparkline.tsx:4-21`. It only gets hover details when both labels and a formatter are supplied `web/src/components/sparkline.tsx:129-143`.

The shared hover frame gives charts one shared hover and keyboard behaviour: pointer position picks the nearest point, arrow keys, Home and End step through points, Escape clears, and a polite live region reads the selected point aloud `web/src/components/chart-hover.tsx:37-66` `web/src/components/chart-hover.tsx:114-118`.

The context occupancy chart draws one bar per model call showing how full the context window was, in the warning colour at 85 percent or more, with mean and peak lines and a mark where the context was compacted `web/src/components/trace.tsx:34` `web/src/components/trace.tsx:149-163` `web/src/components/trace.tsx:166-190`.

## Tables, filters and controls

`useHiddenColumns` keeps the hidden column keys in `localStorage` under a key chosen by the caller, and ignores storage errors. `visibleColumns` returns all columns if the reader hid every one `web/src/components/columns.tsx:22-60`. The column chooser menu stays open while ticking items `web/src/components/columns.tsx:83-90`.

The filters file holds the filter controls: a search box with a clear button, checkbox facets with counts, single-choice chips, a from and to date pair that bounds each side by the other, a sort select, and removable chips for the active filters with a "Clear all" link `web/src/components/filters.tsx:18-54` `web/src/components/filters.tsx:63-118` `web/src/components/filters.tsx:156-193` `web/src/components/filters.tsx:231-269`.

`SortButton` shows the sort direction icon and `ariaSort` maps it to the ARIA value for table headers `web/src/components/states.tsx:21-66`.

## Panels, states and layout helpers

`Panel`, `PanelHeader`, `PanelBody` and `PanelNote` are the card frame used by most views `web/src/components/panel.tsx:5-69`. `EmptyState`, `ErrorState`, `PanelSkeleton`, `StatSkeleton` and `DisclosurePanel` cover empty, failed, loading and collapsed content `web/src/components/states.tsx:68-172` `web/src/components/states.tsx:330-338`.

`OfflineCard` is the full-page message shown when the local reader is not running. It tells the reader nothing was uploaded, shows the start command and offers retry and copy buttons `web/src/components/states.tsx:280-328`.

`WarningsList` groups scan warnings by kind, lets the reader filter by kind and explains each group's severity and estimated impact `web/src/components/states.tsx:174-278`.

The detail file offers small layout pieces for side panels: `Section`, `MetaGrid`, `CodeBlock` and `PathList` `web/src/components/detail.tsx:6-80`. `useWorkspacePanel` stores the side panel width, clamped between 360 and 900 pixels and at most 90 percent of the window, and the fullscreen flag in `localStorage` `web/src/components/workspace-panel.ts:3-47` `web/src/components/workspace-panel.ts:49-73`. `useMediaQuery` subscribes to a CSS media query `web/src/components/use-media-query.ts:3-18`.

## Session and source cards

`SessionCard` shows state, outcome, error count, model (plus a count of extra models), client, project, start time, requests, tokens and cost. A full-card button opens the session `web/src/components/session.tsx:117-205`. `TracedDot`, `ErrorCount` and `TokenCell` are the compact table cell versions, and `TokenCell` bars are scaled to the largest row shown `web/src/components/session.tsx:7-99`.

`SourceCard` and `SourceDetail` summarise one log source: label, path, whether it has token counts or only sessions, an experimental badge in the detail view, a headline figure and a trend sparkline `web/src/components/source-card.tsx:9-121`.

The span timeline lists trace spans with a glyph per span kind, a status colour and arrow key navigation using a single tab stop `web/src/components/trace.tsx:11-32` `web/src/components/trace.tsx:240-255`. The insight list turns an insight into a jump link when it names a span, and the capability grid shows a provenance badge for trace, tokens, cost, context and latency `web/src/components/trace.tsx:364-396` `web/src/components/trace.tsx:408-435`.

## What a reader must know

- Colours come from CSS variables such as `--state-priced` and `--chart-other`, not from fixed values, so the theme decides the look `web/src/components/series.ts:3-5` `web/src/components/status.tsx:8-29`.
- Only three files have tests: the info popover, the ranking helpers and the sparkline geometry. See [[Web UI components Tests]].

## Reference

%% generated:chunk-files start (do not edit; run brain docs generate) %%
### Files

| File | Purpose | Lines | Imports | Imported by | Code |
|---|---|---|---|---|---|
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
%% generated:chunk-files end %%

%% generated:chunk-interface start (do not edit; run brain docs generate) %%
### Public interface

| Name | Kind | File | Code |
|---|---|---|---|
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
| `Section` | function | `web/src/components/detail.tsx` | [[web/src/components/detail.tsx]] `web/src/components/detail.tsx:6` |
| `MetaGrid` | function | `web/src/components/detail.tsx` | [[web/src/components/detail.tsx]] `web/src/components/detail.tsx:28` |
| `CodeBlock` | function | `web/src/components/detail.tsx` | [[web/src/components/detail.tsx]] `web/src/components/detail.tsx:54` |
| `PathList` | function | `web/src/components/detail.tsx` | [[web/src/components/detail.tsx]] `web/src/components/detail.tsx:67` |
| `MetricInfoContent` | type | `web/src/components/metric-info.tsx` | [[web/src/components/metric-info.tsx]] `web/src/components/metric-info.tsx:15` |
| `MetricInfo` | function | `web/src/components/metric-info.tsx` | [[web/src/components/metric-info.tsx]] `web/src/components/metric-info.tsx:46` |
| `InfoGlyph` | function | `web/src/components/metric-info.tsx` | [[web/src/components/metric-info.tsx]] `web/src/components/metric-info.tsx:193` |
| `SourceSummary` | interface | `web/src/components/source-card.tsx` | [[web/src/components/source-card.tsx]] `web/src/components/source-card.tsx:9` |
| `SourceCard` | function | `web/src/components/source-card.tsx` | [[web/src/components/source-card.tsx]] `web/src/components/source-card.tsx:33` |
| `SourceDetail` | function | `web/src/components/source-card.tsx` | [[web/src/components/source-card.tsx]] `web/src/components/source-card.tsx:66` |
| `geometry` | function | `web/src/components/sparkline.tsx` | [[web/src/components/sparkline.tsx]] `web/src/components/sparkline.tsx:4` |
| `Sparkline` | function | `web/src/components/sparkline.tsx` | [[web/src/components/sparkline.tsx]] `web/src/components/sparkline.tsx:89` |
| `SPAN_KIND_GLYPH` | const | `web/src/components/trace.tsx` | [[web/src/components/trace.tsx]] `web/src/components/trace.tsx:11` |
| `SPAN_STATUS_COLOR` | const | `web/src/components/trace.tsx` | [[web/src/components/trace.tsx]] `web/src/components/trace.tsx:25` |
| `HIGH_OCCUPANCY` | const | `web/src/components/trace.tsx` | [[web/src/components/trace.tsx]] `web/src/components/trace.tsx:34` |
| `OccupancyPoint` | interface | `web/src/components/trace.tsx` | [[web/src/components/trace.tsx]] `web/src/components/trace.tsx:36` |
| `ContextOccupancy` | function | `web/src/components/trace.tsx` | [[web/src/components/trace.tsx]] `web/src/components/trace.tsx:45` |
| `TraceSpanRow` | interface | `web/src/components/trace.tsx` | [[web/src/components/trace.tsx]] `web/src/components/trace.tsx:214` |
| `SpanTimeline` | function | `web/src/components/trace.tsx` | [[web/src/components/trace.tsx]] `web/src/components/trace.tsx:227` |
| `TraceInsight` | interface | `web/src/components/trace.tsx` | [[web/src/components/trace.tsx]] `web/src/components/trace.tsx:323` |
| `InsightList` | function | `web/src/components/trace.tsx` | [[web/src/components/trace.tsx]] `web/src/components/trace.tsx:332` |
| `CapabilityGrid` | function | `web/src/components/trace.tsx` | [[web/src/components/trace.tsx]] `web/src/components/trace.tsx:416` |
| `useMediaQuery` | function | `web/src/components/use-media-query.ts` | [[web/src/components/use-media-query.ts]] `web/src/components/use-media-query.ts:3` |
| `STATE_RANK` | const | `web/src/components/rank.ts` | [[web/src/components/rank.ts]] `web/src/components/rank.ts:3` |
| `PROVENANCE_RANK` | const | `web/src/components/rank.ts` | [[web/src/components/rank.ts]] `web/src/components/rank.ts:5` |
| `worstState` | function | `web/src/components/rank.ts` | [[web/src/components/rank.ts]] `web/src/components/rank.ts:13` |
| `worstProvenance` | function | `web/src/components/rank.ts` | [[web/src/components/rank.ts]] `web/src/components/rank.ts:17` |
| `TracedDot` | function | `web/src/components/session.tsx` | [[web/src/components/session.tsx]] `web/src/components/session.tsx:7` |
| `ErrorCount` | function | `web/src/components/session.tsx` | [[web/src/components/session.tsx]] `web/src/components/session.tsx:30` |
| `TokenCell` | function | `web/src/components/session.tsx` | [[web/src/components/session.tsx]] `web/src/components/session.tsx:52` |
| `SessionSummary` | interface | `web/src/components/session.tsx` | [[web/src/components/session.tsx]] `web/src/components/session.tsx:101` |
| `SessionCard` | function | `web/src/components/session.tsx` | [[web/src/components/session.tsx]] `web/src/components/session.tsx:117` |
| `HoverEntry` | interface | `web/src/components/chart-hover.tsx` | [[web/src/components/chart-hover.tsx]] `web/src/components/chart-hover.tsx:6` |
| `HoverDetail` | interface | `web/src/components/chart-hover.tsx` | [[web/src/components/chart-hover.tsx]] `web/src/components/chart-hover.tsx:12` |
| `HoverFrame` | function | `web/src/components/chart-hover.tsx` | [[web/src/components/chart-hover.tsx]] `web/src/components/chart-hover.tsx:18` |
| `TimeSeriesRow` | interface | `web/src/components/chart-time.tsx` | [[web/src/components/chart-time.tsx]] `web/src/components/chart-time.tsx:13` |
| `TimeChart` | function | `web/src/components/chart-time.tsx` | [[web/src/components/chart-time.tsx]] `web/src/components/chart-time.tsx:23` |
| `Column` | interface | `web/src/components/columns.tsx` | [[web/src/components/columns.tsx]] `web/src/components/columns.tsx:14` |

9 more public names are omitted; see the cited files.
%% generated:chunk-interface end %%
