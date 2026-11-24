---
archetype: entity
fields: []
tags:
  - ba/model
maturity: draft
---
# WarningsList

## Description

The entity WarningsList, declared in web/src/components/states.tsx line 247. It is the entity that the state machine Warnings list view describes.

## Lifecycle

Lifecycle is described by [[Warnings list view]].

## Used by

- [[UC-01 Compare a dashboard screen with its reference]]
- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-28 Sort the session list and open one session in the prototype]]

## Sources

- [[Code of localtokenomics]] @ declared-in -> web/src/components/states.tsx::WarningsList | inferred
  > export function WarningsList({ groups, className }: { groups: WarningGroup[]; className?: string }) {
