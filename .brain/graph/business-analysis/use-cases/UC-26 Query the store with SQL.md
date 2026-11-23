---
code: UC-26
primary_actor: Person using the tool
subdomain: Spend reporting
level: subfunction
actors:
  - Person using the tool
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
# Query the store with SQL

## Description

The person explores the stored requests with SQL in a browser through Datasette.

## Preconditions

- The sql extra is installed and a store exists.

## Postconditions

- Datasette serves the store.

## Main flow

1. The person runs the sql command. `src/ai_usage_cost/cli.py:229`
2. The command needs Datasette. `src/ai_usage_cost/cli.py:235`
3. It checks that the store file exists. `src/ai_usage_cost/cli.py:239`
4. It hands the store to Datasette. `src/ai_usage_cost/cli.py:248`

## Alternative flows

- A missing store prints a hint and exits with code 2. `src/ai_usage_cost/cli.py:241`

## Acceptance criteria

- The explicit store is handed to Datasette. `tests/test_cli.py:219`
- A missing store is named instead of launching. `tests/test_cli.py:241`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/cli.py::sql | inferred
  > def sql(
