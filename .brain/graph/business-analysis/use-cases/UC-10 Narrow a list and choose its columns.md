---
code: UC-10
primary_actor: Dashboard reader
tags:
  - ba/use-case
maturity: approved
---
# Narrow a list and choose its columns

## Description

The reader filters sessions by search text, facets, chips and dates, sorts them, and hides columns they do not need.

## Preconditions

A table or list view is on screen with options supplied by the screen.

## Postconditions

The filter chips list every active filter, and the hidden columns are remembered in the browser.

## Main flow

1. The reader types in the search box or ticks facet options. `web/src/components/filters.tsx:18`
2. The reader picks a sort order. `web/src/components/filters.tsx:195`
3. The reader sets a from and to date. `web/src/components/filters.tsx:156`
4. Active filters appear as removable chips with a Clear all link. `web/src/components/filters.tsx:231`
5. The reader opens the column menu and ticks columns, which are stored. `web/src/components/columns.tsx:41`

## Alternative flows

- At step 5, when every column is hidden, all columns are shown. `web/src/components/columns.tsx:59`

## Acceptance criteria

- No automated test covers this flow. Criterion from the code: hiding every column leaves all columns visible. `web/src/components/columns.tsx:59`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/components/filters.tsx::FilterChips | inferred
  > export function FilterChips({
- [[Code of localtokenomics]] @ implemented-by -> web/src/components/columns.tsx::ColumnChooser | inferred
  > export function ColumnChooser<T>({
