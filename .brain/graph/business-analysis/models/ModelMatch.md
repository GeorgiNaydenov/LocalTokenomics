---
archetype: entity
fields:
  - 'match: str | None'
  - 'kind: Literal[''exact'', ''suffix'', ''estimated'', ''none'']'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# ModelMatch

## Description

The entity ModelMatch, declared in src/ai_usage_cost/pricing.py lines 224-229. It has 2 fields and 0 relations.

## Attributes

- match: str | None
- kind: Literal['exact', 'suffix', 'estimated', 'none']

## Lifecycle

No lifecycle field was found in the code.

## Used by

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/pricing.py::ModelMatch | inferred
  > class ModelMatch(BaseModel):
