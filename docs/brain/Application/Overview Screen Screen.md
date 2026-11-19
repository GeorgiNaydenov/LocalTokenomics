---
title: Overview Screen Screen
aliases: []
tags: [ui, reference, screen-map]
area: application
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/prototype/**]
verified-against: 5796e68c0471
chunk: ch-localtokenomics-web-src-prototype
---

# Overview Screen Screen

The Overview screen (`web/src/prototype/OverviewScreen.tsx:370-386`). The map is [[Overview Screen Screen Map]]; each numbered badge in the image is one row below. The panels are separate small components in one file, so the rows follow the order on screen, not the order of the file.

## Screen map

| # | Element | What it does | Handler or target | State it depends on | Citation |
|---|---|---|---|---|---|
| 1 | `<PanelHeader` detected readers | Title that counts the readers that found logs out of all readers, with a hint that cost is never invented. | - | `SOURCES` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:48-52` |
| 2 | `<SourceCard` one card per detected reader | Card with the reader name, path, headline cost or request count, and a daily trend. | - | `detected` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:55-72` |
| 3 | `missing > 0` conditional section | Link style row, drawn only when some readers found nothing. | - | conditional: `missing > 0` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:75-83` |
| 4 | `<button` more readers ship with the tool | Row button that moves the user to the Sources screen. | `onSeeAll` (the Sources tab) | `missing` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:76-82` |
| 5 | `<StatGrid` KPI row | Six column grid that holds the five KPI tiles. | - | `PROTOTYPE_SLICE` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:93` |
| 6 | `<Stat` API equivalent cost | Hero tile with the total cost and a cost sparkline. | - | `TOTALS.cost` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:94-101` |
| 7 | `<Stat` tokens | Tile with total tokens and a cache read sparkline. | - | `TOTALS.tokens` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:115-120` |
| 8 | `<Stat` requests | Tile with total requests and a daily sparkline. | - | `TOTALS.requests` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:123-128` |
| 9 | `<Stat` sessions | Tile with total sessions and the average cost of one. | - | `TOTALS.sessions` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:131-136` |
| 10 | `<Stat` cache saved | Tile with the money saved by caching and its share of the no cache price. | - | `TOTALS.cacheSavings` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:139-144` |
| 11 | `<ToggleGroup` stack by | Segmented control that stacks the chart by client, provider or model. | `setStackBy` | `stackBy` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:178-188` |
| 12 | `<ToggleGroup` metric | Segmented control that switches the chart between cost and tokens. | `setMetric` | `metric` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:189-198` |
| 13 | `<TimeChart` daily stacked bars | Stacked daily chart built from the sample series. | - | `days`, `rows` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:203-209` |
| 14 | `<PanelNote` chart reading note | Note that explains the bars, the dashed mean line and the gaps. | - | - | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:211-213` |
| 15 | `<MeterRow` one row per model | Ranked cost bar for each model; free and unpriced models keep a row with their state. | - | `ranked` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:233-246` |
| 16 | `<Legend` token buckets | Legend with the four token buckets and their price multipliers. | - | `TOKEN_BUCKETS` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:270-277` |
| 17 | `<BucketBar` bar per model | Stacked token bar for each model that logged tokens. | - | `model.tokens` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:287-294` |
| 18 | `<ComparisonMeter` billed with no cache discount | Full length meter for the same tokens at full input price. | - | `TOTALS.noCacheEquivalent` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:319-324` |
| 19 | `<ComparisonMeter` actually billed | Shorter meter for the cost at cache rates. | - | `TOTALS.cost` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:325-329` |
| 20 | `<MeterRow` one row per project | Cost bar for each project, led by the biggest. | - | `PROJECTS` | [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:352-359` |

### Conditional sections

- conditional: `missing > 0`, callout 3, [[web/src/prototype/OverviewScreen.tsx]] `web/src/prototype/OverviewScreen.tsx:75-83`

## Diagnosis

**What the user can do.** Read the detected readers, the five KPI tiles, the daily chart and the four breakdown panels `web/src/prototype/OverviewScreen.tsx:373-383`. Two segmented controls change the chart: one stacks it by client, provider or model and one switches between cost and tokens `web/src/prototype/OverviewScreen.tsx:178-198`. A row button under the reader cards moves the user to the Sources screen `web/src/prototype/OverviewScreen.tsx:76-82`.

**What can go wrong.**

- The screen has one prop, a callback to the Sources tab `web/src/prototype/OverviewScreen.tsx:370-370`. It reads its numbers from constants, so the filter rail beside it changes the chips but not one figure on this screen `web/src/prototype/Screens.tsx:360-361`.
- The cost by model panel reads the first model of the ranked list without a check `web/src/prototype/OverviewScreen.tsx:219-227`, and the project panel reads the first project the same way `web/src/prototype/OverviewScreen.tsx:348-348`. With real data and no models or no projects, both panels would fail. The prototype never meets that case because the lists are literal.
- Averages and shares divide by totals without a guard against zero `web/src/prototype/OverviewScreen.tsx:90-90` `web/src/prototype/OverviewScreen.tsx:261-261`. An empty machine would show values that are not numbers.
- The two segmented controls ignore a click on the active option, so a choice can never be cleared `web/src/prototype/OverviewScreen.tsx:183-183` `web/src/prototype/OverviewScreen.tsx:194-194`. That is intended, but it means the chart always has one stack and one metric.

**States the code does not handle.**

- No loading state: the sample series is available at once `web/src/prototype/OverviewScreen.tsx:25-35`. The gallery shows skeleton shapes, but this screen never uses them.
- No error state for a failed scan, and no empty state for a machine where no reader found logs: the detected reader grid would simply be empty under a title that says zero readers `web/src/prototype/OverviewScreen.tsx:48-74`.
