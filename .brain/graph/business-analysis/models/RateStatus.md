---
archetype: entity
fields: []
tags:
  - ba/model
maturity: draft
---
# RateStatus

## Description

The entity RateStatus, declared in web/src/api.ts line 435. It is the entity that the state machine RateStatus lifecycle describes.

## Lifecycle

Lifecycle is described by [[RateStatus lifecycle]].

## Used by

- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-12 Review a session's spans and context use]]

## Sources

- [[Code of localtokenomics]] @ declared-in -> web/src/api.ts::RateStatus | inferred
  > export type RateStatus = 'ga' | 'preview' | 'retired'
