---
archetype: entity
fields:
  - 'id: str'
  - 'label: str'
  - 'clients: dict[str, str]'
  - 'default_roots: Callable[[], list[Path]]'
  - 'files: Callable[[Path], list[Path]]'
  - 'parse: Callable[[Path, list[str]], Iterator[UsageEvent]]'
  - 'token_data: TokenData'
  - 'display_path: str'
  - 'spans: Callable[[Path, list[str]], Iterator[Span]] | None'
  - 'capabilities: Capabilities'
  - 'experimental: bool'
  - 'parse_resume: Callable[[Path, list[str], int, str | None], Iterator[UsageEvent]] | None'
entity_keys: []
relations_to: []
tags:
  - ba/model
maturity: approved
---
# Source

## Description

The entity Source, declared in src/ai_usage_cost/sources/base.py lines 18-44. It has 12 fields and 0 relations.

## Attributes

- id: str
- label: str
- clients: dict[str, str]
- default_roots: Callable[[], list[Path]]
- files: Callable[[Path], list[Path]]
- parse: Callable[[Path, list[str]], Iterator[UsageEvent]]
- token_data: TokenData
- display_path: str
- spans: Callable[[Path, list[str]], Iterator[Span]] | None
- capabilities: Capabilities
- experimental: bool
- parse_resume: Callable[[Path, list[str], int, str | None], Iterator[UsageEvent]] | None

## Lifecycle

No lifecycle field was found in the code.

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/sources/base.py::Source | inferred
  > class Source:
