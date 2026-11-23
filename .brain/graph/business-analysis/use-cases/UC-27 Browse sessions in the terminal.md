---
code: UC-27
primary_actor: Person using the tool
subdomain: Spend reporting
level: subfunction
actors:
  - Person using the tool
models:
  - SessionRow
  - AlertDecision
  - Analysis
  - ClientInfo
  - Facets
  - Meta
  - Report
  - Sample
  - SeriesPoint
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
# Browse sessions in the terminal

## Description

The person lists and sorts sessions in a terminal table and filters them as they type.

## Preconditions

- The tui extra is installed and the report has sessions.

## Postconditions

- A full screen table is shown.

## Main flow

1. The person runs the tui command. `src/ai_usage_cost/cli.py:358`
2. The command shows a notice and exits with code 1 when there are no sessions. `src/ai_usage_cost/cli.py:371`
3. The table is filled from the report sessions. `src/ai_usage_cost/tui.py:119`
4. A header click sorts and a second click reverses. `src/ai_usage_cost/tui.py:105`

## Alternative flows

- Without the extra the command prints an install hint and exits with code 2. `src/ai_usage_cost/cli.py:366`

## Acceptance criteria

- The filter matches any visible session field. `tests/test_cli.py:197`

## Glossary

- Report
- [[Session]]

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/cli.py::tui | inferred
  > def tui(
