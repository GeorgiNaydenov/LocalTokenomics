---
code: UC-24
primary_actor: Person using the tool
subdomain: Usage collection
level: goal
actors:
  - Person using the tool
models:
  - UsageEvent
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
# Try the tool with demo data

## Description

A new person sees a full dashboard from synthetic logs without exposing their own data.

## Preconditions

- None.

## Postconditions

- A demo tree and a demo store exist apart from the real ones.

## Main flow

1. The person runs the demo command. `src/ai_usage_cost/cli.py:141`
2. If the demo folder is missing the synthetic logs are generated. `src/ai_usage_cost/cli.py:161`
3. The command says the data is synthetic and that the real store is not touched. `src/ai_usage_cost/cli.py:163`
4. It serves the demo roots with the demo store. `src/ai_usage_cost/cli.py:171`

## Alternative flows

- With the off option the demo tree is deleted and the real logs are served. `src/ai_usage_cost/cli.py:151`

## Acceptance criteria

- The demo store is separate from the real store. `tests/test_demo.py:27`
- The demo shows priced, estimated and unpriced states. `tests/test_demo.py:89`
- Off removes the demo tree and serves real data. `tests/test_demo.py:61`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/cli.py::demo | inferred
  > def demo(
