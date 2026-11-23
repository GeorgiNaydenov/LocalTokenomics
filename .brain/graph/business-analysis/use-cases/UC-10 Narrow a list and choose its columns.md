---
code: UC-10
primary_actor: Dashboard reader
subdomain: Web UI components area
no_models_reason: No model of the specification is declared in the code this use case cites or in a file that code imports directly.
rules:
  - A table always keeps at least one column
  - Automatic rescan every five minutes
  - Caller class names override primitive defaults
  - Drawer trace blocks show the same sample data for every traced session
  - Prototype filters do not filter the screens
  - Prototype session table shows at most 120 rows
  - Prototype splits session cost across token buckets by fixed weights
  - Screens stay mounted across the four screen tabs but not across the gallery
  - Session table row limit
  - Span text is fetched once per span
  - The date range cannot cross itself
tags:
  - ba/use-case
maturity: approved
---
# Narrow a list and choose its columns

## Description

The reader filters sessions by search text, facets, chips and dates, sorts them, and hides columns they do not need.

## Preconditions

- A table or list view is on screen with options supplied by the screen.

## Postconditions

- The filter chips list every active filter, and the hidden columns are remembered in the browser.

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

## Glossary

- [[Reader]]

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/components/filters.tsx::FilterChips | inferred
  > export function FilterChips({
- [[Code of localtokenomics]] @ implemented-by -> web/src/components/columns.tsx::ColumnChooser | inferred
  > export function ColumnChooser<T>({
