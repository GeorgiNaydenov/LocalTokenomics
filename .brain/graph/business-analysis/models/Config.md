---
archetype: entity
subdomain: Privacy and retention
fields:
  - 'metadata_only: bool'
  - 'exclude_projects: list[str]'
  - 'max_content_bytes: int'
  - 'metadata_retention_days: int | None'
  - 'content_retention_days: int | None'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Config

## Description

The entity Config, declared in src/ai_usage_cost/privacy.py lines 52-57. It has 5 fields and 0 relations.

## Attributes

- metadata_only: bool
- exclude_projects: list[str]
- max_content_bytes: int
- metadata_retention_days: int | None
- content_retention_days: int | None

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/privacy.py::Config | inferred
  > class Config(BaseModel):
