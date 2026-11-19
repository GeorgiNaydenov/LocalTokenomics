---
code: UC-21
primary_actor: Person using the tool
subdomain: Spend reporting
level: goal
actors:
  - Person using the tool
models:
  - Span
  - Outcome
rules:
  - An unknown session answers 404
tags:
  - ba/use-case
maturity: approved
---
# Inspect and rate one session

## Description

The person opens the trace of a session, sees where cost and errors came from, and records whether it went well.

## Preconditions

The session exists in the store.

## Postconditions

A rating is stored for the session.

## Main flow

1. The person asks for the trace of a session. `src/ai_usage_cost/api.py:321`
2. The interface loads the spans once and caches them. `src/ai_usage_cost/api.py:240`
3. The person asks for the economics of the session, which are summed per turn, model and tool. `src/ai_usage_cost/api.py:336`
4. The person stores a rating with notes and tags. `src/ai_usage_cost/api.py:358`
5. The stored rating comes back with signals computed from the spans. `src/ai_usage_cost/api.py:359`

## Alternative flows

- An unknown session answers 404. `src/ai_usage_cost/api.py:236`

## Acceptance criteria

- An unknown session has no trace. `tests/test_api.py:364`
- An outcome round trips and carries computed signals. `tests/test_api.py:525`
- Economics totals equal the sum over model calls. `tests/test_api.py:454`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/api.py::create_app | inferred
  > def trace(source: str, session_id: str)
