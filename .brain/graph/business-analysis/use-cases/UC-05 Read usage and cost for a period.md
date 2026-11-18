---
code: UC-05
primary_actor: Dashboard reader
tags:
  - ba/use-case
maturity: approved
---
# Read usage and cost for a period

## Description

The Dashboard reader sees token usage and list price cost, filtered by date, client, model, project and cost state.

## Preconditions

The ai-usage-cost server is running.

## Postconditions

The overview, sessions, sources or pricing view shows the filtered slice.

## Main flow

1. The page loads metadata and rates together. `web/src/App.tsx:168`
2. The report is fetched for the current query. `web/src/App.tsx:186`
3. The chosen view renders once its data is present. `web/src/App.tsx:333`

## Alternative flows

- At step 1, an unreachable server shows an offline card with a retry button. `web/src/api.ts:494`

## Acceptance criteria

- A value under one cent keeps four decimal places. `web/src/format.test.ts:27`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/App.tsx | inferred
  > fetchReport(query, controller.signal)
