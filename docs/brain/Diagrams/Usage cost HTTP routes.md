---
title: Usage cost HTTP routes
aliases: []
tags: [api-map, diagram, drawio]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [src/ai_usage_cost/*]
sources: [docs/brain/architecture/drawio/drawio-usage-cost-http-routes.drawio]
chunk: ch-localtokenomics-src-ai-usage-cost
authored: true
node_citations:
  drawio-usage-cost-http-routes:
    analysis:
    - src/ai_usage_cost/api.py:255-392
    analysis_m0:
    - src/ai_usage_cost/api.py:255-289
    analysis_p0:
    - src/ai_usage_cost/api.py:255-289
    analysis_m1:
    - src/ai_usage_cost/api.py:289-318
    analysis_p1:
    - src/ai_usage_cost/api.py:289-318
    analysis_m2:
    - src/ai_usage_cost/api.py:384-386
    analysis_p2:
    - src/ai_usage_cost/api.py:384-386
    analysis_m3:
    - src/ai_usage_cost/api.py:388-392
    analysis_p3:
    - src/ai_usage_cost/api.py:388-392
    session:
    - src/ai_usage_cost/api.py:230-242
    session_m0:
    - src/ai_usage_cost/api.py:320-331
    session_p0:
    - src/ai_usage_cost/api.py:320-331
    session_m1:
    - src/ai_usage_cost/api.py:333-343
    session_p1:
    - src/ai_usage_cost/api.py:333-343
    session_m2:
    - src/ai_usage_cost/api.py:345-348
    session_p2:
    - src/ai_usage_cost/api.py:345-348
    session_m3:
    - src/ai_usage_cost/api.py:350-353
    session_p3:
    - src/ai_usage_cost/api.py:350-353
    session_m4:
    - src/ai_usage_cost/api.py:355-359
    session_p4:
    - src/ai_usage_cost/api.py:355-359
    session_m5:
    - src/ai_usage_cost/api.py:361-368
    session_p5:
    - src/ai_usage_cost/api.py:361-368
    session_m6:
    - src/ai_usage_cost/api.py:370-382
    session_p6:
    - src/ai_usage_cost/api.py:370-382
    dash:
    - src/ai_usage_cost/api.py:394-402
    dash_m0:
    - src/ai_usage_cost/api.py:394-395
    dash_p0:
    - src/ai_usage_cost/api.py:394-395
    dash_m1:
    - src/ai_usage_cost/api.py:396-402
    dash_p1:
    - src/ai_usage_cost/api.py:396-402
---

# Usage cost HTTP routes

This map lists every address the local dashboard talks to, grouped by what it serves. It shows which calls only read numbers and which ones change stored data, such as rating or forgetting a session. It also makes plain that no address asks who is calling, so the tool relies on staying on the local machine.

## What the diagram shows

- One function builds the application, keeps the current analysis in memory and caches the spans of each session until the next refresh. `src/ai_usage_cost/api.py:198-214`
- The meta route returns the clients, providers, models, projects, day range, rate table age, grouped warning counts and source list. `src/ai_usage_cost/api.py:255-287`
- The report route passes every filter of its query string to the report builder. `src/ai_usage_cost/api.py:289-318`
- The rates route returns the loaded rate table, and the refresh route runs the analysis again, clears the span cache and returns fresh meta. `src/ai_usage_cost/api.py:384-392`
- The trace, economics, context and outcome routes read one session's spans through a helper that answers 404 when the session is unknown or was forgotten. `src/ai_usage_cost/api.py:230-242` `src/ai_usage_cost/api.py:320-353`
- The economics route labels each turn with a redacted snippet of its first user message, and only when the privacy settings release text. `src/ai_usage_cost/api.py:333-343` `src/ai_usage_cost/api.py:70-83`
- The put route stores a rating with notes and tags and returns it with fresh signals. `src/ai_usage_cost/api.py:355-359`
- The delete route forgets a session, drops its cached spans and returns how many spans it deleted. `src/ai_usage_cost/api.py:361-368`
- The content route returns the text of one span and answers 404 when the span is missing or its text is not released. `src/ai_usage_cost/api.py:370-382`
- The root serves the built dashboard when the bundle folder exists, and otherwise a message that tells the reader how to build it. `src/ai_usage_cost/api.py:394-402`
- Any route that opens the store answers 503 when the analysis was built without one. `src/ai_usage_cost/api.py:219-223`

## Capability and related functionality

- Serves the use cases explore spend in the dashboard, inspect and rate one session, forget a session and read the text of one span, drawn in [[Usage cost goals]].
- The route list with its parameters is in [[Ai usage cost API]], and the refusals are drawn in [[Usage cost refusals]].
- The serve command that starts this application on the loopback address is in [[Ai usage cost Workflows]], and the missing caller check is a risk in [[Ai usage cost Security]].

## Usage cost HTTP routes

![[docs/brain/architecture/rendered/drawio-usage-cost-http-routes.svg]]

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `src/ai_usage_cost/api.py:198-253` | Application, span cache, store and session helpers |
> | `src/ai_usage_cost/api.py:255-318` | Meta and report routes |
> | `src/ai_usage_cost/api.py:320-382` | Session routes |
> | `src/ai_usage_cost/api.py:384-402` | Rates, refresh and dashboard routes |
