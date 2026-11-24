---
code: UC-14
primary_actor: User of Ai usage cost sources
subdomain: Ai usage cost sources area
models:
  - Bucket
  - Capabilities
  - ContextSnapshot
  - CostBreakdown
  - EconRow
  - Economics
  - Insight
  - Outcome
  - OutcomeSignals
  - OutcomeUpdate
  - PricedEvent
  - Source
  - Span
  - SpanContent
  - TokenUsage
  - Trace
  - UsageEvent
  - CostState
rules:
  - Experimental readers carry a flag
  - Readers only read
  - Source databases are opened read only
  - The local calendar day decides the day of an event
  - Unparsable lines are skipped and counted
  - _values_match_provenance refuses when (value is None) != (provenance == 'unavailable')
  - _values_match_provenance validates the model
tags:
  - ba/use-case
maturity: approved
---
# Read a tool's SQLite store without a token count

## Description

For tools that keep conversations in a database and record no tokens, the reader still shows that sessions happened, with no token numbers.

## Preconditions

- The tool's database file exists in a default root.

## Postconditions

- One event per composer exists with tokens set to none.

## Main flow

1. 1. The reader lists the Cursor database files. `src/ai_usage_cost/sources/cursor.py:32`
2. 2. The reader checks that the expected table exists. `src/ai_usage_cost/sources/cursor.py:55`
3. 3. It selects the composer rows through the read only helper. `src/ai_usage_cost/sources/cursor.py:59`
4. 4. It yields one event per composer with no tokens. `src/ai_usage_cost/sources/cursor.py:79`

## Alternative flows

- A value that is not JSON is skipped. `src/ai_usage_cost/sources/cursor.py:66`

## Acceptance criteria

- The Cursor reader has its own test module. `tests/test_cursor.py:28`

## Glossary

- [[Reader]]
- [[Root]]

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/sources/cursor.py | inferred
  > def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
