---
title: Web ui UI components Overview
aliases: []
tags: [module, overview]
area: application
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/components/ui/**]
verified-against: 6ba75315bb66
chunk: ch-localtokenomics-web-src-components-ui
approved-by: human
approved-at: '2026-11-18T19:04:28+00:00'
---

# Web ui UI components Overview

What Web ui UI components is made of and how it connects to the rest of the code.

## How it works

Web ui UI components holds 25 source files and 2083 lines. The most depended-on files are `web/src/components/ui/button.tsx`, `web/src/components/ui/tooltip.tsx`, `web/src/components/ui/table.tsx`. It uses [[Web Overview]]. It is used by [[Web UI components Overview]], [[Web Overview]], [[Web prototype Overview]].

The purpose column quotes each file's own header comment where it has one. Every file is cited by its full line range, and every public name by the line that declares it.

## What this layer is for

This folder is the design system layer of the dashboard. Each file wraps one interface primitive, such as a button, an input, a dialog or a table, so that screens never style these elements from scratch. Screens import the primitives and compose them, for example `web/src/FilterRail.tsx:9-13` pulls in `Button`, `Label`, `Separator`, `Sheet` and `Switch` to build the filter panel.

Every primitive joins its class names through the shared `cn` helper, which combines `clsx` with `tailwind-merge` (`web/src/design-system/cn.ts:1-6`). A caller can therefore pass a `className` that overrides a default style without leaving two conflicting utility classes on the element (`web/src/components/ui/input.tsx:9-14`).

Each primitive also stamps a `data-slot` attribute on its element, for example `button` (`web/src/components/ui/button.tsx:54`) and `input` (`web/src/components/ui/input.tsx:8`). Variants are exposed as `data-variant` and `data-size` attributes as well (`web/src/components/ui/button.tsx:55-56`), so parent components and tests can target a part of a primitive by name.

## Families of primitives

### Actions and status

`Button` offers the variants default, destructive, outline, secondary, ghost and link, and the sizes default, xs, sm, lg and four icon sizes (`web/src/components/ui/button.tsx:10-31`). It is the most reused primitive in the chunk, and its `asChild` option lets it hand its styling to another element through Radix `Slot` (`web/src/components/ui/button.tsx:44-50`). `Badge` is the small pill counterpart with its own variants, and it supports `asChild` the same way (`web/src/components/ui/badge.tsx:10-35`). The dashboard uses it for markers on source cards and pricing rows (`web/src/components/source-card.tsx:3`, `web/src/Pricing.tsx:28`).

`Alert` renders a bordered message with `role="alert"` and a title and description part (`web/src/components/ui/alert.tsx:21-34`). `Skeleton` is a pulsing placeholder block, and `Progress` shows a bar whose indicator is shifted by the `value` prop (`web/src/components/ui/skeleton.tsx:3-11`, `web/src/components/ui/progress.tsx:19-23`). `web/src/components/states.tsx:126-129` composes skeletons into the loading panel.

### Form controls

`Input` and `Textarea` share one look: a bordered field with a focus ring and a red ring when `aria-invalid` is set (`web/src/components/ui/input.tsx:9-14`, `web/src/components/ui/textarea.tsx:8-13`). `Label`, `Checkbox` and `Switch` wrap Radix controls (`web/src/components/ui/label.tsx:10-18`, `web/src/components/ui/checkbox.tsx:13-27`, `web/src/components/ui/switch.tsx:15-30`). `Switch` takes a `size` of `sm` or `default` (`web/src/components/ui/switch.tsx:7-13`). The session workspace builds its edit form from `Button`, `Input`, `Label` and `Textarea` (`web/src/SessionWorkspace.tsx:35-38`).

`Select` is a set of parts: trigger, content, item, group, label, separator and scroll buttons (`web/src/components/ui/select.tsx:6-176`). The trigger has a `size` of `sm` or `default` and always draws a chevron icon (`web/src/components/ui/select.tsx:24-46`). The filter bar uses it together with `Checkbox`, `Input` and `Label` (`web/src/components/filters.tsx:4-14`).

`Toggle` is a two state button, and `ToggleGroup` places several of them in a row. The group passes its variant, size and spacing to every item through a React context, and an item falls back to its own props only when the group sets none (`web/src/components/ui/toggle-group.tsx:8-16`, `web/src/components/ui/toggle-group.tsx:42-44`, `web/src/components/ui/toggle-group.tsx:62-63`). Because the group is reused in six files, it is the usual way the dashboard offers a choice between a few modes (`web/src/Overview.tsx:38`, `web/src/TraceTab.tsx:19`).

### Overlays and disclosure

`Dialog` and `Sheet` are both built on the Radix dialog primitive. Each has a trigger, portal, overlay, content, header, footer, title and description part, and each content part shows a close button with a screen reader label unless `showCloseButton` is false (`web/src/components/ui/dialog.tsx:50-82`, `web/src/components/ui/sheet.tsx:44-83`). `SheetContent` adds a `side` option for top, right, bottom or left, defaulting to right (`web/src/components/ui/sheet.tsx:44-53`). The dashboard uses sheets for slide in panels, such as the filter rail on small screens (`web/src/FilterRail.tsx:486-495`). The only consumer of `Dialog` found in the dashboard is the component gallery (`web/src/prototype/Gallery.tsx:292`).

`Popover`, `Tooltip` and `DropdownMenu` render their content in a portal so that it is not clipped by the panel that owns the trigger (`web/src/components/ui/popover.tsx:23-35`, `web/src/components/ui/tooltip.tsx:38-52`, `web/src/components/ui/dropdown-menu.tsx:31-49`). `TooltipProvider` sets the default hover delay to zero, and the dashboard roots wrap the app in a provider with a 200 ms delay (`web/src/components/ui/tooltip.tsx:7-18`, `web/src/main.tsx:9-11`, `web/src/prototype/Prototype.tsx:32`). The file table below shows `Tooltip` is imported by ten files, the second highest count in the folder.

`Accordion` and `Collapsible` hide and reveal content. The accordion trigger sits inside a header and adds a chevron, while `Collapsible` is a thin wrapper that adds only `data-slot` attributes (`web/src/components/ui/accordion.tsx:27-47`, `web/src/components/ui/collapsible.tsx:3-9`). `web/src/components/states.tsx:150-169` composes a collapsible panel from the trigger and content parts. `Tabs` splits a view into panes, with a `default` and a `line` list variant (`web/src/components/ui/tabs.tsx:8-40`).

The toast host `Toaster` is the one primitive that depends on app state: it reads the current theme mode from `useTheme` and passes it to the Sonner toaster, and it maps the toast colours to the popover theme variables (`web/src/components/ui/sonner.tsx:10-34`). The prototype mounts it once at the bottom right (`web/src/prototype/Prototype.tsx:109`).

### Data display

`Table` wraps a native table in a container that scrolls horizontally, and the header, body, footer, row, head, cell and caption parts each add their own styling (`web/src/components/ui/table.tsx:4-17`, `web/src/components/ui/table.tsx:104-113`). The pricing and sessions screens compose them for their rate and session lists (`web/src/Pricing.tsx:37`, `web/src/Sessions.tsx:29`).

The chart file is the only large one, and it adapts Recharts rather than Radix. `ChartContainer` takes a `ChartConfig` that maps each series to a label, an icon and either one colour or a light and dark colour pair, and it shares that config with its children through a context (`web/src/components/ui/chart.tsx:12-27`, `web/src/components/ui/chart.tsx:60-77`). `ChartStyle` turns the config into CSS variables, one per series key and prefixed with `--color-`, scoped to the chart's own id, in one block for light and one for the `.dark` selector (`web/src/components/ui/chart.tsx:7`, `web/src/components/ui/chart.tsx:81-112`). The tooltip and legend content parts read the same config, and `useChart` throws when they are used outside a container (`web/src/components/ui/chart.tsx:29-37`, `web/src/components/ui/chart.tsx:282`). The time chart builds its config and renders inside the container (`web/src/components/chart-time.tsx:63`, `web/src/components/chart-time.tsx:99`).

## What a reader must know

- The folder has no logic of its own about tokens or costs. Business meaning lives in the screens that compose these parts.
- No test file lives in this folder, so the primitives are exercised only through the screens that use them.
- Most overlay and form primitives are split into several exported parts, so a screen imports the root and the parts it needs, as `web/src/FilterRail.tsx:12` does for the sheet.

## Reference

%% generated:chunk-files start (do not edit; run brain docs generate) %%
### Files

| File | Purpose | Lines | Imports | Imported by | Code |
|---|---|---|---|---|---|
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
%% generated:chunk-files end %%

%% generated:chunk-interface start (do not edit; run brain docs generate) %%
### Public interface

| Name | Kind | File | Code |
|---|---|---|---|
| `ChartConfig` | type | `web/src/components/ui/chart.tsx` | [[web/src/components/ui/chart.tsx]] `web/src/components/ui/chart.tsx:12` |
%% generated:chunk-interface end %%
