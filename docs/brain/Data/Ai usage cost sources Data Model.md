---
title: Ai usage cost sources Data Model
aliases: []
tags: [data, erd]
area: data
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/sources/**]
verified-against: 8a1d896ab1c8
chunk: ch-localtokenomics-src-ai-usage-cost-sources
approved-by: human
approved-at: '2026-11-18T19:05:23+00:00'
---

# Ai usage cost sources Data Model

The entities owned by the Ai usage cost sources chunk.

## How it works

2 entities were found with their columns, defaults, keys, relations and enumerated values. This is the data dictionary of the chunk; tables created only by demo, fixture or seed files are listed here and kept out of the diagrams; the conceptual, logical and physical diagrams are listed in [[Ai usage cost sources Diagrams]].

Both entities are plain frozen dataclasses, not stored tables. `Source` is the description of one reader. `src/ai_usage_cost/sources/base.py:17-40` `Spec` holds the per tool settings the Cline family shares: the source id, the client name, the extension id, whether the input token count already includes cache buckets, and whether the SDK store is read. `src/ai_usage_cost/sources/cline.py:81-87`

`TokenData` is a two value literal, `full` or `session`, which says whether a reader yields token counts or only session presence. `src/ai_usage_cost/sources/base.py:14` The events a reader yields are the `UsageEvent` model of another module, which this chunk only fills. `src/ai_usage_cost/sources/base.py:11`

## Reference

%% generated:chunk-entities start (do not edit; run brain docs generate) %%
### Entity summary

| Entity | Table | Columns | Key | Relations | Referenced by | Code |
|---|---|---|---|---|---|---|
| Source | - | 12 | - | 0 | - | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:18-44` |
| Spec | - | 5 | - | 0 | - | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:82-87` |

### Source

Defined at [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:18-44`. Specification note: Source.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `id` | `str` | yes |  | - | - |
| `label` | `str` | yes |  | - | - |
| `clients` | `dict[str, str]` | yes |  | - | - |
| `default_roots` | `Callable[[], list[Path]]` | yes |  | - | - |
| `files` | `Callable[[Path], list[Path]]` | yes |  | - | - |
| `parse` | `Callable[[Path, list[str]], Iterator[UsageEvent]]` | yes |  | - | - |
| `token_data` | `TokenData` | yes |  | - | values of `TokenData` |
| `display_path` | `str` | yes |  | - | - |
| `spans` | `Callable[[Path, list[str]], Iterator[Span]] \| None` | yes |  | - | - |
| `capabilities` | `Capabilities` | yes |  | - | - |
| `experimental` | `bool` | yes |  | - | - |
| `parse_resume` | `Callable[[Path, list[str], int, str \| None], Iterator[UsageEvent]] \| None` | yes |  | - | - |

No relations were extracted.

### Spec

Defined at [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:82-87`. Specification note: Spec.

| Column | Type | Null | Key | Default | Note |
|---|---|---|---|---|---|
| `source_id` | `str` | yes |  | - | - |
| `client` | `str` | yes |  | - | - |
| `ext_id` | `str` | yes |  | - | - |
| `tokens_in_inclusive` | `bool` | yes |  | - | - |
| `sdk` | `bool` | yes |  | - | - |

No relations were extracted.

### Enumerated values

| Type | Values | Code |
|---|---|---|
| `TokenData` | `full`, `session` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:14` |
%% generated:chunk-entities end %%
