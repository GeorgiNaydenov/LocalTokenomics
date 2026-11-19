---
title: UC-06 Inspect one session
aliases: [UC-06, Inspect one session]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [web/src/App.tsx, web/src/SessionWorkspace.tsx, web/src/TraceTab.test.ts]
generated: true
use-cases: [UC-06]
subdomain: ''
---

# UC-06 Inspect one session

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Actors:** [[Actors#Dashboard reader|Dashboard reader]]
- **Maturity:** approved

## Description

The Dashboard reader opens a session to see its summary, trace, economics and context.

## Preconditions

A report with sessions is loaded.

## Main flow

1. The reader selects a session row. [[web/src/App.tsx|web/src/App.tsx:287]]
2. The workspace asks for the outcome at once. [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx:471]]
3. A tab's data is fetched when that tab was requested. [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx:472]]

## Alternative flows

- At step 3, a failed fetch shows the endpoint did not answer note with the error text. [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx:561]]

## Postconditions

The workspace shows the selected tab; trace, economics and context are fetched only once requested.

## Acceptance criteria

- A trace breaks into turns by turn id. [[web/src/TraceTab.test.ts|web/src/TraceTab.test.ts:196]]

## Business rules

- [[General Rules#BR-124 A workspace tab loads its data only when first opened|BR-124 A workspace tab loads its data only when first opened]]
- [[General Rules#BR-15 Unavailable is never shown as zero|BR-15 Unavailable is never shown as zero]]
- [[General Rules#BR-16 Unpriced cost stays out of totals|BR-16 Unpriced cost stays out of totals]]
- [[General Rules#BR-24 Outcome notes are saved only when changed|BR-24 Outcome notes are saved only when changed]]
- [[General Rules#BR-25 Automatic rescan every five minutes|BR-25 Automatic rescan every five minutes]]

## Code

- [[web/src/App.tsx]]
- [[web/src/SessionWorkspace.tsx]]
- [[web/src/TraceTab.test.ts]]
