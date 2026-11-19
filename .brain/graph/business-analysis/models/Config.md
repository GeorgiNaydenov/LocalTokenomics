---
archetype: value object
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
maturity: draft
---
# Config

## Description

The privacy settings read from config.json in the store folder. `src/ai_usage_cost/privacy.py:52`

## Attributes

- metadata_only: default true
- exclude_projects, max_content_bytes
- metadata_retention_days, content_retention_days: default None

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/privacy.py::Config | inferred
  > class Config(BaseModel):
