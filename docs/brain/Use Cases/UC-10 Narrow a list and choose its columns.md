---
title: UC-10 Narrow a list and choose its columns
aliases: [UC-10, Narrow a list and choose its columns]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [web/src/components/filters.tsx, web/src/components/columns.tsx]
generated: true
use-cases: [UC-10]
subdomain: ''
---

# UC-10 Narrow a list and choose its columns

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Actors:** [[Actors#Dashboard reader|Dashboard reader]]
- **Maturity:** approved

## Description

The reader filters sessions by search text, facets, chips and dates, sorts them, and hides columns they do not need.

## Preconditions

A table or list view is on screen with options supplied by the screen.

## Main flow

1. The reader types in the search box or ticks facet options. [[web/src/components/filters.tsx|web/src/components/filters.tsx:18]]
2. The reader picks a sort order. [[web/src/components/filters.tsx|web/src/components/filters.tsx:195]]
3. The reader sets a from and to date. [[web/src/components/filters.tsx|web/src/components/filters.tsx:156]]
4. Active filters appear as removable chips with a Clear all link. [[web/src/components/filters.tsx|web/src/components/filters.tsx:231]]
5. The reader opens the column menu and ticks columns, which are stored. [[web/src/components/columns.tsx|web/src/components/columns.tsx:41]]

## Alternative flows

- At step 5, when every column is hidden, all columns are shown. [[web/src/components/columns.tsx|web/src/components/columns.tsx:59]]

## Postconditions

The filter chips list every active filter, and the hidden columns are remembered in the browser.

## Acceptance criteria

- No automated test covers this flow. Criterion from the code: hiding every column leaves all columns visible. [[web/src/components/columns.tsx|web/src/components/columns.tsx:59]]

## Code

- [[web/src/components/filters.tsx]]
- [[web/src/components/columns.tsx]]
