---
archetype: entity
fields:
  - 'id: str'
  - 'label: str'
  - 'clients: list[str]'
  - 'token_data: TokenData'
  - 'path: str'
  - 'root_hint: str'
  - 'detected: bool'
  - 'files: int'
  - 'capabilities: Capabilities'
  - 'experimental: bool'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# SourceInfo

## Description

The entity SourceInfo, declared in src/ai_usage_cost/pipeline.py lines 31-41. It has 10 fields and 0 relations.

## Attributes

- id: str
- label: str
- clients: list[str]
- token_data: TokenData
- path: str
- root_hint: str
- detected: bool
- files: int
- capabilities: Capabilities
- experimental: bool

## Lifecycle

No lifecycle field was found in the code.

## Used by

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-15 Print a usage and cost summary in the terminal]]
- [[UC-16 Export a usage and cost chart as a PNG image]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-19 Export a report as a file]]
- [[UC-20 Be alerted when spend rises]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]
- [[UC-24 Try the tool with demo data]]
- [[UC-25 Sample GPU use for local models]]
- [[UC-26 Query the store with SQL]]
- [[UC-27 Browse sessions in the terminal]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/pipeline.py::SourceInfo | inferred
  > class SourceInfo(BaseModel):
