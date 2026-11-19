---
title: Usage collection Rules
aliases: []
tags: [business, generated, rules, spec]
area: business
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [src/ai_usage_cost/sources/base.py, src/ai_usage_cost/store.py]
generated: true
anchors: true
---

# Usage collection Rules

> [!info] What this is
> The business rules of the [[Usage collection]] subdomain, as the code enforces them. Each rule is a heading, so a use case links straight to it, and each names the line of code that enforces it.

## BR-119 Schema migrations only run forward

Opening the store runs every migration after the stored schema version, in list order, and records the new version after each; there is no downgrade step. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:147]]

- **Category:** data

Source:
- `open_store`: `for index, migration in enumerate(MIGRATIONS[current:], start=current):`

## BR-69 A request is stored once per fingerprint

A later record with the same fingerprint replaces an earlier one only when it carries more output, because streamed records grow and the last one holds the billed count. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:359]]

- **Category:** data integrity

Source:
- `_insert`: `the last (equivalently, largest) record carries the final, billed count`

## BR-70 Records that disagree on input tokens keep the first

When two records for one request disagree on input tokens, the first is kept and a warning is added. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:352]]

- **Category:** data integrity

Source:
- `_insert`: `disagree on input tokens -- keeping the first`

## BR-71 An unchanged file is not parsed again

A file whose modification time, size and parser version match the stored values is skipped. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:229]]

- **Category:** performance

Source:
- `ingest`: `(mtime, size, PARSER_VERSION) == prior[:3]`

## BR-72 A grown file resumes only when its earlier bytes are unchanged

A file is read from its old end only when its source has a resume hook, it only grew, the previous scan reached its old end and a hash of the bytes before that point still matches. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:250]]

- **Category:** performance

Source:
- `ingest`: `_boundary_hash(path, prior[1]) == prior[4]`

## BR-86 Source databases are opened read only

A source database is opened with a read only URI, so the tool never changes another tool's data. [[src/ai_usage_cost/sources/base.py|src/ai_usage_cost/sources/base.py:123]]

- **Category:** privacy

Source:
- `read_sqlite`: `?mode=ro`
