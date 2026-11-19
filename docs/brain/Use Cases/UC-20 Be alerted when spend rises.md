---
title: UC-20 Be alerted when spend rises
aliases: [UC-20, Be alerted when spend rises]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [src/ai_usage_cost/cli.py, tests/test_cli.py]
generated: true
use-cases: [UC-20]
subdomain: Spend reporting
---

# UC-20 Be alerted when spend rises

> [!info] What this is
> A use case of the [[Spend reporting]] subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Subdomain:** [[Spend reporting]]
- **Actors:** [[Actors|An alert needs exactly one threshold]], [[Actors#Notification target|Notification target]], [[Actors#Person using the tool|Person using the tool]], [[Actors|Report]]
- **Maturity:** approved

## Description

The person is notified through a service of their choice when the spend of a window, or its rise over the window before, passes a threshold.

## Preconditions

The alert extra is installed and one threshold is given.

## Main flow

1. The person runs the alert command with a target and a threshold. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:299]]
2. The command checks the window and the threshold options. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:323]]
3. It builds the report for the window, and for the window before when the rise is asked for. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:335]]
4. It decides whether to fire. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:282]]
5. It sends the message to every target. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:349]]

## Alternative flows

- A rejected target exits with code 1. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:347]]
- A failed delivery exits with code 1. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:353]]
- A missing extra prints how to install it and exits with code 2. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:53]]

## Postconditions

A notification is delivered when the threshold is crossed, and nothing is sent otherwise.

## Acceptance criteria

- Spend over the threshold fires and exactly at it does not. [[tests/test_cli.py|tests/test_cli.py:73]] [[tests/test_cli.py|tests/test_cli.py:77]]
- A drop never fires in rise mode. [[tests/test_cli.py|tests/test_cli.py:90]]
- The message lists unpriced and unavailable usage as excluded. [[tests/test_cli.py|tests/test_cli.py:94]]
- The command needs exactly one threshold. [[tests/test_cli.py|tests/test_cli.py:150]]

## Business rules

- [[Spend reporting Rules#BR-116 The alert window ends today|BR-116 The alert window ends today]]
- [[Spend reporting Rules#BR-117 A rise is measured against the window just before|BR-117 A rise is measured against the window just before]]
- [[Spend reporting Rules#BR-118 An alert fires only above the threshold|BR-118 An alert fires only above the threshold]]
- [[Spend reporting Rules#BR-84 An alert needs exactly one threshold|BR-84 An alert needs exactly one threshold]]

## Code

- [[src/ai_usage_cost/cli.py]]
- [[tests/test_cli.py]]
