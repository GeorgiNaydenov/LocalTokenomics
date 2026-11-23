---
archetype: entity
fields:
  - 'match: str'
  - 'note: str'
  - 'status: Literal[''watchlist'', ''no_list_price''] | None'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# UnpricedModel

## Description

The entity UnpricedModel, declared in src/ai_usage_cost/pricing.py lines 232-242. It has 3 fields and 0 relations.

## Attributes

- match: str
- note: str
- status: Literal['watchlist', 'no_list_price'] | None

## Lifecycle

No lifecycle field was found in the code.

## Used by

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/pricing.py::UnpricedModel | inferred
  > class UnpricedModel(BaseModel):
