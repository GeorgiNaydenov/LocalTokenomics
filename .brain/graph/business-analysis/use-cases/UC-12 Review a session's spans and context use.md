---
code: UC-12
primary_actor: Dashboard reader
subdomain: Web UI components area
no_models_reason: No model of the specification is declared in the code this use case cites or in a file that code imports directly.
rules:
  - A missing value is shown as unavailable, never as zero
  - An estimated price is marked next to the cost state
  - Caller class names override primitive defaults
  - Drawer trace blocks show the same sample data for every traced session
  - Prototype filters do not filter the screens
  - Prototype splits session cost across token buckets by fixed weights
  - Screens stay mounted across the four screen tabs but not across the gallery
  - Span text is fetched once per span
  - Tooltip provider default delay is zero
  - getJson refuses when !response.ok
tags:
  - ba/use-case
maturity: approved
---
# Review a session's spans and context use

## Description

The reader opens a session and steps through its trace spans, insights and context window occupancy.

## Preconditions

- Trace spans or occupancy points were supplied for the session.

## Postconditions

- The reader has seen each span with its kind and status, and which calls came close to a full context window.

## Main flow

1. The span timeline lists spans with a glyph per kind and a colour per status. `web/src/components/trace.tsx:227`
2. Arrow keys, Home and End move between rows with one tab stop. `web/src/components/trace.tsx:247`
3. An insight that names a span is a button that selects it. `web/src/components/trace.tsx:389`
4. The occupancy chart shows a bar per call in the warning colour at 85 percent or more. `web/src/components/trace.tsx:157`

## Alternative flows

- At step 4, a call with unknown occupancy is a hatched bar with a note that it is not zero. `web/src/components/trace.tsx:206`

## Acceptance criteria

- No automated test covers this flow. Criterion from the code: unknown occupancy is shown as unknown, never as zero. `web/src/components/trace.tsx:206`

## Glossary

- [[Reader]]
- [[Session]]
- Span

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/components/trace.tsx::SpanTimeline | inferred
  > export function SpanTimeline({
- [[Code of localtokenomics]] @ implemented-by -> web/src/components/trace.tsx::ContextOccupancy | inferred
  > export function ContextOccupancy({
