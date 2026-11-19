---
code: UC-22
primary_actor: Person using the tool
subdomain: Privacy and retention
level: goal
actors:
  - Person using the tool
models:
  - Span
rules:
  - A forgotten session is not stored again
tags:
  - ba/use-case
maturity: approved
---
# Forget a session

## Description

The person removes the trace of a session from the store and keeps it from coming back on later scans.

## Preconditions

The session exists.

## Postconditions

Its spans and rating are gone and an exclusion row is kept. Its requests stay in the totals.

## Main flow

1. The person sends a delete for the session. `src/ai_usage_cost/api.py:362`
2. The store deletes the spans and the rating. `src/ai_usage_cost/store.py:597`
3. It records an exclusion. `src/ai_usage_cost/store.py:601`
4. The span cache entry of that session is dropped. `src/ai_usage_cost/api.py:367`

## Alternative flows

- An unknown session answers 404. `src/ai_usage_cost/api.py:235`

## Acceptance criteria

- Deleting removes the trace but not the requests. `tests/test_api.py:553`
- The exclusion survives a later scan. `tests/test_store.py:665`
- Only the deleted session's cache entry is dropped. `tests/test_api.py:427`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/api.py::create_app | inferred
  > def forget_session(source: str, session_id: str)
