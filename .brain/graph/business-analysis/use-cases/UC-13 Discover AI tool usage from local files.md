---
code: UC-13
tags:
  - ba/use-case
maturity: approved
---
# Discover AI tool usage from local files

## Description

The tool finds the logs and data stores of the supported AI coding tools on this machine and turns each into usage events, without changing any of them.

## Preconditions

At least one supported tool has written data in a default root, or the user passes a root.

## Postconditions

Usage events and a file record exist in the usage store for every readable file.

## Main flow

1. 1. The registry collects the SOURCE of every reader module. `src/ai_usage_cost/sources/__init__.py:17`
2. 2. The store keeps only the roots that exist. `src/ai_usage_cost/sources/base.py:49`
3. 3. The reader lists the files under each root. `src/ai_usage_cost/store.py:220`
4. 4. Unchanged files are skipped. `src/ai_usage_cost/store.py:230`
5. 5. The reader parses a changed file into usage events. `src/ai_usage_cost/store.py:255`
6. 6. The store writes the event rows and a file record. `src/ai_usage_cost/store.py:281`

## Alternative flows

A file that cannot be read adds a warning and is skipped. `src/ai_usage_cost/store.py:225`

## Acceptance criteria

The Claude Code reader skips synthetic and zero token records. `tests/test_claude_code.py:102`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/sources/__init__.py | inferred
  > def registry() -> dict[str, Source]:
