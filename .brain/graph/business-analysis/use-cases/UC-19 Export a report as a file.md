---
code: UC-19
primary_actor: Person using the tool
subdomain: Spend reporting
level: goal
actors:
  - Person using the tool
models:
  - Report
rules: []
tags:
  - ba/use-case
maturity: draft
---
# Export a report as a file

## Description

The person saves a report as JSON for other tools or as a PNG chart to share.

## Preconditions

Logs or a store exist for the period.

## Postconditions

A file with the chosen extension is written.

## Main flow

1. The person runs the export command with an output path. `src/ai_usage_cost/cli.py:176`
2. The command analyses and builds the report for the dates. `src/ai_usage_cost/cli.py:185`
3. A json path gets the report as JSON. `src/ai_usage_cost/cli.py:188`
4. A png path gets four charts. `src/ai_usage_cost/render/png.py:18`

## Alternative flows

- Any other extension is refused with exit code 2. `src/ai_usage_cost/cli.py:194`

## Acceptance criteria

- Computed fields are serialized in the report. `tests/test_api.py:199`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/cli.py::export | inferred
  > def export(
