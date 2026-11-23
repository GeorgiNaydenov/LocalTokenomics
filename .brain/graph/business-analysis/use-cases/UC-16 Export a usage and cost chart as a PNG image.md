---
code: UC-16
primary_actor: CLI user
subdomain: Ai usage cost render area
models:
  - AlertDecision
  - Analysis
  - ClientInfo
  - Facets
  - Meta
  - Report
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
# Export a usage and cost chart as a PNG image

## Description

A user runs the export command with a .png output path and receives a four panel chart of the report.

## Preconditions

- The output file name ends in .png.

## Postconditions

- An image file exists at the output path and the command prints its path.

## Main flow

1. 1. The user runs export with a path; the command builds the report and checks the file extension. `src/ai_usage_cost/cli.py:186`
2. 2. For .png it calls the picture writer. `src/ai_usage_cost/cli.py:192`
3. 3. The writer sets a title with cost, tokens and requests and draws cost per day, cost by model, token mix and cost by project. `src/ai_usage_cost/render/png.py:26`
4. 4. It creates the parent folder and saves the figure, then closes it. `src/ai_usage_cost/render/png.py:32`

## Alternative flows

- Step 1 alt: an extension other than .json or .png prints an error and exits with code 2. `src/ai_usage_cost/cli.py:56`

## Acceptance criteria

- The chart is written with the Agg backend, so no display is needed. `src/ai_usage_cost/render/png.py:9`

## Glossary

- Report

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/render/png.py::write_png | confirmed
  > def write_png(
