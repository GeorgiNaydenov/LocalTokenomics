---
code: UC-22
primary_actor: Person using the tool
subdomain: Privacy and retention
level: goal
actors:
  - Person using the tool
models:
  - Span
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
  - Report
  - Sample
  - SeriesPoint
  - SessionRow
  - Source
  - SourceInfo
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
  - files
  - outcomes
  - requests
  - samples
  - session_exclusions
  - trace_events
rules:
  - A forgotten session is not stored again
  - A bad configuration file gives the defaults
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
  - An unknown session answers 404
  - An unpriced tier is billed standard and flagged
  - Cache prices fall back in a fixed order
  - Content retention is inert
  - Duplicate rate keys are rejected
  - Experimental readers carry a flag
  - Export accepts only json and png
  - Missing token counts mean unavailable
  - Old rates raise a warning
  - Only listed suffixes count as the same model
  - Peak windows must not wrap midnight
  - Price periods must not overlap
  - Readers only read
  - Records that disagree on input tokens keep the first
  - Released text is cut and then redacted
  - Schema migrations only run forward
  - Source databases are opened read only
  - Span text is refused in metadata only mode
  - The alert window ends today
  - The first covering period replaces the row prices
  - The largest band at or under the request size applies
  - The local calendar day decides the day of an event
  - The longest matching row wins
  - Unparsable lines are skipped and counted
  - Unreadable span text answers 404
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
# Forget a session

## Description

The person removes the trace of a session from the store and keeps it from coming back on later scans.

## Preconditions

- The session exists.

## Postconditions

- Its spans and rating are gone and an exclusion row is kept. Its requests stay in the totals.

## Main flow

1. The person sends a delete for the session. `src/ai_usage_cost/api.py:362`
2. The store deletes the spans and the rating. `src/ai_usage_cost/store.py:597`
3. It records an exclusion. `src/ai_usage_cost/store.py:601`
4. The span cache entry of that session is dropped. `src/ai_usage_cost/api.py:367`

## Alternative flows

- An unknown session answers 404. `src/ai_usage_cost/api.py:235`

## Acceptance criteria

- Deleting removes the trace but not the requests. `tests/test_api.py:553`
- The exclusion survives a later scan. `tests/test_store.py:665`
- Only the deleted session's cache entry is dropped. `tests/test_api.py:427`

## Glossary

- [[Session]]
- Span

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/api.py::create_app | inferred
  > def forget_session(source: str, session_id: str)
