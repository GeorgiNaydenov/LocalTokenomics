---
archetype: entity
subdomain: Spend reporting
tags:
  - ba/model
maturity: approved
---
# Outcome

## Description

The rating a person gives to a session, with notes and tags, plus signals computed from its spans. `src/ai_usage_cost/trace.py:147`

## Attributes

- source, session_id: identity
- outcome: successful, partial, failed, abandoned or unrated
- notes, tags, updated_at, signals

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/trace.py::Outcome | inferred
  > class Outcome(OutcomeUpdate):
