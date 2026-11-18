---
code: UC-08
primary_actor: Dashboard reader
tags:
  - ba/use-case
maturity: approved
---
# Check list prices

## Description

The Dashboard reader reviews the rate table, which rates are used, and which models were priced from a sibling rate.

## Preconditions

The rate table and report are loaded.

## Postconditions

The pricing view shows one row per rate with its state and spend.

## Main flow

1. The reader opens the pricing view. `web/src/App.tsx:337`
2. Each rate row gets a state from its rules and spend. `web/src/Pricing.tsx:128`

## Alternative flows

- At step 2, a model with only a prefix match is listed separately under its parent rate. `web/src/Pricing.tsx:106`

## Acceptance criteria

- An estimated bucket is not credited to the parent. `web/src/Pricing.test.ts:127`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/Pricing.tsx | inferred
  > export function buildRow(
