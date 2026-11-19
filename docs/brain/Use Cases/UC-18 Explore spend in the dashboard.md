---
title: UC-18 Explore spend in the dashboard
aliases: [UC-18, Explore spend in the dashboard]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [src/ai_usage_cost/cli.py, src/ai_usage_cost/api.py, tests/test_api.py]
generated: true
use-cases: [UC-18]
subdomain: Spend reporting
---

# UC-18 Explore spend in the dashboard

> [!info] What this is
> A use case of the [[Spend reporting]] subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Subdomain:** [[Spend reporting]]
- **Actors:** [[Actors|An unknown session answers 404]], [[Actors#Person using the tool|Person using the tool]], [[Actors|Report]], [[Actors|SessionRow]]
- **Maturity:** approved

## Description

The person opens a local web dashboard to filter and compare cost by client, model, project and session.

## Preconditions

The dashboard bundle is built, otherwise the root page says how to build it.

## Main flow

1. The person runs the serve command, which scans the logs first. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:109]]
2. The command builds the application from the analysis. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:133]]
3. The browser asks for the meta data and the report. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:255]]
4. The report route passes its filters to the same function the command line uses. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:304]]
5. A refresh route analyses again and clears the span cache. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:390]]

## Alternative flows

- Without the built bundle the root page returns a message to build it. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:401]]

## Postconditions

The browser shows the report; the interface answers the same filters as the command line.

## Acceptance criteria

- The report has the expected shape. [[tests/test_api.py|tests/test_api.py:133]]
- Each filter narrows the report. [[tests/test_api.py|tests/test_api.py:233]]
- A filter that matches nothing returns an empty report. [[tests/test_api.py|tests/test_api.py:284]]
- Refresh invalidates the span cache. [[tests/test_api.py|tests/test_api.py:392]]

## Business rules

- [[Spend reporting Rules#BR-116 The alert window ends today|BR-116 The alert window ends today]]
- [[Spend reporting Rules#BR-117 A rise is measured against the window just before|BR-117 A rise is measured against the window just before]]
- [[Spend reporting Rules#BR-118 An alert fires only above the threshold|BR-118 An alert fires only above the threshold]]
- [[Spend reporting Rules#BR-120 A route without a store answers 503|BR-120 A route without a store answers 503]]
- [[Spend reporting Rules#BR-84 An alert needs exactly one threshold|BR-84 An alert needs exactly one threshold]]
- [[Spend reporting Rules#BR-85 An unknown session answers 404|BR-85 An unknown session answers 404]]

## Code

- [[src/ai_usage_cost/cli.py]]
- [[src/ai_usage_cost/api.py]]
- [[tests/test_api.py]]
