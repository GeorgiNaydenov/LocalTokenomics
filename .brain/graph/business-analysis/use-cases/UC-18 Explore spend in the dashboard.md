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
  - AlertDecision
  - Analysis
  - Bucket
  - Capabilities
  - ClientInfo
  - Config
  - ContextSnapshot
  - CostBreakdown
  - EconRow
  - Economics
  - Facets
  - IngestSummary
  - Insight
  - Meta
  - ModelMatch
  - ModelRate
  - Outcome
  - OutcomeSignals
  - OutcomeUpdate
  - PartialRules
  - Period
  - Prefix
  - PriceSet
  - PricedEvent
  - ProviderRules
  - RateTable
  - Sample
  - SeriesPoint
  - SourceInfo
  - Span
  - SpanContent
  - TokenUsage
  - Totals
  - Trace
  - UnknownModel
  - UnpricedModel
  - UsageEvent
  - WarningGroup
  - WarningInstance
  - WarningSummary
  - apps
  - chats
  - files
  - messages
  - outcomes
  - requests
  - samples
  - session_exclusions
  - trace_events
  - CostState
  - RowStatus
rules:
  - An unknown session answers 404
  - A bad configuration file gives the defaults
  - A forgotten session is not stored again
  - A free provider costs zero
  - A grown file resumes only when its earlier bytes are unchanged
  - A known unpriced model beats a guess
  - A model without a rate row is unpriced
  - A prefix match is an estimate
  - A reader is found by its SOURCE value
  - A reported cost that differs is flagged
  - A request is stored once per fingerprint
  - A rise is measured against the window just before
  - A route without a store answers 503
  - A row must name a defined provider
  - A session shows its worst cost state
  - A session title prefers the tool, then the latest
  - A settings file that cannot be loaded is ignored as a whole
  - An alert fires only above the threshold
  - An alert needs exactly one threshold
  - An excluded project drops its spans
  - An unchanged file is not parsed again
  - An unpriced tier is billed standard and flagged
  - Cache prices fall back in a fixed order
  - Chart colours follow position, not meaning
  - Content retention is inert
  - Day breakdown is listed oldest first
  - Duplicate rate keys are rejected
  - Empty project panel is left blank
  - Export accepts only json and png
  - Missing token counts mean unavailable
  - Old rates raise a warning
  - Only listed suffixes count as the same model
  - PNG charts are limited to the top buckets
  - Peak windows must not wrap midnight
  - Price periods must not overlap
  - Records that disagree on input tokens keep the first
  - Released text is cut and then redacted
  - Schema migrations only run forward
  - Span text is refused in metadata only mode
  - Terminal table shows at most 30 rows
  - The alert window ends today
  - The first covering period replaces the row prices
  - The largest band at or under the request size applies
  - The local calendar day decides the day of an event
  - The longest matching row wins
  - Unknown grouping falls back to model
  - Unpriced models are shown but not totalled
  - Unreadable span text answers 404
  - Warnings are summarised unless verbose
  - _consistent refuses when duplicates
  - _consistent refuses when missing
  - _consistent validates the model
  - _disjoint_periods refuses when earlier.until is None or (later.from_ or date.min) ‹ ea
  - _disjoint_periods validates the model
  - _ordered refuses when self.from_ is not None and self.until is not None and (
  - _ordered validates the model
  - _roots refuses when not path
  - _sorted_bands validates bands
  - _valid_window refuses when any((not 0 ‹= day ‹= 6 for day in self.weekdays))
  - _valid_window refuses when any((not 0 ‹= start ‹ end ‹= 24 for start, end in self
  - _valid_window validates the model
  - _values_match_provenance refuses when (value is None) != (provenance == 'unavailable')
  - _values_match_provenance validates the model
  - alert refuses when days ‹ 1
  - alert refuses when over is not None and rise_over is not None
  - alert refuses when threshold is None
  - create_app refuses when not store.session_exists(conn, source, session_id)
  - create_app refuses when not store.session_exists(conn, source, session_id) (line 364)
  - create_app refuses when path is None
  - create_app refuses when span is None
  - forget_session refuses when not store.session_exists(conn, source, session_id)
  - opened refuses when path is None
  - read_content refuses when config.metadata_only or span.content_path is None
  - resolve_path refuses when index ›= len(current)
  - session_spans refuses when not store.session_exists(conn, source, session_id)
  - span_content refuses when span is None
tags:
  - ba/use-case
maturity: approved
---
# Explore spend in the dashboard

## Description

The person opens a local web dashboard to filter and compare cost by client, model, project and session.

## Preconditions

- The dashboard bundle is built, otherwise the root page says how to build it.

## Postconditions

- The browser shows the report; the interface answers the same filters as the command line.

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

## Glossary

- [[Dashboard bundle]]
- Report
- [[Root]]
- [[Session]]
- Span

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/api.py::create_app | inferred
  > def create_app(
