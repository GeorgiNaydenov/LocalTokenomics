---
title: UC-14 Read a tool's SQLite store without a token count
aliases: [UC-14, Read a tool's SQLite store without a token count]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [src/ai_usage_cost/sources/cursor.py, tests/test_cursor.py]
generated: true
use-cases: [UC-14]
subdomain: ''
---

# UC-14 Read a tool's SQLite store without a token count

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Maturity:** approved

## Description

For tools that keep conversations in a database and record no tokens, the reader still shows that sessions happened, with no token numbers.

## Preconditions

The tool's database file exists in a default root.

## Main flow

1. 1. The reader lists the Cursor database files. [[src/ai_usage_cost/sources/cursor.py|src/ai_usage_cost/sources/cursor.py:32]]
2. 2. The reader checks that the expected table exists. [[src/ai_usage_cost/sources/cursor.py|src/ai_usage_cost/sources/cursor.py:55]]
3. 3. It selects the composer rows through the read only helper. [[src/ai_usage_cost/sources/cursor.py|src/ai_usage_cost/sources/cursor.py:59]]
4. 4. It yields one event per composer with no tokens. [[src/ai_usage_cost/sources/cursor.py|src/ai_usage_cost/sources/cursor.py:79]]

## Alternative flows

A value that is not JSON is skipped. [[src/ai_usage_cost/sources/cursor.py|src/ai_usage_cost/sources/cursor.py:66]]

## Postconditions

One event per composer exists with tokens set to none.

## Acceptance criteria

The Cursor reader has its own test module. [[tests/test_cursor.py|tests/test_cursor.py:28]]

## Code

- [[src/ai_usage_cost/sources/cursor.py]]
- [[tests/test_cursor.py]]
