---
code: UC-19
primary_actor: Person using the tool
subdomain: Spend reporting
level: goal
actors:
  - Person using the tool
models:
  - Report
  - AlertDecision
  - Analysis
  - ClientInfo
  - Facets
  - Meta
  - Sample
  - SeriesPoint
  - SessionRow
  - SourceInfo
  - Totals
  - UnknownModel
  - WarningGroup
  - WarningInstance
  - WarningSummary
  - apps
  - chats
  - messages
  - samples
rules:
  - A reported cost that differs is flagged
  - A rise is measured against the window just before
  - A route without a store answers 503
  - A session shows its worst cost state
  - A session title prefers the tool, then the latest
  - An alert fires only above the threshold
  - An alert needs exactly one threshold
  - An unknown session answers 404
  - Chart colours follow position, not meaning
  - Content retention is inert
  - Day breakdown is listed oldest first
  - Empty project panel is left blank
  - Export accepts only json and png
  - Old rates raise a warning
  - PNG charts are limited to the top buckets
  - Terminal table shows at most 30 rows
  - The alert window ends today
  - Unknown grouping falls back to model
  - Unpriced models are shown but not totalled
  - Unreadable span text answers 404
  - Warnings are summarised unless verbose
  - _roots refuses when not path
  - alert refuses when days ‹ 1
  - alert refuses when over is not None and rise_over is not None
  - alert refuses when threshold is None
  - create_app refuses when not store.session_exists(conn, source, session_id)
  - create_app refuses when not store.session_exists(conn, source, session_id) (line 364)
  - create_app refuses when path is None
  - create_app refuses when span is None
  - forget_session refuses when not store.session_exists(conn, source, session_id)
  - opened refuses when path is None
  - session_spans refuses when not store.session_exists(conn, source, session_id)
  - span_content refuses when span is None
tags:
  - ba/use-case
maturity: approved
---
# Export a report as a file

## Description

The person saves a report as JSON for other tools or as a PNG chart to share.

## Preconditions

- Logs or a store exist for the period.

## Postconditions

- A file with the chosen extension is written.

## Main flow

1. The person runs the export command with an output path. `src/ai_usage_cost/cli.py:176`
2. The command analyses and builds the report for the dates. `src/ai_usage_cost/cli.py:185`
3. A json path gets the report as JSON. `src/ai_usage_cost/cli.py:188`
4. A png path gets four charts. `src/ai_usage_cost/render/png.py:18`

## Alternative flows

- Any other extension is refused with exit code 2. `src/ai_usage_cost/cli.py:194`

## Acceptance criteria

- Computed fields are serialized in the report. `tests/test_api.py:199`

## Glossary

- Report

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/cli.py::export | inferred
  > def export(
