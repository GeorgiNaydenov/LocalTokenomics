---
archetype: entity
fields: []
tags:
  - ba/model
maturity: draft
---
# Workspace tab

## Description

The entity Workspace tab, declared in web/src/SessionWorkspace.tsx line 49. It is the entity that the state machine Workspace tab data describes.

## Lifecycle

Lifecycle is described by [[Workspace tab data]].

## Used by

- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]

## Sources

- [[Code of localtokenomics]] @ declared-in -> web/src/SessionWorkspace.tsx | inferred
  > export type WorkspaceTab = 'summary' | 'trace' | 'economics' | 'context'
