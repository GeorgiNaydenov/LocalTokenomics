---
title: UC-16 Export a usage and cost chart as a PNG image
aliases: [UC-16, Export a usage and cost chart as a PNG image]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [src/ai_usage_cost/cli.py, src/ai_usage_cost/render/png.py]
generated: true
use-cases: [UC-16]
subdomain: ''
---

# UC-16 Export a usage and cost chart as a PNG image

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Actors:** [[Actors#CLI user|CLI user]]
- **Maturity:** approved

## Description

A user runs the export command with a .png output path and receives a four panel chart of the report.

## Preconditions

The output file name ends in .png.

## Main flow

1. 1. The user runs export with a path; the command builds the report and checks the file extension. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:186]]
2. 2. For .png it calls the picture writer. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:192]]
3. 3. The writer sets a title with cost, tokens and requests and draws cost per day, cost by model, token mix and cost by project. [[src/ai_usage_cost/render/png.py|src/ai_usage_cost/render/png.py:26]]
4. 4. It creates the parent folder and saves the figure, then closes it. [[src/ai_usage_cost/render/png.py|src/ai_usage_cost/render/png.py:32]]

## Alternative flows

Step 1 alt: an extension other than .json or .png prints an error and exits with code 2. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:56]]

## Postconditions

An image file exists at the output path and the command prints its path.

## Acceptance criteria

The chart is written with the Agg backend, so no display is needed. [[src/ai_usage_cost/render/png.py|src/ai_usage_cost/render/png.py:9]]

## Business rules

- [[General Rules#BR-115 Chart colours follow position, not meaning|BR-115 Chart colours follow position, not meaning]]

## Code

- [[src/ai_usage_cost/cli.py]]
- [[src/ai_usage_cost/render/png.py]]
