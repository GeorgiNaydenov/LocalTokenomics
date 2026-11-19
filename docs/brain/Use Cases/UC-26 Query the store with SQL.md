---
title: UC-26 Query the store with SQL
aliases: [UC-26, Query the store with SQL]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [src/ai_usage_cost/cli.py, tests/test_cli.py]
generated: true
use-cases: [UC-26]
subdomain: Spend reporting
---

# UC-26 Query the store with SQL

> [!info] What this is
> A use case of the [[Spend reporting]] subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Subdomain:** [[Spend reporting]]
- **Actors:** [[Actors#Person using the tool|Person using the tool]]
- **Maturity:** approved

## Description

The person explores the stored requests with SQL in a browser through Datasette.

## Preconditions

The sql extra is installed and a store exists.

## Main flow

1. The person runs the sql command. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:229]]
2. The command needs Datasette. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:235]]
3. It checks that the store file exists. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:239]]
4. It hands the store to Datasette. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:248]]

## Alternative flows

- A missing store prints a hint and exits with code 2. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:241]]

## Postconditions

Datasette serves the store.

## Acceptance criteria

- The explicit store is handed to Datasette. [[tests/test_cli.py|tests/test_cli.py:219]]
- A missing store is named instead of launching. [[tests/test_cli.py|tests/test_cli.py:241]]

## Business rules

- [[Spend reporting Rules#BR-116 The alert window ends today|BR-116 The alert window ends today]]
- [[Spend reporting Rules#BR-117 A rise is measured against the window just before|BR-117 A rise is measured against the window just before]]
- [[Spend reporting Rules#BR-118 An alert fires only above the threshold|BR-118 An alert fires only above the threshold]]
- [[Spend reporting Rules#BR-84 An alert needs exactly one threshold|BR-84 An alert needs exactly one threshold]]

## Code

- [[src/ai_usage_cost/cli.py]]
- [[tests/test_cli.py]]
