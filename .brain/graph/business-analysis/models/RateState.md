---
archetype: entity
fields: []
tags:
  - ba/model
maturity: draft
---
# RateState

## Description

The entity RateState, declared in web/src/Pricing.tsx line 55. It is the entity that the state machine RateState lifecycle describes.

## Lifecycle

Lifecycle is described by [[RateState lifecycle]].

## Used by

- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]

## Sources

- [[Code of localtokenomics]] @ declared-in -> web/src/Pricing.tsx::RateState | inferred
  > type RateState = 'free' | 'priced' | 'unused'
