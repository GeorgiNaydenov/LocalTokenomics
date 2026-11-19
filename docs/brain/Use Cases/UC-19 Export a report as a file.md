---
title: UC-19 Export a report as a file
aliases: [UC-19, Export a report as a file]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [src/ai_usage_cost/cli.py, src/ai_usage_cost/render/png.py, tests/test_api.py]
generated: true
use-cases: [UC-19]
subdomain: Spend reporting
---

# UC-19 Export a report as a file

> [!info] What this is
> A use case of the [[Spend reporting]] subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Subdomain:** [[Spend reporting]]
- **Actors:** [[Actors#Person using the tool|Person using the tool]], [[Actors|Report]]
- **Maturity:** approved

## Description

The person saves a report as JSON for other tools or as a PNG chart to share.

## Preconditions

Logs or a store exist for the period.

## Main flow

1. The person runs the export command with an output path. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:176]]
2. The command analyses and builds the report for the dates. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:185]]
3. A json path gets the report as JSON. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:188]]
4. A png path gets four charts. [[src/ai_usage_cost/render/png.py|src/ai_usage_cost/render/png.py:18]]

## Alternative flows

- Any other extension is refused with exit code 2. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:194]]

## Postconditions

A file with the chosen extension is written.

## Acceptance criteria

- Computed fields are serialized in the report. [[tests/test_api.py|tests/test_api.py:199]]

## Business rules

- [[Spend reporting Rules#BR-116 The alert window ends today|BR-116 The alert window ends today]]
- [[Spend reporting Rules#BR-117 A rise is measured against the window just before|BR-117 A rise is measured against the window just before]]
- [[Spend reporting Rules#BR-118 An alert fires only above the threshold|BR-118 An alert fires only above the threshold]]
- [[Spend reporting Rules#BR-84 An alert needs exactly one threshold|BR-84 An alert needs exactly one threshold]]

## Code

- [[src/ai_usage_cost/cli.py]]
- [[src/ai_usage_cost/render/png.py]]
- [[tests/test_api.py]]
