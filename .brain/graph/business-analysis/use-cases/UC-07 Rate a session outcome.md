---
code: UC-07
primary_actor: Dashboard reader
tags:
  - ba/use-case
maturity: approved
---
# Rate a session outcome

## Description

The Dashboard reader marks a session successful, partial, failed, abandoned or unrated and adds notes and tags.

## Preconditions

A session workspace is open.

## Postconditions

The server holds the outcome, notes and tags.

## Main flow

1. The reader picks an outcome label. `web/src/SessionWorkspace.tsx:312`
2. The page sends it with PUT. `web/src/api.ts:577`

## Alternative flows

- At step 2, a failed save shows the error text in the status line. `web/src/SessionWorkspace.tsx:287`

## Acceptance criteria

- Notes and tags are not resent when unchanged. `web/src/SessionWorkspace.tsx:292`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/SessionWorkspace.tsx | inferred
  > function OutcomeControl(props
