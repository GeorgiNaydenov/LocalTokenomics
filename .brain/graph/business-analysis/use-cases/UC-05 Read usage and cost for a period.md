---
code: UC-05
primary_actor: Dashboard reader
subdomain: Web area
no_models_reason: No model of the specification is declared in the code this use case cites or in a file that code imports directly.
rules:
  - A rollup shows its least trustworthy cost state and provenance
  - A workspace tab loads its data only when first opened
  - Automatic rescan every five minutes
  - Cache price derivation
  - Outcome notes are saved only when changed
  - Rate age notice thresholds
  - Rate row state
  - Reported cost divergence threshold
  - Session table row limit
  - Span text is fetched once per span
  - Unattributed turn is excluded from rankings
  - Unavailable is never shown as zero
  - Unpriced cost stays out of totals
  - getJson refuses when !response.ok
  - A missing value is shown as unavailable, never as zero
  - An estimated price is marked next to the cost state
  - Caller class names override primitive defaults
  - Prototype figures are invented
  - Prototype session table shows at most 120 rows
  - Sub cent money keeps four decimals
  - The date range cannot cross itself
tags:
  - ba/use-case
maturity: approved
---
# Read usage and cost for a period

## Description

The Dashboard reader sees token usage and list price cost, filtered by date, client, model, project and cost state.

## Preconditions

- The ai-usage-cost server is running.

## Postconditions

- The overview, sessions, sources or pricing view shows the filtered slice.

## Main flow

1. The page loads metadata and rates together. `web/src/App.tsx:168`
2. The report is fetched for the current query. `web/src/App.tsx:186`
3. The chosen view renders once its data is present. `web/src/App.tsx:333`

## Alternative flows

- At step 1, an unreachable server shows an offline card with a retry button. `web/src/api.ts:494`

## Acceptance criteria

- A value under one cent keeps four decimal places. `web/src/format.test.ts:27`

## Glossary

- [[Cost state]]
- [[Reader]]
- Report

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/App.tsx | inferred
  > fetchReport(query, controller.signal)
