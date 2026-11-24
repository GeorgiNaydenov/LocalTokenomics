---
archetype: entity
fields: []
tags:
  - ba/model
maturity: draft
---
# SpanKind

## Description

The entity SpanKind, declared in web/src/api.ts line 67. It is the entity that the state machine SpanKind lifecycle describes.

## Lifecycle

Lifecycle is described by [[SpanKind lifecycle]].

## Used by

- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-12 Review a session's spans and context use]]

## Sources

- [[Code of localtokenomics]] @ declared-in -> web/src/api.ts::SpanKind | inferred
  > export type SpanKind =
