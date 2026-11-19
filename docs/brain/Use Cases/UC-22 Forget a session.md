---
title: UC-22 Forget a session
aliases: [UC-22, Forget a session]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [src/ai_usage_cost/api.py, src/ai_usage_cost/store.py, tests/test_api.py,
  tests/test_store.py]
generated: true
use-cases: [UC-22]
subdomain: Privacy and retention
---

# UC-22 Forget a session

> [!info] What this is
> A use case of the [[Privacy and retention]] subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Subdomain:** [[Privacy and retention]]
- **Actors:** [[Actors|A forgotten session is not stored again]], [[Actors#Person using the tool|Person using the tool]], [[Actors|Span]]
- **Maturity:** approved

## Description

The person removes the trace of a session from the store and keeps it from coming back on later scans.

## Preconditions

The session exists.

## Main flow

1. The person sends a delete for the session. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:362]]
2. The store deletes the spans and the rating. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:597]]
3. It records an exclusion. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:601]]
4. The span cache entry of that session is dropped. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:367]]

## Alternative flows

- An unknown session answers 404. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:235]]

## Postconditions

Its spans and rating are gone and an exclusion row is kept. Its requests stay in the totals.

## Acceptance criteria

- Deleting removes the trace but not the requests. [[tests/test_api.py|tests/test_api.py:553]]
- The exclusion survives a later scan. [[tests/test_store.py|tests/test_store.py:665]]
- Only the deleted session's cache entry is dropped. [[tests/test_api.py|tests/test_api.py:427]]

## Business rules

- [[Privacy and retention Rules#BR-121 Unreadable span text answers 404|BR-121 Unreadable span text answers 404]]
- [[Privacy and retention Rules#BR-73 A forgotten session is not stored again|BR-73 A forgotten session is not stored again]]
- [[Privacy and retention Rules#BR-74 An excluded project drops its spans|BR-74 An excluded project drops its spans]]

## Code

- [[src/ai_usage_cost/api.py]]
- [[src/ai_usage_cost/store.py]]
- [[tests/test_api.py]]
- [[tests/test_store.py]]
