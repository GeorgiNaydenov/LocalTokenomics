---
title: Economics Tab Screen Map
aliases: []
tags: [diagram, drawio, screen-map]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
sources: [docs/brain/architecture/drawio/drawio-screen-economics-tab.drawio]
chunk: ch-localtokenomics-web-src
authored: true
screen-note: Economics Tab Screen
node_citations:
  drawio-screen-economics-tab:
    el-1: ['web/src/EconomicsTab.tsx:615-615']
    el-2: ['web/src/EconomicsTab.tsx:635-635']
    el-3: ['web/src/EconomicsTab.tsx:663-663']
    el-4: ['web/src/EconomicsTab.tsx:674-674']
    el-5: ['web/src/EconomicsTab.tsx:683-683']
    el-6: ['web/src/EconomicsTab.tsx:694-694']
    el-7: ['web/src/EconomicsTab.tsx:705-705']
    el-8: ['web/src/EconomicsTab.tsx:715-715']
    el-9: ['web/src/EconomicsTab.tsx:439-444']
    el-10: ['web/src/EconomicsTab.tsx:508-508']
    el-11: ['web/src/EconomicsTab.tsx:555-561']
    el-12: ['web/src/EconomicsTab.tsx:568-568']
    el-13: ['web/src/EconomicsTab.tsx:573-573']
    el-14: ['web/src/EconomicsTab.tsx:578-583']
    el-15: ['web/src/EconomicsTab.tsx:588-588']
    el-16: ['web/src/EconomicsTab.tsx:747-747']
    el-17: ['web/src/EconomicsTab.tsx:758-758']
    el-18: ['web/src/EconomicsTab.tsx:402-402']
    el-19: ['web/src/EconomicsTab.tsx:415-415']
    badge-1: ['web/src/EconomicsTab.tsx:615-615']
    badge-2: ['web/src/EconomicsTab.tsx:635-635']
    badge-3: ['web/src/EconomicsTab.tsx:663-663']
    badge-4: ['web/src/EconomicsTab.tsx:674-674']
    badge-5: ['web/src/EconomicsTab.tsx:683-683']
    badge-6: ['web/src/EconomicsTab.tsx:694-694']
    badge-7: ['web/src/EconomicsTab.tsx:705-705']
    badge-8: ['web/src/EconomicsTab.tsx:715-715']
    badge-9: ['web/src/EconomicsTab.tsx:439-444']
    badge-10: ['web/src/EconomicsTab.tsx:508-508']
    badge-11: ['web/src/EconomicsTab.tsx:555-561']
    badge-12: ['web/src/EconomicsTab.tsx:568-568']
    badge-13: ['web/src/EconomicsTab.tsx:573-573']
    badge-14: ['web/src/EconomicsTab.tsx:578-583']
    badge-15: ['web/src/EconomicsTab.tsx:588-588']
    badge-16: ['web/src/EconomicsTab.tsx:747-747']
    badge-17: ['web/src/EconomicsTab.tsx:758-758']
    badge-18: ['web/src/EconomicsTab.tsx:402-402']
    badge-19: ['web/src/EconomicsTab.tsx:415-415']
    region-1: ['web/src/EconomicsTab.tsx:615-615', 'web/src/EconomicsTab.tsx:635-635',
      'web/src/EconomicsTab.tsx:663-663', 'web/src/EconomicsTab.tsx:674-674', 'web/src/EconomicsTab.tsx:683-683',
      'web/src/EconomicsTab.tsx:694-694', 'web/src/EconomicsTab.tsx:705-705', 'web/src/EconomicsTab.tsx:715-715']
    region-2: ['web/src/EconomicsTab.tsx:439-444', 'web/src/EconomicsTab.tsx:508-508']
    region-3: ['web/src/EconomicsTab.tsx:555-561', 'web/src/EconomicsTab.tsx:568-568',
      'web/src/EconomicsTab.tsx:573-573', 'web/src/EconomicsTab.tsx:578-583', 'web/src/EconomicsTab.tsx:588-588']
    region-4: ['web/src/EconomicsTab.tsx:747-747']
    region-5: ['web/src/EconomicsTab.tsx:758-758']
    region-6: ['web/src/EconomicsTab.tsx:402-402', 'web/src/EconomicsTab.tsx:415-415']
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Economics Tab Screen Map

This map shows where a reader sees what one session cost and where the cost came from. It lets them find the costliest turn, the slowest one and the one with errors, and compare models and tools. It also shows which figures are left blank when the log does not carry them.

## What the diagram shows

- Eight totals open the tab, each with an explanation and an unavailable marker where the log lacks the figure `web/src/EconomicsTab.tsx:614-730`.
- Turn insight cards select a turn in the per turn table and show all turns when the turn is outside the top list `web/src/EconomicsTab.tsx:425-510` `web/src/EconomicsTab.tsx:526-531`.
- The per turn table starts with the top turns by cost; sorting is offered after Show all `web/src/EconomicsTab.tsx:521-523` `web/src/EconomicsTab.tsx:554-567`.
- Per model and per tool tables share one panel with an empty state and batch reveal `web/src/EconomicsTab.tsx:376-423` `web/src/EconomicsTab.tsx:747-767`.

## Capability and related functionality

The tab lives inside [[Session Workspace Screen]]. The turn insights come from the helpers described in [[Web Overview]], and the unattributed turn rule is in [[Web Specification]].

## Economics Tab Screen screen map

![[docs/brain/architecture/rendered/drawio-screen-economics-tab.svg]]

> [!example]- Code references
> | Badge | Element | Code |
> |---|---|---|
> | 1 | `<Stat` Tokens | `web/src/EconomicsTab.tsx:615-615` |
> | 2 | `<Stat` Cost | `web/src/EconomicsTab.tsx:635-635` |
> | 3 | `<Stat` Duration | `web/src/EconomicsTab.tsx:663-663` |
> | 4 | `<Stat` Calls | `web/src/EconomicsTab.tsx:674-674` |
> | 5 | `<Stat` Retries | `web/src/EconomicsTab.tsx:683-683` |
> | 6 | `<Stat` Amplification | `web/src/EconomicsTab.tsx:694-694` |
> | 7 | `<Stat` Cache hit ratio | `web/src/EconomicsTab.tsx:705-705` |
> | 8 | `<Stat` Tokens per second | `web/src/EconomicsTab.tsx:715-715` |
> | 9 | `<Stat` Cost concentration and other cards | `web/src/EconomicsTab.tsx:439-444` |
> | 10 | `cards.length === 0` empty section | `web/src/EconomicsTab.tsx:508-508` |
> | 11 | `<SortSelect` Sort turns | `web/src/EconomicsTab.tsx:555-561` |
> | 12 | `<ColumnChooser` columns | `web/src/EconomicsTab.tsx:568-568` |
> | 13 | `props.rows.length === 0` empty section | `web/src/EconomicsTab.tsx:573-573` |
> | 14 | `<DataRows` turn rows | `web/src/EconomicsTab.tsx:578-583` |
> | 15 | `<Button` Show all | `web/src/EconomicsTab.tsx:588-588` |
> | 16 | `<EconPanel` Per model | `web/src/EconomicsTab.tsx:747-747` |
> | 17 | `<EconPanel` Per tool | `web/src/EconomicsTab.tsx:758-758` |
> | 18 | `props.rows.length === 0` empty section | `web/src/EconomicsTab.tsx:402-402` |
> | 19 | `<Button` Show more | `web/src/EconomicsTab.tsx:415-415` |
