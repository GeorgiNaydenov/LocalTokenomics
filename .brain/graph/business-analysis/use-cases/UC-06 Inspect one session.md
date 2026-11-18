---
code: UC-06
primary_actor: Dashboard reader
tags:
  - ba/use-case
maturity: approved
---
# Inspect one session

## Description

The Dashboard reader opens a session to see its summary, trace, economics and context.

## Preconditions

A report with sessions is loaded.

## Postconditions

The workspace shows the selected tab; trace, economics and context are fetched only once requested.

## Main flow

1. The reader selects a session row. `web/src/App.tsx:287`
2. The workspace asks for the outcome at once. `web/src/SessionWorkspace.tsx:471`
3. A tab's data is fetched when that tab was requested. `web/src/SessionWorkspace.tsx:472`

## Alternative flows

- At step 3, a failed fetch shows the endpoint did not answer note with the error text. `web/src/SessionWorkspace.tsx:561`

## Acceptance criteria

- A trace breaks into turns by turn id. `web/src/TraceTab.test.ts:196`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/SessionWorkspace.tsx | inferred
  > const trace = useLazyResource<Trace>(requested.includes('trace'), loadTrace)
