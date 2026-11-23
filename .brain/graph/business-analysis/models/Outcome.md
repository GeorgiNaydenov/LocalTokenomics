---
archetype: entity
subdomain: Spend reporting
tags:
  - ba/model
maturity: draft
---
# Outcome

## Description

The rating a person gives to a session, with notes and tags, plus signals computed from its spans. `src/ai_usage_cost/trace.py:147`

## Attributes

- source, session_id: identity
- outcome: successful, partial, failed, abandoned or unrated
- notes, tags, updated_at, signals

## Used by

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-14 Read a tool's SQLite store without a token count]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::Outcome | inferred
  > class Outcome(OutcomeUpdate):
