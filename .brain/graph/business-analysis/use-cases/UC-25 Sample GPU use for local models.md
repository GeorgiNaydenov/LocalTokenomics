---
code: UC-25
primary_actor: Person using the tool
subdomain: Usage collection
level: subfunction
actors:
  - Person using the tool
models:
  - AlertDecision
  - Analysis
  - ClientInfo
  - Facets
  - IngestSummary
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
  - files
  - messages
  - outcomes
  - requests
  - samples
  - session_exclusions
  - trace_events
rules:
  - A forgotten session is not stored again
  - A grown file resumes only when its earlier bytes are unchanged
  - A reported cost that differs is flagged
  - A request is stored once per fingerprint
  - A rise is measured against the window just before
  - A route without a store answers 503
  - A session shows its worst cost state
  - A session title prefers the tool, then the latest
  - An alert fires only above the threshold
  - An alert needs exactly one threshold
  - An excluded project drops its spans
  - An unchanged file is not parsed again
  - An unknown session answers 404
  - Chart colours follow position, not meaning
  - Content retention is inert
  - Day breakdown is listed oldest first
  - Empty project panel is left blank
  - Export accepts only json and png
  - Old rates raise a warning
  - PNG charts are limited to the top buckets
  - Records that disagree on input tokens keep the first
  - Schema migrations only run forward
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
# Sample GPU use for local models

## Description

The person records GPU load and memory while local models run, so energy can be estimated from a power rating.

## Preconditions

- A sampler is available: nvidia-smi, rocm-smi or Windows performance counters.

## Postconditions

- Samples are stored, and energy is shown when a power rating is given.

## Main flow

1. The person runs the collect command. `src/ai_usage_cost/cli.py:200`
2. The command picks a backend. `src/ai_usage_cost/collect.py:85`
3. Each interval it takes a sample and stores it. `src/ai_usage_cost/collect.py:275`
4. Energy is the rating times utilisation times elapsed time, only when a rating is given. `src/ai_usage_cost/collect.py:255`

## Alternative flows

- With no sampler the command prints that none is available and exits with code 1. `src/ai_usage_cost/cli.py:214`

## Acceptance criteria

- Energy is unavailable without a rating. `tests/test_collect.py:105`
- No rows are written when no backend exists. `tests/test_collect.py:87`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/cli.py::collect | inferred
  > def collect(
