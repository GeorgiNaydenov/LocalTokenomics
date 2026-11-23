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
maturity: draft
---
# Source

## Description

The frozen description of one reader: id, label, client names, default roots, file lister, parse function, token data flag, display path, optional spans, capabilities, experimental flag and resume hook.

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

## Used by

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-14 Read a tool's SQLite store without a token count]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-22 Forget a session]]

## Sources

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/sources/base.py | inferred
  > class Source:
