---
title: UC-08 Check list prices
aliases: [UC-08, Check list prices]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [web/src/App.tsx, web/src/Pricing.tsx, web/src/Pricing.test.ts]
generated: true
use-cases: [UC-08]
subdomain: ''
---

# UC-08 Check list prices

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Actors:** [[Actors#Dashboard reader|Dashboard reader]]
- **Maturity:** approved

## Description

The Dashboard reader reviews the rate table, which rates are used, and which models were priced from a sibling rate.

## Preconditions

The rate table and report are loaded.

## Main flow

1. The reader opens the pricing view. [[web/src/App.tsx|web/src/App.tsx:337]]
2. Each rate row gets a state from its rules and spend. [[web/src/Pricing.tsx|web/src/Pricing.tsx:128]]

## Alternative flows

- At step 2, a model with only a prefix match is listed separately under its parent rate. [[web/src/Pricing.tsx|web/src/Pricing.tsx:106]]

## Postconditions

The pricing view shows one row per rate with its state and spend.

## Acceptance criteria

- An estimated bucket is not credited to the parent. [[web/src/Pricing.test.ts|web/src/Pricing.test.ts:127]]

## Business rules

- [[General Rules#BR-20 Rate row state|BR-20 Rate row state]]
- [[General Rules#BR-25 Automatic rescan every five minutes|BR-25 Automatic rescan every five minutes]]

## Code

- [[web/src/App.tsx]]
- [[web/src/Pricing.tsx]]
- [[web/src/Pricing.test.ts]]
