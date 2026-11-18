---
archetype: value object
subdomain: Spend reporting
tags:
  - ba/model
maturity: draft
---
# Bucket

## Description

A group of priced events under one key such as a client, provider, model, project or day, with summed tokens and cost. `src/ai_usage_cost/models.py:123`

## Attributes

- key, label, tokens, cost, events, sessions, reported_cost

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/models.py::Bucket | inferred
  > class Bucket(BaseModel):
