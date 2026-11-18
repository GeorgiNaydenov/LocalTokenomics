---
code: UC-18
primary_actor: Person using the tool
subdomain: Spend reporting
level: goal
actors:
  - Person using the tool
models:
  - Report
  - SessionRow
rules:
  - An unknown session answers 404
tags:
  - ba/use-case
maturity: draft
---
# Explore spend in the dashboard

## Description

The person opens a local web dashboard to filter and compare cost by client, model, project and session.

## Preconditions

The dashboard bundle is built, otherwise the root page says how to build it.

## Postconditions

The browser shows the report; the interface answers the same filters as the command line.

## Main flow

1. The person runs the serve command, which scans the logs first. `src/ai_usage_cost/cli.py:109`
2. The command builds the application from the analysis. `src/ai_usage_cost/cli.py:133`
3. The browser asks for the meta data and the report. `src/ai_usage_cost/api.py:255`
4. The report route passes its filters to the same function the command line uses. `src/ai_usage_cost/api.py:304`
5. A refresh route analyses again and clears the span cache. `src/ai_usage_cost/api.py:390`

## Alternative flows

- Without the built bundle the root page returns a message to build it. `src/ai_usage_cost/api.py:401`

## Acceptance criteria

- The report has the expected shape. `tests/test_api.py:133`
- Each filter narrows the report. `tests/test_api.py:233`
- A filter that matches nothing returns an empty report. `tests/test_api.py:284`
- Refresh invalidates the span cache. `tests/test_api.py:392`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/api.py::create_app | inferred
  > def create_app(
