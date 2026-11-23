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
  - An alert needs exactly one threshold
  - A reported cost that differs is flagged
  - A rise is measured against the window just before
  - A route without a store answers 503
  - A session shows its worst cost state
  - A session title prefers the tool, then the latest
  - An alert fires only above the threshold
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
# Be alerted when spend rises

## Description

The person is notified through a service of their choice when the spend of a window, or its rise over the window before, passes a threshold.

## Preconditions

- The alert extra is installed and one threshold is given.

## Postconditions

- A notification is delivered when the threshold is crossed, and nothing is sent otherwise.

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

## Glossary

- Report

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/cli.py::alert | inferred
  > def alert(
