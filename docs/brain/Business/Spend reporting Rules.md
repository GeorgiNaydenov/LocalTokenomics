---
title: Spend reporting Rules
aliases: []
tags: [business, generated, rules, spec]
area: business
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [src/ai_usage_cost/aggregate.py, src/ai_usage_cost/api.py, src/ai_usage_cost/cli.py,
  src/ai_usage_cost/models.py, src/ai_usage_cost/pipeline.py]
generated: true
anchors: true
---

# Spend reporting Rules

> [!info] What this is
> The business rules of the [[Spend reporting]] subdomain, as the code enforces them. Each rule is a heading, so a use case links straight to it, and each names the line of code that enforces it.

## BR-116 The alert window ends today

The alert reports the window of local days that ends today and starts the given number of days back, today included. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:330]]

- **Category:** calculation
- **Used in:** [[UC-17 See what my AI usage would cost]], [[UC-18 Explore spend in the dashboard]], [[UC-19 Export a report as a file]], [[UC-20 Be alerted when spend rises]], [[UC-26 Query the store with SQL]], [[UC-27 Browse sessions in the terminal]]

Source:
- `alert`: `since = until - timedelta(days=days - 1)`

## BR-117 A rise is measured against the window just before

With the rise threshold the earlier window has the same length and ends the day before the current window starts. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:336]]

- **Category:** calculation
- **Used in:** [[UC-17 See what my AI usage would cost]], [[UC-18 Explore spend in the dashboard]], [[UC-19 Export a report as a file]], [[UC-20 Be alerted when spend rises]], [[UC-26 Query the store with SQL]], [[UC-27 Browse sessions in the terminal]]

Source:
- `alert`: `analysis, since=since - timedelta(days=days), until=since - timedelta(days=1)`

## BR-118 An alert fires only above the threshold

The alert fires when the compared amount is strictly greater than the threshold; an equal amount sends nothing. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:282]]

- **Category:** calculation
- **Used in:** [[UC-17 See what my AI usage would cost]], [[UC-18 Explore spend in the dashboard]], [[UC-19 Export a report as a file]], [[UC-20 Be alerted when spend rises]], [[UC-26 Query the store with SQL]], [[UC-27 Browse sessions in the terminal]]

Source:
- `alert_decision`: `return AlertDecision(fire=amount > threshold, message="\n".join(lines))`

## BR-120 A route without a store answers 503

A route that must open the store answers 503 when the analysis was built without a store path. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:223]]

- **Category:** interface
- **Used in:** [[UC-18 Explore spend in the dashboard]], [[UC-21 Inspect and rate one session]]

Source:
- `create_app.opened`: `raise HTTPException(503, "this analysis was built without a store")`

## BR-78 The local calendar day decides the day of an event

An event belongs to the machine's local calendar day, a timestamp without an offset is read as UTC, and both bucketing and date filters use the same function. [[src/ai_usage_cost/models.py|src/ai_usage_cost/models.py:146]]

- **Category:** reporting

Source:
- `local_day`: `return aware.astimezone().date()`

## BR-79 A session shows its worst cost state

The cost state of a session is the worst of its requests, ranked priced, free, unpriced, unavailable. [[src/ai_usage_cost/aggregate.py|src/ai_usage_cost/aggregate.py:640]]

- **Category:** reporting

Source:
- `sessions_of`: `row.cost_state = max(states[key], key=lambda s: _STATE_RANK[s])`

## BR-80 A session title prefers the tool, then the latest

The title of a session comes from the highest ranked title source among its events, a tool title first and a folder fallback last, and among equals the latest wins. [[src/ai_usage_cost/aggregate.py|src/ai_usage_cost/aggregate.py:21]]

- **Category:** reporting

Source:
- `_TITLE_SOURCE_RANK`: `Lower rank wins when picking a session's display title`

## BR-81 A reported cost that differs is flagged

A session whose tool reported cost and computed cost differ by more than five percent of the reported figure or one cent gets a warning. Free models are never compared. [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py:133]]

- **Category:** reporting
- **Used in:** [[UC-17 See what my AI usage would cost]]

Source:
- `reported_cost_divergences`: `if abs(reported - computed) > max(0.05 * reported, 0.01):`

## BR-82 Old rates raise a warning

When the rate table's as of date is more than 30 days old a warning asks for the table to be checked again. [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py:235]]

- **Category:** reporting
- **Used in:** [[UC-17 See what my AI usage would cost]]

Source:
- `analyze`: `if age is not None and age > STALE_INFO_DAYS:`

## BR-84 An alert needs exactly one threshold

The alert command needs a window length of at least one day and exactly one of a window total threshold or a rise threshold. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:323]]

- **Category:** reporting
- **Used in:** [[UC-17 See what my AI usage would cost]], [[UC-18 Explore spend in the dashboard]], [[UC-19 Export a report as a file]], [[UC-20 Be alerted when spend rises]], [[UC-26 Query the store with SQL]], [[UC-27 Browse sessions in the terminal]]

Source:
- `alert`: `pass --over or --rise-over, not both`

## BR-85 An unknown session answers 404

A session route for a source and session id that the store does not hold, or that was forgotten, answers 404. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:236]]

- **Category:** interface
- **Used in:** [[UC-18 Explore spend in the dashboard]], [[UC-21 Inspect and rate one session]]

Source:
- `create_app.session_spans`: `no session {session_id!r} under source {source!r}`
