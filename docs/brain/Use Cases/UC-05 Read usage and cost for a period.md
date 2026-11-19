---
title: UC-05 Read usage and cost for a period
aliases: [UC-05, Read usage and cost for a period]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [web/src/App.tsx, web/src/api.ts, web/src/format.test.ts]
generated: true
use-cases: [UC-05]
subdomain: ''
---

# UC-05 Read usage and cost for a period

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Actors:** [[Actors#Dashboard reader|Dashboard reader]]
- **Maturity:** approved

## Description

The Dashboard reader sees token usage and list price cost, filtered by date, client, model, project and cost state.

## Preconditions

The ai-usage-cost server is running.

## Main flow

1. The page loads metadata and rates together. [[web/src/App.tsx|web/src/App.tsx:168]]
2. The report is fetched for the current query. [[web/src/App.tsx|web/src/App.tsx:186]]
3. The chosen view renders once its data is present. [[web/src/App.tsx|web/src/App.tsx:333]]

## Alternative flows

- At step 1, an unreachable server shows an offline card with a retry button. [[web/src/api.ts|web/src/api.ts:494]]

## Postconditions

The overview, sessions, sources or pricing view shows the filtered slice.

## Acceptance criteria

- A value under one cent keeps four decimal places. [[web/src/format.test.ts|web/src/format.test.ts:27]]

## Business rules

- [[General Rules#BR-25 Automatic rescan every five minutes|BR-25 Automatic rescan every five minutes]]

## Code

- [[web/src/App.tsx]]
- [[web/src/api.ts]]
- [[web/src/format.test.ts]]
