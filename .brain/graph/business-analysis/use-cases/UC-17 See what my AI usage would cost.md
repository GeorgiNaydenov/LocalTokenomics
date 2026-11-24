---
code: UC-17
primary_actor: Person using the tool
subdomain: Spend reporting
level: goal
actors:
  - Person using the tool
  - AI coding tool logs
models:
  - UsageEvent
  - PricedEvent
  - Report
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
  - ProviderRules
  - RateTable
  - Sample
  - SeriesPoint
  - SessionRow
  - Source
  - SourceInfo
  - Span
  - SpanContent
  - TokenUsage
  - Totals
  - Trace
  - UnknownModel
  - UnpricedModel
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
  - An unchanged file is not parsed again
  - A model without a rate row is unpriced
  - The local calendar day decides the day of an event
  - A bad configuration file gives the defaults
  - A free provider costs zero
  - A known unpriced model beats a guess
  - A prefix match is an estimate
  - A row must name a defined provider
  - A settings file that cannot be loaded is ignored as a whole
  - An unpriced tier is billed standard and flagged
  - Cache prices fall back in a fixed order
  - Duplicate rate keys are rejected
  - Missing token counts mean unavailable
  - Only listed suffixes count as the same model
  - Peak windows must not wrap midnight
  - Price periods must not overlap
  - The first covering period replaces the row prices
  - The largest band at or under the request size applies
  - The longest matching row wins
  - _consistent refuses when duplicates
  - _consistent refuses when missing
  - _consistent validates the model
  - _disjoint_periods refuses when earlier.until is None or (later.from_ or date.min) ‹ ea
  - _disjoint_periods validates the model
  - _ordered refuses when self.from_ is not None and self.until is not None and (
  - _ordered validates the model
  - _sorted_bands validates bands
  - _valid_window refuses when any((not 0 ‹= day ‹= 6 for day in self.weekdays))
  - _valid_window refuses when any((not 0 ‹= start ‹ end ‹= 24 for start, end in self
  - _valid_window validates the model
  - read_content refuses when config.metadata_only or span.content_path is None
  - resolve_path refuses when index ›= len(current)
  - A forgotten session is not stored again
  - A grown file resumes only when its earlier bytes are unchanged
  - A reader is found by its SOURCE value
  - A reported cost that differs is flagged
  - A request is stored once per fingerprint
  - A rise is measured against the window just before
  - A route without a store answers 503
  - A session shows its worst cost state
  - A session title prefers the tool, then the latest
  - An alert fires only above the threshold
  - An alert needs exactly one threshold
  - An excluded project drops its spans
  - An unknown session answers 404
  - Chart colours follow position, not meaning
  - Content retention is inert
  - Day breakdown is listed oldest first
  - Empty project panel is left blank
  - Experimental readers carry a flag
  - Export accepts only json and png
  - Old rates raise a warning
  - PNG charts are limited to the top buckets
  - Readers only read
  - Records that disagree on input tokens keep the first
  - Released text is cut and then redacted
  - Schema migrations only run forward
  - Source databases are opened read only
  - Span text is refused in metadata only mode
  - Terminal table shows at most 30 rows
  - The alert window ends today
  - Unknown grouping falls back to model
  - Unparsable lines are skipped and counted
  - Unpriced models are shown but not totalled
  - Unreadable span text answers 404
  - Warnings are summarised unless verbose
  - _roots refuses when not path
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
  - session_spans refuses when not store.session_exists(conn, source, session_id)
  - span_content refuses when span is None
tags:
  - ba/use-case
maturity: approved
---
# See what my AI usage would cost

## Description

The person runs one command and sees what the usage of all their AI coding tools would have cost at list prices, by model, client, provider, project or day.

## Preconditions

- At least one supported tool has written logs on the machine, or the person points to them with a root option.

## Postconditions

- A report is printed or returned as JSON. The store holds the parsed requests for the next run.

## Main flow

1. The person runs the scan command, which accepts since, until, source, by, json, root, db, rates and rebuild options. `src/ai_usage_cost/cli.py:72`
2. The command analyses the logs. `src/ai_usage_cost/cli.py:87`
3. The analysis loads the privacy settings and opens the store. `src/ai_usage_cost/pipeline.py:175`
4. Changed files are ingested into the store. `src/ai_usage_cost/pipeline.py:178`
5. Stored requests are loaded and each is priced against the rate table. `src/ai_usage_cost/pipeline.py:198`
6. The report is filtered by the dates and sources. `src/ai_usage_cost/cli.py:88`
7. With the json option the report is printed as JSON. `src/ai_usage_cost/cli.py:96`
8. Otherwise the terminal tables are printed. `src/ai_usage_cost/cli.py:105`

## Alternative flows

- When the report has no requests the command prints that no usage was found and exits with code 1. `src/ai_usage_cost/cli.py:104`
- A model with no rate is listed as unpriced and left out of the total. `src/ai_usage_cost/render/terminal.py:34`

## Acceptance criteria

- Since and until include their boundary days. `tests/test_pipeline.py:71`
- Every breakdown sums to the grand total. `tests/test_pipeline.py:203`
- Unavailable and unpriced requests count but do not add cost. `tests/test_pipeline.py:486`
- Scanning twice changes nothing. `tests/test_store.py:158`

## Glossary

- [[Rate table]]
- Report
- [[Root]]
- Source

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/cli.py::scan | inferred
  > def scan(
