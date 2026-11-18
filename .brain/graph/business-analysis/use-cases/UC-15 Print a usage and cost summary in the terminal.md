---
code: UC-15
primary_actor: CLI user
tags:
  - ba/use-case
maturity: approved
---
# Print a usage and cost summary in the terminal

## Description

A user runs the scan command and reads the headline cost and one breakdown table as text.

## Preconditions

Usage was found: the scan command exits with code 1 and a hint when the report has no events.

## Postconditions

The terminal shows a Total panel, one table for the chosen grouping, and the unpriced and warning notices when they apply.

## Main flow

1. 1. The user runs scan; the command builds the report and, when --json is not set, passes it to the terminal renderer. `src/ai_usage_cost/cli.py:105`
2. 2. The renderer prints the Total panel with cost, tokens, requests, sessions, date span, log file count and rates date. `src/ai_usage_cost/render/terminal.py:20`
3. 3. It picks the table for the requested grouping and prints it when the bucket list is not empty. `src/ai_usage_cost/render/terminal.py:29`
4. 4. It lists unpriced models and tells the user to add them to rates.json. `src/ai_usage_cost/render/terminal.py:40`
5. 5. It prints every warning when verbose, otherwise only a count. `src/ai_usage_cost/render/terminal.py:46`

## Alternative flows

Step 3 alt: an unknown grouping name falls back to the model table. `src/ai_usage_cost/render/terminal.py:29`
Start alt: no events found, the command prints a notice and exits with code 1. `src/ai_usage_cost/cli.py:104`

## Acceptance criteria

The headline shows a prompt caching saving line only when the saving is above zero. `src/ai_usage_cost/render/terminal.py:62`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/render/terminal.py::render | confirmed
  > def render(
