---
title: UC-27 Browse sessions in the terminal
aliases: [UC-27, Browse sessions in the terminal]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [src/ai_usage_cost/cli.py, src/ai_usage_cost/tui.py, tests/test_cli.py]
generated: true
use-cases: [UC-27]
subdomain: Spend reporting
---

# UC-27 Browse sessions in the terminal

> [!info] What this is
> A use case of the [[Spend reporting]] subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Subdomain:** [[Spend reporting]]
- **Actors:** [[Actors#Person using the tool|Person using the tool]], [[Actors|SessionRow]]
- **Maturity:** approved

## Description

The person lists and sorts sessions in a terminal table and filters them as they type.

## Preconditions

The tui extra is installed and the report has sessions.

## Main flow

1. The person runs the tui command. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:358]]
2. The command shows a notice and exits with code 1 when there are no sessions. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:371]]
3. The table is filled from the report sessions. [[src/ai_usage_cost/tui.py|src/ai_usage_cost/tui.py:119]]
4. A header click sorts and a second click reverses. [[src/ai_usage_cost/tui.py|src/ai_usage_cost/tui.py:105]]

## Alternative flows

- Without the extra the command prints an install hint and exits with code 2. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:366]]

## Postconditions

A full screen table is shown.

## Acceptance criteria

- The filter matches any visible session field. [[tests/test_cli.py|tests/test_cli.py:197]]

## Business rules

- [[Spend reporting Rules#BR-116 The alert window ends today|BR-116 The alert window ends today]]
- [[Spend reporting Rules#BR-117 A rise is measured against the window just before|BR-117 A rise is measured against the window just before]]
- [[Spend reporting Rules#BR-118 An alert fires only above the threshold|BR-118 An alert fires only above the threshold]]
- [[Spend reporting Rules#BR-84 An alert needs exactly one threshold|BR-84 An alert needs exactly one threshold]]

## Code

- [[src/ai_usage_cost/cli.py]]
- [[src/ai_usage_cost/tui.py]]
- [[tests/test_cli.py]]
