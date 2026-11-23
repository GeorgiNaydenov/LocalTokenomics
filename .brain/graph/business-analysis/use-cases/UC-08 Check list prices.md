---
code: UC-08
primary_actor: Dashboard reader
subdomain: Web area
no_models_reason: No model of the specification is declared in the code this use case cites or in a file that code imports directly.
rules:
  - A missing value is shown as unavailable, never as zero
  - A workspace tab loads its data only when first opened
  - An estimated price is marked next to the cost state
  - An explanation popover does not take focus back on close
  - Automatic rescan every five minutes
  - Cache price derivation
  - Caller class names override primitive defaults
  - Outcome notes are saved only when changed
  - Rate row state
  - Session table row limit
  - Sub cent money keeps four decimals
  - The date range cannot cross itself
  - Unavailable is never shown as zero
  - Unpriced cost stays out of totals
  - getJson refuses when !response.ok
tags:
  - ba/use-case
maturity: approved
---
# Check list prices

## Description

The Dashboard reader reviews the rate table, which rates are used, and which models were priced from a sibling rate.

## Preconditions

- The rate table and report are loaded.

## Postconditions

- The pricing view shows one row per rate with its state and spend.

## Main flow

1. The reader opens the pricing view. `web/src/App.tsx:337`
2. Each rate row gets a state from its rules and spend. `web/src/Pricing.tsx:128`

## Alternative flows

- At step 2, a model with only a prefix match is listed separately under its parent rate. `web/src/Pricing.tsx:106`

## Acceptance criteria

- An estimated bucket is not credited to the parent. `web/src/Pricing.test.ts:127`

## Glossary

- Bucket
- [[Rate table]]
- [[Reader]]
- Report

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/Pricing.tsx | inferred
  > export function buildRow(
