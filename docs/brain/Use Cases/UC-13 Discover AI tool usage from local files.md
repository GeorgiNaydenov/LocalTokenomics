---
title: UC-13 Discover AI tool usage from local files
aliases: [UC-13, Discover AI tool usage from local files]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [src/ai_usage_cost/sources/__init__.py, src/ai_usage_cost/sources/base.py,
  src/ai_usage_cost/store.py, tests/test_claude_code.py]
generated: true
use-cases: [UC-13]
subdomain: ''
---

# UC-13 Discover AI tool usage from local files

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Maturity:** approved

## Description

The tool finds the logs and data stores of the supported AI coding tools on this machine and turns each into usage events, without changing any of them.

## Preconditions

At least one supported tool has written data in a default root, or the user passes a root.

## Main flow

1. 1. The registry collects the SOURCE of every reader module. [[src/ai_usage_cost/sources/__init__.py|src/ai_usage_cost/sources/__init__.py:17]]
2. 2. The store keeps only the roots that exist. [[src/ai_usage_cost/sources/base.py|src/ai_usage_cost/sources/base.py:49]]
3. 3. The reader lists the files under each root. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:220]]
4. 4. Unchanged files are skipped. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:230]]
5. 5. The reader parses a changed file into usage events. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:255]]
6. 6. The store writes the event rows and a file record. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:281]]

## Alternative flows

A file that cannot be read adds a warning and is skipped. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:225]]

## Postconditions

Usage events and a file record exist in the usage store for every readable file.

## Acceptance criteria

The Claude Code reader skips synthetic and zero token records. [[tests/test_claude_code.py|tests/test_claude_code.py:102]]

## Business rules

- [[General Rules#BR-39 Readers only read|BR-39 Readers only read]]
- [[General Rules#BR-40 A reader is found by its SOURCE value|BR-40 A reader is found by its SOURCE value]]
- [[General Rules#BR-41 Unparsable lines are skipped and counted|BR-41 Unparsable lines are skipped and counted]]
- [[General Rules#BR-45 Experimental readers carry a flag|BR-45 Experimental readers carry a flag]]

## Diagrams

- [[Reader data lineage]]
- [[Reader glossary map]]
- [[Reader module imports]]
- [[Reader types]]
- [[Readers concepts]]

## Code

- [[src/ai_usage_cost/sources/__init__.py]]
- [[src/ai_usage_cost/sources/base.py]]
- [[src/ai_usage_cost/store.py]]
- [[tests/test_claude_code.py]]
