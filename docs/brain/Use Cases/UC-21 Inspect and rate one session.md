---
title: UC-21 Inspect and rate one session
aliases: [UC-21, Inspect and rate one session]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [src/ai_usage_cost/api.py, tests/test_api.py]
generated: true
use-cases: [UC-21]
subdomain: Spend reporting
---

# UC-21 Inspect and rate one session

> [!info] What this is
> A use case of the [[Spend reporting]] subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Subdomain:** [[Spend reporting]]
- **Actors:** [[Actors|An unknown session answers 404]], [[Actors|Outcome]], [[Actors#Person using the tool|Person using the tool]], [[Actors|Span]]
- **Maturity:** approved

## Description

The person opens the trace of a session, sees where cost and errors came from, and records whether it went well.

## Preconditions

The session exists in the store.

## Main flow

1. The person asks for the trace of a session. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:321]]
2. The interface loads the spans once and caches them. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:240]]
3. The person asks for the economics of the session, which are summed per turn, model and tool. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:336]]
4. The person stores a rating with notes and tags. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:358]]
5. The stored rating comes back with signals computed from the spans. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:359]]

## Alternative flows

- An unknown session answers 404. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:236]]

## Postconditions

A rating is stored for the session.

## Acceptance criteria

- An unknown session has no trace. [[tests/test_api.py|tests/test_api.py:364]]
- An outcome round trips and carries computed signals. [[tests/test_api.py|tests/test_api.py:525]]
- Economics totals equal the sum over model calls. [[tests/test_api.py|tests/test_api.py:454]]

## Business rules

- [[Spend reporting Rules#BR-120 A route without a store answers 503|BR-120 A route without a store answers 503]]
- [[Spend reporting Rules#BR-85 An unknown session answers 404|BR-85 An unknown session answers 404]]

## Code

- [[src/ai_usage_cost/api.py]]
- [[tests/test_api.py]]
