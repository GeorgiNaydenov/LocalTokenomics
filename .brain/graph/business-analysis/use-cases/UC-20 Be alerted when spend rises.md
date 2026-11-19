---
code: UC-20
primary_actor: Person using the tool
subdomain: Spend reporting
level: goal
actors:
  - Person using the tool
  - Notification target
models:
  - Report
rules:
  - An alert needs exactly one threshold
tags:
  - ba/use-case
maturity: approved
---
# Be alerted when spend rises

## Description

The person is notified through a service of their choice when the spend of a window, or its rise over the window before, passes a threshold.

## Preconditions

The alert extra is installed and one threshold is given.

## Postconditions

A notification is delivered when the threshold is crossed, and nothing is sent otherwise.

## Main flow

1. The person runs the alert command with a target and a threshold. `src/ai_usage_cost/cli.py:299`
2. The command checks the window and the threshold options. `src/ai_usage_cost/cli.py:323`
3. It builds the report for the window, and for the window before when the rise is asked for. `src/ai_usage_cost/cli.py:335`
4. It decides whether to fire. `src/ai_usage_cost/cli.py:282`
5. It sends the message to every target. `src/ai_usage_cost/cli.py:349`

## Alternative flows

- A rejected target exits with code 1. `src/ai_usage_cost/cli.py:347`
- A failed delivery exits with code 1. `src/ai_usage_cost/cli.py:353`
- A missing extra prints how to install it and exits with code 2. `src/ai_usage_cost/cli.py:53`

## Acceptance criteria

- Spend over the threshold fires and exactly at it does not. `tests/test_cli.py:73` `tests/test_cli.py:77`
- A drop never fires in rise mode. `tests/test_cli.py:90`
- The message lists unpriced and unavailable usage as excluded. `tests/test_cli.py:94`
- The command needs exactly one threshold. `tests/test_cli.py:150`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/cli.py::alert | inferred
  > def alert(
