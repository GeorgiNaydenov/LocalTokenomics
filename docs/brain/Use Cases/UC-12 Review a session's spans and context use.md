---
title: UC-12 Review a session's spans and context use
aliases: [UC-12, Review a session's spans and context use]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [web/src/components/trace.tsx]
generated: true
use-cases: [UC-12]
subdomain: ''
---

# UC-12 Review a session's spans and context use

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Actors:** [[Actors#Dashboard reader|Dashboard reader]]
- **Maturity:** approved

## Description

The reader opens a session and steps through its trace spans, insights and context window occupancy.

## Preconditions

Trace spans or occupancy points were supplied for the session.

## Main flow

1. The span timeline lists spans with a glyph per kind and a colour per status. [[web/src/components/trace.tsx|web/src/components/trace.tsx:227]]
2. Arrow keys, Home and End move between rows with one tab stop. [[web/src/components/trace.tsx|web/src/components/trace.tsx:247]]
3. An insight that names a span is a button that selects it. [[web/src/components/trace.tsx|web/src/components/trace.tsx:389]]
4. The occupancy chart shows a bar per call in the warning colour at 85 percent or more. [[web/src/components/trace.tsx|web/src/components/trace.tsx:157]]

## Alternative flows

- At step 4, a call with unknown occupancy is a hatched bar with a note that it is not zero. [[web/src/components/trace.tsx|web/src/components/trace.tsx:206]]

## Postconditions

The reader has seen each span with its kind and status, and which calls came close to a full context window.

## Acceptance criteria

- No automated test covers this flow. Criterion from the code: unknown occupancy is shown as unknown, never as zero. [[web/src/components/trace.tsx|web/src/components/trace.tsx:206]]

## Code

- [[web/src/components/trace.tsx]]
