---
code: UC-15
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
  - A rise is measured against the window just before
  - An alert fires only above the threshold
  - Chart colours follow position, not meaning
  - Day breakdown is listed oldest first
  - Empty project panel is left blank
  - Export accepts only json and png
  - PNG charts are limited to the top buckets
  - Terminal table shows at most 30 rows
  - The alert window ends today
  - Unknown grouping falls back to model
  - Unpriced models are shown but not totalled
  - Warnings are summarised unless verbose
  - _roots refuses when not path
  - alert refuses when days ‹ 1
  - alert refuses when over is not None and rise_over is not None
  - alert refuses when threshold is None
  - A reported cost that differs is flagged
  - A route without a store answers 503
  - A session shows its worst cost state
  - A session title prefers the tool, then the latest
  - An alert needs exactly one threshold
  - An unknown session answers 404
  - Content retention is inert
  - Old rates raise a warning
  - Unreadable span text answers 404
  - create_app refuses when not store.session_exists(conn, source, session_id)
  - create_app refuses when not store.session_exists(conn, source, session_id) (line 364)
  - create_app refuses when path is None
  - create_app refuses when span is None
  - forget_session refuses when not store.session_exists(conn, source, session_id)
  - opened refuses when path is None
  - session_spans refuses when not store.session_exists(conn, source, session_id)
  - span_content refuses when span is None
events:
  - Spend alert sent
tags:
  - ba/use-case
maturity: approved
---
# Print a usage and cost summary in the terminal

## Description

A user runs the scan command and reads the headline cost and one breakdown table as text.

## Preconditions

- Usage was found: the scan command exits with code 1 and a hint when the report has no events.

## Postconditions

- The terminal shows a Total panel, one table for the chosen grouping, and the unpriced and warning notices when they apply.

## Main flow

1. 1. The user runs scan; the command builds the report and, when --json is not set, passes it to the terminal renderer. `src/ai_usage_cost/cli.py:105`
2. 2. The renderer prints the Total panel with cost, tokens, requests, sessions, date span, log file count and rates date. `src/ai_usage_cost/render/terminal.py:20`
3. 3. It picks the table for the requested grouping and prints it when the bucket list is not empty. `src/ai_usage_cost/render/terminal.py:29`
4. 4. It lists unpriced models and tells the user to add them to rates.json. `src/ai_usage_cost/render/terminal.py:40`
5. 5. It prints every warning when verbose, otherwise only a count. `src/ai_usage_cost/render/terminal.py:46`

## Alternative flows

- Step 3 alt: an unknown grouping name falls back to the model table. `src/ai_usage_cost/render/terminal.py:29`
- Start alt: no events found, the command prints a notice and exits with code 1. `src/ai_usage_cost/cli.py:104`

## Acceptance criteria

- The headline shows a prompt caching saving line only when the saving is above zero. `src/ai_usage_cost/render/terminal.py:62`

## Glossary

- Bucket
- Report
- Span

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/render/terminal.py::render | confirmed
  > def render(
