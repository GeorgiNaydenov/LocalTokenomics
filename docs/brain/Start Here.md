---
title: Start Here
aliases: []
tags: [overview]
area: navigation
status: active
audience: internal
maturity: approved
confidence: confirmed
covers: []
---

# Start Here

This vault documents the codebase in chunks. Every statement cites the code it describes, and every note
declares the code it owns in `covers`.

## How to read it
- Pick a role in [[Reading Paths by Role]].
- Browse by area: Business, Architecture, Application, Data, Technology, Security, Operations.
- Diagrams live under the `architecture/` folder next to this vault and are embedded from their wrapper notes in Diagrams.
- Decisions are in the `adr/` folder next to this vault; the generated ADR Index lists them after the first `brain docs generate`, which also replaces this page with `00 Start Here`.

## Conventions
- Code is the truth. A note that disagrees with the code is marked stale by `brain docs check`.
- Text between generated markers is produced by `brain docs generate`; never edit it by hand.
- Confidence `inferred` means the statement was derived from code or documents, not confirmed by a person.
