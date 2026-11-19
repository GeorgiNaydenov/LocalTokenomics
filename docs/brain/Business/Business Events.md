---
title: Business Events
aliases: []
tags: [business, events, generated, spec]
area: business
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [src/ai_usage_cost/api.py, src/ai_usage_cost/cli.py, src/ai_usage_cost/collect.py,
  src/ai_usage_cost/pipeline.py, src/ai_usage_cost/store.py]
generated: true
anchors: true
---

# Business Events

> [!info] What this is
> The things that happen in the business that the application reacts to or records. Each event names the code that raises or declares it.

## Analysis refreshed

Happens when the dashboard asks for a refresh: the analysis is rebuilt and the span cache is cleared. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:391]]

Source:
- `create_app.refresh`: `state["analysis"] = analyze(db_path=db_path, roots=roots, rates_path=rates_path)`

## Conflicting records warning

Raised when two records for one request disagree on input tokens. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:352]]

Source:
- `_insert`: `disagree on input tokens`

## Estimated price warning

Raised once per model priced from a shorter prefix, naming the parent rate and the token volume. [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py:225]]

Source:
- `analyze`: `has no rates.json row of its own`

## GPU sample recorded

Written once per successful reading of the GPU sampler, into the samples table. [[src/ai_usage_cost/collect.py|src/ai_usage_cost/collect.py:275]]

Source:
- `insert_sample`: `def insert_sample(conn: sqlite3.Connection, sample: Sample) -> None:`

## Reported cost divergence warning

Raised for a session whose tool reported cost and computed cost disagree. [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py:135]]

Source:
- `reported_cost_divergences`: `differs from`

## Session forgotten

Recorded when a person forgets a session: its spans and rating go and an exclusion is stored. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:595]]

Source:
- `delete_session`: `def delete_session(`

## Session rated

Recorded when a person stores an outcome for a session. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:568]]

Source:
- `put_outcome`: `def put_outcome(`

## Spend alert sent

Raised when the window's spend or rise crosses the threshold and the notification is delivered. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:349]]

Source:
- `alert`: `if not notifier.notify(`

## Stale rates warning

Raised when the rate table is older than the threshold. [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py:237]]

Source:
- `analyze`: `prices may have changed`

## Tier unpriced warning

Raised when requests ran on a tier the row has no price for and were billed at the standard rate. [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py:231]]

Source:
- `analyze`: `billed at the standard rate instead`

## Unpriced model warning

Raised once per model that has tokens and no rate. [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py:215]]

Source:
- `analyze`: `no rate for model {unknown.model!r}`
