---
code: UC-06
primary_actor: Dashboard reader
subdomain: Web area
no_models_reason: No model of the specification is declared in the code this use case cites or in a file that code imports directly.
rules:
  - An explanation popover does not take focus back on close
  - The side panel width is bounded
  - Toggle group settings win over item settings
  - A missing value is shown as unavailable, never as zero
  - A workspace tab loads its data only when first opened
  - An estimated price is marked next to the cost state
  - Automatic rescan every five minutes
  - Caller class names override primitive defaults
  - Outcome notes are saved only when changed
  - Rate age notice thresholds
  - Rate row state
  - Reported cost divergence threshold
  - Session table row limit
  - Sheet opens from the right by default
  - Span text is fetched once per span
  - Sub cent money keeps four decimals
  - The daily chart names at most twelve series
  - The date range cannot cross itself
  - Unavailable is never shown as zero
  - Unpriced cost stays out of totals
  - getJson refuses when !response.ok
tags:
  - ba/use-case
maturity: approved
---
# Inspect one session

## Description

The Dashboard reader opens a session to see its summary, trace, economics and context.

## Preconditions

- A report with sessions is loaded.

## Postconditions

- The workspace shows the selected tab; trace, economics and context are fetched only once requested.

## Main flow

1. The reader selects a session row. `web/src/App.tsx:287`
2. The workspace asks for the outcome at once. `web/src/SessionWorkspace.tsx:471`
3. A tab's data is fetched when that tab was requested. `web/src/SessionWorkspace.tsx:472`

## Alternative flows

- At step 3, a failed fetch shows the endpoint did not answer note with the error text. `web/src/SessionWorkspace.tsx:561`

## Acceptance criteria

- A trace breaks into turns by turn id. `web/src/TraceTab.test.ts:196`

## Glossary

- Outcome
- [[Reader]]
- Report
- [[Session]]

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/SessionWorkspace.tsx | inferred
  > const trace = useLazyResource<Trace>(requested.includes('trace'), loadTrace)
