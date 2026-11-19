---
title: UC-15 Print a usage and cost summary in the terminal
aliases: [UC-15, Print a usage and cost summary in the terminal]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [src/ai_usage_cost/cli.py, src/ai_usage_cost/render/terminal.py]
generated: true
use-cases: [UC-15]
subdomain: ''
---

# UC-15 Print a usage and cost summary in the terminal

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Actors:** [[Actors#CLI user|CLI user]]
- **Maturity:** approved

## Description

A user runs the scan command and reads the headline cost and one breakdown table as text.

## Preconditions

Usage was found: the scan command exits with code 1 and a hint when the report has no events.

## Main flow

1. 1. The user runs scan; the command builds the report and, when --json is not set, passes it to the terminal renderer. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:105]]
2. 2. The renderer prints the Total panel with cost, tokens, requests, sessions, date span, log file count and rates date. [[src/ai_usage_cost/render/terminal.py|src/ai_usage_cost/render/terminal.py:20]]
3. 3. It picks the table for the requested grouping and prints it when the bucket list is not empty. [[src/ai_usage_cost/render/terminal.py|src/ai_usage_cost/render/terminal.py:29]]
4. 4. It lists unpriced models and tells the user to add them to rates.json. [[src/ai_usage_cost/render/terminal.py|src/ai_usage_cost/render/terminal.py:40]]
5. 5. It prints every warning when verbose, otherwise only a count. [[src/ai_usage_cost/render/terminal.py|src/ai_usage_cost/render/terminal.py:46]]

## Alternative flows

Step 3 alt: an unknown grouping name falls back to the model table. [[src/ai_usage_cost/render/terminal.py|src/ai_usage_cost/render/terminal.py:29]]
Start alt: no events found, the command prints a notice and exits with code 1. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:104]]

## Postconditions

The terminal shows a Total panel, one table for the chosen grouping, and the unpriced and warning notices when they apply.

## Acceptance criteria

The headline shows a prompt caching saving line only when the saving is above zero. [[src/ai_usage_cost/render/terminal.py|src/ai_usage_cost/render/terminal.py:62]]

## Code

- [[src/ai_usage_cost/cli.py]]
- [[src/ai_usage_cost/render/terminal.py]]
