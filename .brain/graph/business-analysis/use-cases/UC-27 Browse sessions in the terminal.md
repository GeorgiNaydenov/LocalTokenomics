---
code: UC-27
primary_actor: Person using the tool
subdomain: Spend reporting
level: subfunction
actors:
  - Person using the tool
models:
  - SessionRow
rules: []
tags:
  - ba/use-case
maturity: draft
---
# Browse sessions in the terminal

## Description

The person lists and sorts sessions in a terminal table and filters them as they type.

## Preconditions

The tui extra is installed and the report has sessions.

## Postconditions

A full screen table is shown.

## Main flow

1. The person runs the tui command. `src/ai_usage_cost/cli.py:358`
2. The command shows a notice and exits with code 1 when there are no sessions. `src/ai_usage_cost/cli.py:371`
3. The table is filled from the report sessions. `src/ai_usage_cost/tui.py:119`
4. A header click sorts and a second click reverses. `src/ai_usage_cost/tui.py:105`

## Alternative flows

- Without the extra the command prints an install hint and exits with code 2. `src/ai_usage_cost/cli.py:366`

## Acceptance criteria

- The filter matches any visible session field. `tests/test_cli.py:197`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/cli.py::tui | inferred
  > def tui(
