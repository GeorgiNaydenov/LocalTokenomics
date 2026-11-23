---
code: UC-13
primary_actor: User of Ai usage cost sources
subdomain: Ai usage cost sources area
models:
  - Analysis
  - Bucket
  - Capabilities
  - ClientInfo
  - ContextSnapshot
  - CostBreakdown
  - EconRow
  - Economics
  - Facets
  - IngestSummary
  - Insight
  - Meta
  - Outcome
  - OutcomeSignals
  - OutcomeUpdate
  - PricedEvent
  - Report
  - Sample
  - SeriesPoint
  - SessionRow
  - Source
  - SourceInfo
  - Span
  - SpanContent
  - Spec
  - TokenUsage
  - Totals
  - Trace
  - UnknownModel
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
rules:
  - A grown file resumes only when its earlier bytes are unchanged
  - A reader is found by its SOURCE value
  - A reported cost that differs is flagged
  - A request is stored once per fingerprint
  - A route without a store answers 503
  - A session shows its worst cost state
  - A session title prefers the tool, then the latest
  - An excluded project drops its spans
  - Content retention is inert
  - Experimental readers carry a flag
  - Muse Code control folders are skipped
  - Old rates raise a warning
  - Readers only read
  - Records that disagree on input tokens keep the first
  - Repeated Codex token totals are not counted twice
  - Schema migrations only run forward
  - Source databases are opened read only
  - Synthetic Claude Code records are not usage
  - Unparsable lines are skipped and counted
  - Unreadable span text answers 404
  - _values_match_provenance refuses when (value is None) != (provenance == 'unavailable')
  - _values_match_provenance validates the model
  - create_app refuses when not store.session_exists(conn, source, session_id)
  - create_app refuses when not store.session_exists(conn, source, session_id) (line 364)
  - create_app refuses when path is None
  - create_app refuses when span is None
  - forget_session refuses when not store.session_exists(conn, source, session_id)
  - opened refuses when path is None
  - session_spans refuses when not store.session_exists(conn, source, session_id)
  - span_content refuses when span is None
  - A forgotten session is not stored again
  - An unchanged file is not parsed again
  - An unknown session answers 404
  - The local calendar day decides the day of an event
events:
  - Analysis refreshed
  - Conflicting records warning
  - Estimated price warning
  - GPU sample recorded
  - Reported cost divergence warning
  - Session forgotten
  - Session rated
  - Stale rates warning
  - Tier unpriced warning
  - Unpriced model warning
tags:
  - ba/use-case
maturity: approved
---
# Discover AI tool usage from local files

## Description

The tool finds the logs and data stores of the supported AI coding tools on this machine and turns each into usage events, without changing any of them.

## Preconditions

- At least one supported tool has written data in a default root, or the user passes a root.

## Postconditions

- Usage events and a file record exist in the usage store for every readable file.

## Main flow

1. 1. The registry collects the SOURCE of every reader module. `src/ai_usage_cost/sources/__init__.py:17`
2. 2. The store keeps only the roots that exist. `src/ai_usage_cost/sources/base.py:49`
3. 3. The reader lists the files under each root. `src/ai_usage_cost/store.py:220`
4. 4. Unchanged files are skipped. `src/ai_usage_cost/store.py:230`
5. 5. The reader parses a changed file into usage events. `src/ai_usage_cost/store.py:255`
6. 6. The store writes the event rows and a file record. `src/ai_usage_cost/store.py:281`

## Alternative flows

- A file that cannot be read adds a warning and is skipped. `src/ai_usage_cost/store.py:225`

## Acceptance criteria

- The Claude Code reader skips synthetic and zero token records. `tests/test_claude_code.py:102`

## Glossary

- [[Reader]]
- [[Root]]
- Source

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/sources/__init__.py | inferred
  > def registry() -> dict[str, Source]:
