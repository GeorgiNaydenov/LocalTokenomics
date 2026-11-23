---
code: UC-07
primary_actor: Dashboard reader
subdomain: Web area
no_models_reason: No model of the specification is declared in the code this use case cites or in a file that code imports directly.
rules:
  - A missing value is shown as unavailable, never as zero
  - A rollup shows its least trustworthy cost state and provenance
  - A workspace tab loads its data only when first opened
  - An estimated price is marked next to the cost state
  - An explanation popover does not take focus back on close
  - Automatic rescan every five minutes
  - Cache price derivation
  - Caller class names override primitive defaults
  - Outcome notes are saved only when changed
  - Prototype figures are invented
  - Prototype session table shows at most 120 rows
  - Rate age notice thresholds
  - Rate row state
  - Reported cost divergence threshold
  - Session table row limit
  - Sheet opens from the right by default
  - Span text is fetched once per span
  - Sub cent money keeps four decimals
  - The daily chart names at most twelve series
  - The side panel width is bounded
  - Toggle group settings win over item settings
  - Unattributed turn is excluded from rankings
  - Unavailable is never shown as zero
  - Unpriced cost stays out of totals
  - getJson refuses when !response.ok
tags:
  - ba/use-case
maturity: approved
---
# Rate a session outcome

## Description

The Dashboard reader marks a session successful, partial, failed, abandoned or unrated and adds notes and tags.

## Preconditions

- A session workspace is open.

## Postconditions

- The server holds the outcome, notes and tags.

## Main flow

1. The reader picks an outcome label. `web/src/SessionWorkspace.tsx:312`
2. The page sends it with PUT. `web/src/api.ts:577`

## Alternative flows

- At step 2, a failed save shows the error text in the status line. `web/src/SessionWorkspace.tsx:287`

## Acceptance criteria

- Notes and tags are not resent when unchanged. `web/src/SessionWorkspace.tsx:292`

## Glossary

- Outcome
- [[Reader]]
- [[Session]]

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/SessionWorkspace.tsx | inferred
  > function OutcomeControl(props
