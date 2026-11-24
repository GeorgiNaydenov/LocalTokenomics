---
archetype: entity
fields: []
tags:
  - ba/model
maturity: draft
---
# SpanStatus

## Description

The entity SpanStatus, declared in web/src/api.ts line 80. It is the entity that the state machine SpanStatus lifecycle describes.

## Lifecycle

Lifecycle is described by [[SpanStatus lifecycle]].

## Used by

- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-12 Review a session's spans and context use]]

## Sources

- [[Code of localtokenomics]] @ declared-in -> web/src/api.ts::SpanStatus | inferred
  > export type SpanStatus = 'ok' | 'error' | 'interrupted' | 'aborted' | 'running' | 'unknown'
