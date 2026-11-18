---
title: Web UI components Tests
aliases: []
tags: [tests]
area: application
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/components/*]
verified-against: e5313fbd7062
chunk: ch-localtokenomics-web-src-components
---

# Web UI components Tests

The tests that cover the Web UI components chunk and what they check.

## How it works

18 tests exercise this chunk. 40 of its 43 files are not imported by any test.

Three areas have tests. The `MetricInfo` popover is tested for opening on click, for closing on a second click without focus returning to the trigger, and for rendering the structured content `web/src/components/metric-info.test.tsx:7-63`. The ranking helpers are tested for picking the worst value, for an empty list and for ignoring input order `web/src/components/rank.test.ts:4-35`. The sparkline geometry is tested for scaling, staying inside the box and flat series `web/src/components/sparkline.test.ts:4-29`.

Nothing else here has a test: the stat cards, the stacked time chart, the filter controls, the column chooser and the session and trace views. A change to them is checked only by running the dashboard.

## Reference

%% generated:chunk-tests start (do not edit; run brain docs generate) %%
| Test | Scenario | File | Code |
|---|---|---|---|
| `MetricInfo` | Metric info | `web/src/components/metric-info.test.tsx` | [[web/src/components/metric-info.test.tsx]] `web/src/components/metric-info.test.tsx:6` |
| `opens on click and shows the simple content` | Opens on click and shows the simple content | `web/src/components/metric-info.test.tsx` | [[web/src/components/metric-info.test.tsx]] `web/src/components/metric-info.test.tsx:7` |
| `closes on a second click and does not return focus to the trigger` | Closes on a second click and does not return focus to the trigger | `web/src/components/metric-info.test.tsx` | [[web/src/components/metric-info.test.tsx]] `web/src/components/metric-info.test.tsx:17` |
| `renders the rich metric content with meaning, formula and computed value` | Renders the rich metric content with meaning, formula and computed value | `web/src/components/metric-info.test.tsx` | [[web/src/components/metric-info.test.tsx]] `web/src/components/metric-info.test.tsx:43` |
| `worstState` | Worst state | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:4` |
| `picks unavailable over unpriced, free and priced` | Picks unavailable over unpriced, free and priced | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:5` |
| `picks unpriced over free and priced` | Picks unpriced over free and priced | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:9` |
| `returns unavailable for an empty list` | Returns unavailable for an empty list | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:13` |
| `is order-independent` | Is order-independent | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:17` |
| `worstProvenance` | Worst provenance | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:23` |
| `picks unavailable as the worst` | Picks unavailable as the worst | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:24` |
| `picks measured as the best when nothing worse is present` | Picks measured as the best when nothing worse is present | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:28` |
| `returns unavailable for an empty list` | Returns unavailable for an empty list | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:32` |
| `geometry` | Geometry | `web/src/components/sparkline.test.ts` | [[web/src/components/sparkline.test.ts]] `web/src/components/sparkline.test.ts:4` |
| `scales a series that peaks below 1 to the real max instead of flattening it` | Scales a series that peaks below 1 to the real max instead of flattening it | `web/src/components/sparkline.test.ts` | [[web/src/components/sparkline.test.ts]] `web/src/components/sparkline.test.ts:5` |
| `keeps every y coordinate inside the viewBox height for a series with negative dips` | Keeps every y coordinate inside the view box height for a series with negative dips | `web/src/components/sparkline.test.ts` | [[web/src/components/sparkline.test.ts]] `web/src/components/sparkline.test.ts:10` |
| `falls back to a flat line without dividing by zero when every value is identical` | Falls back to a flat line without dividing by zero when every value is identical | `web/src/components/sparkline.test.ts` | [[web/src/components/sparkline.test.ts]] `web/src/components/sparkline.test.ts:19` |
| `draws the highest value nearest the top of the box` | Draws the highest value nearest the top of the box | `web/src/components/sparkline.test.ts` | [[web/src/components/sparkline.test.ts]] `web/src/components/sparkline.test.ts:24` |
%% generated:chunk-tests end %%
