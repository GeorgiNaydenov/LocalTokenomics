---
title: UC-07 Rate a session outcome
aliases: [UC-07, Rate a session outcome]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [web/src/SessionWorkspace.tsx, web/src/api.ts]
generated: true
use-cases: [UC-07]
subdomain: ''
---

# UC-07 Rate a session outcome

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Actors:** [[Actors#Dashboard reader|Dashboard reader]]
- **Maturity:** approved

## Description

The Dashboard reader marks a session successful, partial, failed, abandoned or unrated and adds notes and tags.

## Preconditions

A session workspace is open.

## Main flow

1. The reader picks an outcome label. [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx:312]]
2. The page sends it with PUT. [[web/src/api.ts|web/src/api.ts:577]]

## Alternative flows

- At step 2, a failed save shows the error text in the status line. [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx:287]]

## Postconditions

The server holds the outcome, notes and tags.

## Acceptance criteria

- Notes and tags are not resent when unchanged. [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx:292]]

## Business rules

- [[General Rules#BR-124 A workspace tab loads its data only when first opened|BR-124 A workspace tab loads its data only when first opened]]
- [[General Rules#BR-15 Unavailable is never shown as zero|BR-15 Unavailable is never shown as zero]]
- [[General Rules#BR-16 Unpriced cost stays out of totals|BR-16 Unpriced cost stays out of totals]]
- [[General Rules#BR-24 Outcome notes are saved only when changed|BR-24 Outcome notes are saved only when changed]]

## Code

- [[web/src/SessionWorkspace.tsx]]
- [[web/src/api.ts]]
