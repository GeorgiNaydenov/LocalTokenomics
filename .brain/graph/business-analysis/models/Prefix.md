---
archetype: entity
fields:
  - 'prefix: str'
  - 'provider: str | None'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Prefix

## Description

The entity Prefix, declared in src/ai_usage_cost/pricing.py lines 169-171. It has 2 fields and 0 relations.

## Attributes

- prefix: str
- provider: str | None

## Lifecycle

No lifecycle field was found in the code.

## Used by

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/pricing.py::Prefix | inferred
  > class Prefix(BaseModel):
